import csv
import pandas as pd
from io import StringIO
from lenders.models import Lender
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from csv_in_bulk.authenticators import basic_auth_logged_in
from csv_in_bulk.helpers import convert_bool_string_to_bool
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework import status
from django.http import StreamingHttpResponse
import datetime


class PseudoBuffer:
    """
    mock file-likeinterface.
    """
    def write(self, value):
        """
        zero buffer
        """
        return value

def row_generator(header):
    yield header
    for dg in (model_to_dict(x) for x in Lender.objects.all()):
        temp = []
        for field in header:
            temp.append(dg[field])
        yield temp


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def csv_in_bulk(request):
    if basic_auth_logged_in(request):
        if request.method == 'POST':
            #these will be used for determining the response status code and the response json
            csv_parsing_errors, items_not_added,items_added  = [], [], []
            try:
                df = pd.read_csv(StringIO(request.read().decode(encoding='utf-8')))
            except (UnicodeDecodeError, pd.errors.EmptyDataError) as e:# handles issues with the csv file
                csv_parsing_errors.append({'exception':str(e)})
            else:
                for _,row in df.iterrows():
                    new_lender = None
                    try:
                        new_lender = Lender(name=str(row['name']),
                               code=str(row['code']),
                               upfront_commission_rate=float(row['upfront_commission_rate']),
                               trial_commission_rate=float(row['trial_commission_rate']),
                               active=convert_bool_string_to_bool(row['active'])
                               )
                        new_lender.full_clean()
                        new_lender.save()
                    except (IntegrityError,ValidationError) as e:#handles issues with object creation
                        if new_lender:#for avoiding calling .mode_to_dict() on a None object
                            item_content = model_to_dict(new_lender)
                        else: #in case new lender cannot be retrieved, use row['name'] to provide diagnosis clues
                            item_content = row['name']
                        items_not_added.append({'item': item_content,'exception': str(e)})
                    else:
                        items_added.append({'item': model_to_dict(new_lender),'exception': None})
            #decide response code after object creation
            if items_added and not items_not_added:
                response_code = status.HTTP_200_OK
            else:
                response_code = status.HTTP_207_MULTI_STATUS
            if csv_parsing_errors:
                response_code = status.HTTP_400_BAD_REQUEST
            # return a json containing the result of this upload attempt
            return JsonResponse({
                                 'csv_parsing_errors': csv_parsing_errors,
                                 'items_added':items_added,
                                 'items_not_added':items_not_added
                                 },
                                 status=response_code)
        else:#GET request for CSV download
            a_lender = Lender.objects.first() # store in memory first to prevent race condition when getting the header
            if a_lender:
                csv_writer = csv.writer(PseudoBuffer())
                header =[k for k,v in model_to_dict(a_lender).items()]
                writer_generator = (csv_writer.writerow(row) for row in row_generator(header))
            else:
                writer_generator = iter(())#empty generator for returning an empty csv file
            datetime_str_now = datetime.datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
            #stream the response to protect load balancer and feed the stream with write_generator to prevent memory hog
            return StreamingHttpResponse(writer_generator,content_type="text/csv",headers={"Content-Disposition": f'attachment; filename="bulk_download_{datetime_str_now}.csv"'})
    else:
        return JsonResponse(data={'error':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
from rest_framework.renderers import BaseRenderer
import pandas as pd

class CSVRenderer(BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'
    def render(self, data, media_type=None, renderer_context={}):
        if 'id' in data:
            content = [data]
        else:
            content = data['results']
        return str(pd.DataFrame(data=content).to_csv(index=False))
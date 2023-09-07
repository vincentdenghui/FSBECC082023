from rest_framework import serializers
from lenders.models import Lender


class LenderSerializer(serializers.HyperlinkedModelSerializer):

    options = serializers.HyperlinkedRelatedField(
                                                    view_name='lender-detail',
                                                    lookup_field = 'code',
                                                    many=False,
                                                    read_only=True,
                                                )
    class Meta:
        model = Lender
        fields = ['id', 'url', 'name', 'code', 'upfront_commission_rate', 'trial_commission_rate', 'active', 'options']
        lookup_field = 'code'
        extra_kwargs = {
            'url': {'lookup_field': 'code'}
        }
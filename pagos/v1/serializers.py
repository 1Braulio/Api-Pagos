from rest_framework import serializers
from pagos.models import PagosV1

class PagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagosV1
        fields = '__all__'
        read_only_fields = '__all__',
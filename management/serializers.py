from . models import Employee
from rest_framework import serializers


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'position',
            'last_name',
            'first_name',
            'second_name',
            'status',
            'iin',
            'date_of_birth'
            'phone_number',
            'city',
            'street',
            'house',
            'apartment'
        )


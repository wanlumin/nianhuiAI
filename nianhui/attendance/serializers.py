#coding=utf-8
from rest_framework import serializers
from nianhui.attendance.models import Person


class EmployeeSerializer(serializers.ModelSerializer):

    def validate_employee_id(self,value):
        try:
            employee = Person.objects.get(employee_id=value)
        except:
            raise serializers.ValidationError("person not found")
        return value

    def update(self,instance,validated_data):
        instance.snap_pic=validated_data.get('snap_pic')
        instance.save()
        return instance

    class Meta:
        model = Person
        fields = ("employee_id","snap_pic")

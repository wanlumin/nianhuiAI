#coding=utf-8
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from nianhui.attendance.serializers import EmployeeSerializer
from nianhui.attendance.models import Person,Awards
from django.db.models import Q
import json,random

def constructed_ret(code=200,message="",success=0,data={"data":None}):
    ret = {}
    ret.update({"code":code})
    ret.update({"message":json.dumps(message,ensure_ascii=False)})
    ret.update({"success":success})
    ret.update(data)
    return ret

class AttendanceView(APIView):
    def post(self, request):
        employee_id = request.data['employee_id']
        employee = Person.objects.get(employee_id=employee_id)
        serializer = EmployeeSerializer(employee,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(constructed_ret(message=u'上传成功'))
        return Response(constructed_ret(code=200, message=serializer.errors, success=1))

    def get(self, request):
        employee_list = Person.objects.filter(Q(flag=0)&(~Q(snap_pic='')))
        ret_list = []
        list = {}
        ret = {}
        for employee in employee_list:
            employee.flag = 1
            employee.save()
            sub_ret = {}
            sub_ret.update({"id": employee.id})
            sub_ret.update({"name": employee.name})
            sub_ret.update({"depart_name": employee.depart_name})
            sub_ret.update({"origin_pic": employee.origin_pic})
            sub_ret.update({"snap_pic": employee.snap_pic.url})
            sub_ret.update({"employee_id": employee.employee_id})
            ret_list.append(sub_ret)
        list.update({'list':ret_list})
        ret.update({'data':list})

        return Response(constructed_ret(data=ret))

class AllAttendanceView(APIView):

    def get(self, request):
        employee_list = Person.objects.all()
        ret_list = []
        ret = {}
        for employee in employee_list:
            employee.flag = 1
            employee.save()
            sub_ret = {}
            sub_ret.update({"id": employee.id})
            sub_ret.update({"name": employee.name})
            sub_ret.update({"depart_name": employee.depart_name})
            sub_ret.update({"origin_pic": employee.origin_pic})
            sub_ret.update({"snap_pic": employee.snap_pic.url})
            sub_ret.update({"employee_id": employee.employee_id})
            ret_list.append(sub_ret)
        ret.update({'data':ret_list})

        return Response(constructed_ret(data=ret))

class AwardsView(APIView):
    type_list ={1:'employee',2:'leader'}

    def format_data(self,list,award_name,id):
        details = []
        ret = {}
        for item in list:
            sub_ret = {}
            sub_ret.update({"id": item.id})
            sub_ret.update({"name": item.name})
            sub_ret.update({"depart_name": item.depart_name})
            sub_ret.update({"origin_pic": item.origin_pic})
            sub_ret.update({"snap_pic": item.snap_pic.url})
            sub_ret.update({"employee_id": item.employee_id})
            details.append(sub_ret)
        sum = len(details)
        ret.update({"id": id})
        ret.update({"total": sum})
        ret.update({"award_name": award_name})
        ret.update({"details": details})
        return ret


    def get(self, request):
        ret = {}
        data = {}
        employee_list = Person.objects.filter(award_id=1)
        employee_award = Awards.objects.get(pk=1)
        leader_list = Person.objects.filter(award_id=2)
        leader_award = Awards.objects.get(pk=2)
        employee = self.format_data(employee_list, employee_award.award_name,employee_award.id)
        leader = self.format_data(leader_list, leader_award.award_name,leader_award.id)
        ret.update({"employee": employee})
        ret.update({"leader": leader})
        data.update({"data": ret})
        return Response(constructed_ret(data=data))

class RandomView(APIView):

    def get(self, request):
        num = request.GET.get("num")
        employee_list = Person.objects.filter(Q(flag=0) & (Q(snap_pic='')))
        employee_num = len(employee_list)
        if(employee_num<int(num)):
            sample = random.sample(range(len(employee_list)), int(employee_num))
        else:
            sample = random.sample(range(len(employee_list)), int(num))
        result = [employee_list[i] for i in sample]
        for employee in result:
            employee.snap_pic =employee.origin_pic
            employee.flag = 1
            employee.save()
        return Response(constructed_ret())

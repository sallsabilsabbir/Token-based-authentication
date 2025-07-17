
from django.shortcuts import render
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Create your views here.

# for "GET","POST"
@extend_schema(
    methods=["GET", "POST"],
    request=EmployeeSerializer,
    responses=EmployeeSerializer
)

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def employee_list_create(request, pk = None):

    if request.method == "GET":
        id = pk
        #for single id value
        if id is not None:
            try:
                emp = Employee.objects.get(id=id)
                serializer = EmployeeSerializer(emp)
                return Response(serializer.data)
            except Employee.DoesNotExist:
                return Response([],status=status.HTTP_200_OK)
            
        emp = Employee.objects.all()
        serializer= EmployeeSerializer(emp, many=True)
        return Response(serializer.data)

    
            
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Successfully Insert Data"})
        return Response(serializer.errors)
    

    
# for "RETRIVE","PUT","DELETE"
@extend_schema(
    methods=["GET", "PUT", "DELETE"],
    request=EmployeeSerializer,
    responses=EmployeeSerializer
)
@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def employee_retrive_put_delete(request, pk = None):

    if request.method == "GET":
        id = pk
        #for single id value
        if id is not None:
            try:
                emp = Employee.objects.get(id=id)
                serializer = EmployeeSerializer(emp)
                return Response(serializer.data)
            except Employee.DoesNotExist:
                return Response([],status=status.HTTP_200_OK)
            
        emp = Employee.objects.all()
        serializer= EmployeeSerializer(emp, many=True)
        return Response(serializer.data)

    
    if request.method == 'PUT':
        id = pk
        emp = Employee.objects.get(pk=id)
        serializer = EmployeeSerializer(emp, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Update Data Successfully"})
        return Response(serializer.errors)
    
    if request.method=='DELETE':
        id=pk
        emp = Employee.objects.get(id=pk)
        emp.delete()
        return Response({"msg":"Delete Successfully"})
    








from django.shortcuts import render

"""
    REST LIBRARY IMPORT
"""

from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView

"""
    IMPORT CORE FILES 
"""
from  kreedo.general_views import Mixins,GeneralClass

"""
    IMPORT USER APP FILE
""" 
from django.contrib.auth.models import User
from .serializer import*
from  ..models import*
from .filters import*
import traceback

import logging

logger = logging.getLogger(__name__)

# A simple string logged at the "warning" level
logger.warning("Your log message is here")

# A string with a variable at the "info" level
logger.info("The value of var is test")



# Create your views here.
""" Role List and Create API"""
class RoleListCreate(Mixins,GeneralClass,ListCreateAPIView):
    model = Role
    serializer_class = RoleSerializer
    filterset_class = RoleFilter

""" Role Retrive, Update and Delete  API"""
class RoleRetriveUpdateDestroy(Mixins,GeneralClass,RetrieveUpdateDestroyAPIView):
    model = Role
    serializer_class = RoleSerializer
    filterset_class = RoleFilter

""" Reporting_to  List and Create API"""
class ReportingToListCreate(Mixins, GeneralClass, ListCreateAPIView):
    model = ReportingTo
    serializer_class = ReportingToSerializer
    filterset_class  = ReportingToFilter

""" Reporting to  Retrive, Update and Delete  API"""
class ReportingToRetriveUpdateDestroy(Mixins, GeneralClass, RetrieveUpdateDestroyAPIView):
    model = ReportingTo
    serializer_class = ReportingToSerializer
    filterset_class  = ReportingToFilter



""" User Register API """
class UserRegister(CreateAPIView):
    def post(self, request):
        try:
            user_data = {
                "username":"test",
                "password":request.data.get('password', None),
                "first_name":request.data.get('first_name', None),
                "last_name":request.data.get('last_name', None),
                "email":request.data.get('email', None)
                
            }
            user_detail_data = {
                "phone":request.data.get('phone',None),
                "reason_for_discontinution":request.data.get('reason_for_discontinution',None),
                "relationship_with_child":request.data.get('relationship_with_child',None),
                "role":request.data.get('role', None),
                "own_schools":request.data.get('own_schools',None),
                "school":request.data.get('school',None)
             
            }
            
            address_detail ={
                "country":request.data.get('country', None),
                "state":request.data.get('state', None),
                "city":request.data.get('city', None),
                "address":request.data.get('address', None),
                "pincode":request.data.get('pincode', None)
            }


            # Using Context pass dict into serialzer 
            context = super().get_serializer_context()
            context.update({"user_data": user_data, "user_detail_data": user_detail_data,
                            "address_detail": address_detail})

            # print("context",context)
            """  Pass dictionary through Context """

            user_data_serializer = UserRegisterSerializer(data=dict(user_data), context=context)
            if user_data_serializer.is_valid():
                print("user", user_data_serializer.data)
            else:
                print("else",user_data_serializer.errors)
                print("trac", traceback.print_exc())
            
           
        except Exception as ex:
            logger.debug("Entering index method")
            # print("Exception",ex)
            # print("traceback",traceback.print_exc())
           



           

        
    





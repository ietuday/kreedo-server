import traceback
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from kreedo.general_views import*
from child.models import*
from .edoofun_serializer import*
from .filters import*
from session.models import*
from schools.models import*
from users.api.serializer import*
from rest_framework import status
from datetime import date

""" import Logger """

from kreedo.conf import logger
from kreedo.conf.logger import CustomFormatter
import logging

""" Logger Function """


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")


"""  Register Child """


class RegisterChild(ListCreateAPIView):
    def post(self, request):
        try:
            child_detail = {
                "photo": request.data.get('photo', None),
                "first_name": request.data.get('first_name', None),
                "last_name": request.data.get('last_name', None),
                "date_of_birth": request.data.get('date_of_birth', None),
                "class_teacher": request.data.get('class_teacher', None),
                "school_name": request.data.get('school_name', None),
                "account_manager": request.data.get('account_manager', None),
                "parent": ""
            }
            parent_detail = {
                "parents": request.data.get('parents', None)
            }
            academic_session_detail = {
                "section": request.data.get('section', None),
                "grade": request.data.get('grade', None)
            }

            """  Pass dictionary through Context """
            context = super().get_serializer_context()
            context.update(
                {"child_detail": child_detail, "parent_detail": parent_detail,
                 "academic_session_detail": academic_session_detail})

            try:

                child_detail_serializer = ChildRegisterSerializer(
                    data=dict(child_detail), context=context)
                if child_detail_serializer.is_valid():
                    child_detail_serializer.save()

                    context = {"isSuccess": True, "message": "Child register successfully", "status": status.HTTP_200_OK,
                               "error": "", "data": child_detail_serializer.data}
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context = {"isSuccess": True, "message": "Issue in Child Creation", "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                               "error": child_detail_serializer.errors, "data": ""}
                    return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as ex:
                print("ERROR---1", ex)
                context = {"isSuccess": False, "message": "Issue in Child Creation", "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                           "error": ex, "data": ""}
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            print("Traceback------", traceback.print_exc())
            print("ERROR----2", ex)
            context = {"isSuccess": False, "message": "Issue in Child Creation", "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" child list by section id """


class ChildListAssociatedToSectionID(ListCreateAPIView):
    def post(self, request):
        try:
            print(request)
            # if request.data['school'] == school:

        except Exception as ex:
            print("Traceback------", traceback.print_exc())
            print("ERROR----2", ex)
            context = {"isSuccess": False, "message": "Issue in Child Creation", "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


""" Update Secret Pin For Selected Child """


class UpdateSecretPinForSelectedChild(ListCreateAPIView):
    def post(self, request):
        try:
            print(request.data)
            child_detail = {
                "child": request.data.get('child', None),
                "parent_id": request.data.get('parent', None),
                "old_pin": request.data.get('old_pin', None),
                "new_pin": request.data.get('new_pin', None)
            }

            context = super().get_serializer_context()
            context.update({"child_detail": child_detail})
            print("child_detail-----------", child_detail)
            child_detail_serilaizer = UpdateSecretPinForChildSerializer(
                data=request.data, context=context)

            if child_detail_serilaizer.is_valid():
                child_detail_serilaizer.save()
                print("child_detail_serilaizer------>")
                context = {'isSuccess': True, 'message': "Pin changed Successfully",
                            "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)

            else:
                print("child_detail_serilaizer errors ------->",
                      child_detail_serilaizer.errors)
                context = {'isSuccess': False, 'message': "Child Not Found",
                           'data': " ", "error":user_qs_serializer.errors,"statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print("Traceback------", traceback.print_exc())
            print("ERROR----2", ex)
            context = {"isSuccess": False, "message": "Issue in Child Reset Pin", "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



""" GetChildListBasedOnParentID """
class GetChildListBasedOnParentID(ListCreateAPIView):
    def get(self, request, pk):
        try:
            print("@@@@@@@@@@@@@@@3",pk)
            child_qs = Child.objects.filter(parent=pk)
            if child_qs:
                child_qs_serializer = ChildListParentSerializer(child_qs,many=True)
                print("child_qs----",child_qs)  
                context = {'isSuccess': True, 'message': "Child List based on ParentId",'data': child_qs_serializer.data,
                            "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, 'message': "Child List based on ParentId Not Found",
                           'data': " ", "error":child_qs_serializer.errors,"statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print("Traceback------", traceback.print_exc())
            print("ERROR----2", ex)
            context = {"isSuccess": False, "message": "Issue in Child Creation", "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




""" GetChildDetailsBasedOnChildID  """
class GetChildDetailsBasedOnChildID(RetrieveUpdateDestroyAPIView):
    model = Child
    filterset_class = ChildFilter


    def get(self, request, pk):
        try:
            print("@@@@@@@@@@@@@@@3",pk)
            child_qs = Child.objects.filter(id=pk)
            if child_qs:
                child_qs_serializer = ChildDetailSerializer(child_qs,many=True)
                print("child_qs----",child_qs)  
                context = {'isSuccess': True, 'message': "Child Detail based on Child Id",'data': child_qs_serializer.data,
                            "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, 'message': "Child Detail based on Child Id Not Found",
                           'data': " ", "error":child_qs_serializer.errors,"statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print("Traceback------", traceback.print_exc())
            print("ERROR----2", ex)
            context = {"isSuccess": False, "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""  GetChildListAssociatedToLicenseID """

class GetChildListAssociatedToLicenseID(ListCreateAPIView):
    def post(self, request):
        try:
            child_qs = Child.objects.filter(school=request.data.get('school',None),
            school__license = request.data.get('license',None))
            print("@@@@@@@@@@", child_qs)
            if len(child_qs) !=0:
                child_qs_serializer = ChildListbylicenseSerializer(child_qs,many=True)
                print("child_qs----",child_qs)  
                context = {'isSuccess': True, 'message': "Child List associated to License Id",'data': child_qs_serializer.data,
                            "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, 'message': "Child List associated to License Id Not Found",
                           'data': " ", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print("Traceback------", traceback.print_exc())
            print("ERROR----2", ex)
            context = {"isSuccess": False, "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from area_of_devlopment.api.edoofun_serializer import*

""" GetSkillsAssociatedToChildId """
class GetSkillsAssociatedToChildId(ListCreateAPIView):
    def get(self, request,pk):
        try:
            child_qs = ChildPlan.objects.filter(child=pk).values('subjects')
            print("child_qs------",child_qs)
            activity_qs = Subject.objects.filter(id__in= child_qs).values('activity')
            print("activity_qs",activity_qs)
            skill_qs = Skill.objects.filter(activity__in=activity_qs)
            print("SKILLL---------------", skill_qs)
            if len(skill_qs) != 0:
                skill_qs_serializer = SkillListForChildSerializer(skill_qs, many=True)
                context = {'isSuccess': True, 'message': "Skills Associated To Child Id",'data': skill_qs_serializer.data,
                            "statusCode": status.HTTP_200_OK}
                return Response(context, status=status.HTTP_200_OK)
            else:

                context = {'isSuccess': False, 'message': "Skills Associated To Child Id Not Found",
                           'data': " ", "statusCode": status.HTTP_404_NOT_FOUND}
                return Response(context, status=status.HTTP_404_NOT_FOUND)



        except Exception as ex:
            print("Traceback------", traceback.print_exc())
            print("ERROR----2", ex)
            context = {"isSuccess": False, "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                       "error": ex, "data": ""}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


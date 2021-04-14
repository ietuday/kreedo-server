from django.shortcuts import render
from django.shortcuts import render
from .serializer import*
from .filters import*
from kreedo.general_views import*
from material.models import*

from rest_framework .generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
# Create your views here.

""" List and Create of Material """


class MaterialListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = Material
    filterset_class = MaterialFilter
    serializer_class = MaterialSerializer


""" Retrive Update Delete Material """


class MaterialRetriveUpdateDestroy(GeneralClass, Mixins, RetrieveUpdateDestroyAPIView):
    model = Material
    filterset_class = MaterialFilter
    serializer_class = MaterialSerializer


""" Activity Master Supporting Material List and Create  """


class ActivityMasterSupportingMaterialListCreate(GeneralClass, Mixins, ListCreateAPIView):
    model = ActivityMasterSupportingMaterial
    # filterset_class = ActivityMasterSupportingMaterialFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityMasterSupportingMaterialListSerializer
        if self.request.method == 'POST':
            return ActivityMasterSupportingMaterialCreateSerializer

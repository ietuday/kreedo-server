from kreedo.renderers.api_renderer import Renderer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import *


class GeneralClass(object):
    renderer_classes = (Renderer,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]


class Mixins(GenericAPIView):

    def get_queryset(self):
        model = self.model
        queryset = model.objects.all()
        return queryset




class Mixin(GenericAPIView):

    def get_queryset(self):
        model = self.model
        queryset = model.objects.all().order_by('id')
        return queryset

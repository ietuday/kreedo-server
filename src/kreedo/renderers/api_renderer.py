from collections import OrderedDict
from rest_framework import renderers
import json
import rest_framework.status
from rest_framework.pagination import LimitOffsetPagination
from kreedo.utils import*

""" 
    Custom renderer extends jsonRenderer class. 
    render method to render json custom response. 
    Returns paginated response if request has 'limit' and 'offset' parameter .
"""


class Renderer(renderers.JSONRenderer, LimitOffsetPagination):

    charset = 'utf-8'
    max_limit = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            context_request = renderer_context['request']
            response_obj = renderer_context['response']

            """ 
                Get URL method 
            """
            absolute_url, method = get_url(context_request)
            """ 
                according URL getting Message 
            """
            message = get_message(absolute_url, method)

            limit = absolute_url.find('limit')
            offset = absolute_url.find('offset')

            # if limit != -1 and offset != -1:
            #     print("Data---->", data)
            #     print("context_request", context_request)
            #     paginated_data = super().paginate_queryset( queryset=data, request=context_request)
            #     print("@@@@@@@@@@@@@", paginated_data)
            #     data = self.get_paginated_response(paginated_data)
            """
                if data == None or 'detail not in data : 
                this we use when we have 'detail' in data and for DELETE method. 
                find way to integrate both this three in one if statements.
            """
            
            response = get_response(data, response_obj, message)

            try:
                return response
            except Exception as ex:
                raise Exception("Error", ex)
        except Exception as ex:
            raise Exception("Error", ex)

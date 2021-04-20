import json
import rest_framework.status
import logging
from kreedo.conf.logger import*


""" Create Log for Utils"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")

""" 
    Extracting url and method name from request
"""


def get_url(request_obj):
    try:
        data = str(request_obj).split()
        method = data[1]
        url0 = data[2].rstrip('>')
        url1 = url0.strip("'/")
        url2 = url1.split("/")
        url = url2[1]

        return url, method
    except Exception as ex:
        logger.info(ex)
        logger.debug(ex)
        raise Exception(ex)


""" 
    Generating generic message based on method and url
# """


def get_message(api_name, method):
    apiname_list = api_name.split('_')

    model_name = ['user-type', 'role', 'grade', 'subject', 'section',
                  'license', 'school', 'school-session', 'academic-session',
                  'section-subject-teacher', 'subject-school-grade-plan',
                  'school-holiday', 'school-weak-off', 'calendar', 'package',
                  'school-package', 'plan', 'child-plan', 'plan-activity',
                  'activity', 'activity-asset', 'material',
                  'activity-master-supporting-material', 'area-of-devlopment',
                  'concept', 'skill', 'room', 'period-template',
                  'period-template-detail']

    for name in model_name:
        if name in apiname_list:
            if 'retrive' in apiname_list and method == 'GET':
                return f'{name} detail'

            switcher = {


                'GET': f'all {name} details',
                'POST': f'{name} created',
                'PUT': f'{name} updated',
                'DELETE': f'{name} deleted',
                'PATCH': f'{name} partially updated',

            }

            return switcher[method]


""" 
    Pagination Response Method 

"""


def get_paginated_response(self, data):
    return (OrderedDict([
        ('count', self.count),
        ('next', self.get_next_link()),
        ('previous', self.get_previous_link()),
        ('results', data)
    ]))


""" 
    Genrate Response
"""


def get_response(data, response_obj, message):
    try:
        if data:
            error_msg = ["non_field_errors", "detail"]
            for error_message in error_msg:
                if error_message in data:

                    response = json.dumps(
                        {
                            'isSuccess': False,
                            'statusCode': response_obj.status_code,
                            'error': data[error_message],
                            'message': '',
                        }
                    )
                    return response
        response = json.dumps(
            {
                'isSuccess': True,
                'statusCode': 200 if response_obj.status_code == 204 else response_obj.status_code,
                'message': message,
                'data': data,
            }
        )
        return response
    except Exception as ex:
        logger.info(ex)
        logger.debug(ex)
        raise Exception(ex)

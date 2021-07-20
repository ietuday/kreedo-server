from datetime import datetime
from django.core.exceptions import ValidationError
from schools.models import Subject
import random



""" Calculate Working Days """
def calculate_working_days(start_date, end_date):
    try:
        working_days = end_date - start_date
        return working_days.days
    except Exception as ex:
        raise ValidationError(ex)

""" Calculate Blocks """
def calculate_blocks(working_days):
    try:
        return round(working_days/20)
    except Exception as ex:
        raise ValidationError(ex)



def random_activity(academic_session):
   acad_subjects = academic_session.Subject.all()
   for id, value in enumerate(acad_subjects, start=1):
       print("Value",value)
       subject_qs = Subject.objects.filter(name=value)
       for sub_id, sub in enumerate(subject_qs, start=1):
           print(sub.activity.all())
           return random.choice(sub.activity.all()).id
from activity.models import*

""" ChildJsonData"""
def ChildJsonData(Child_data,period_detail):

    childs = []
    for child in Child_data:
        if ActivityComplete.objects.filter(child=child['child']['id'],period=period_detail['period'],
            activity=period_detail['activity']).exists():
            activity_qs = ActivityComplete.objects.get(child=child['child'],period=self.context['period_detail']['period'],
                                activity=self.context['period_detail']['activity'])
            child['is_completed'] = activity_qs.is_completed
        else:
            child['is_completed'] = True

        child_dict = {
        "name":child['child']['first_name']+" "+child['child']['last_name'],
        "child_id" :child['child']['id'],
        "present":"FALSE",
        "is_completed": child['is_completed']
        }
        childs.append(child_dict)
    return childs

    
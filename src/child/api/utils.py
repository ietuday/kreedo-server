from datetime import datetime
from plan.models import ChildSubjectPlan, Plan
from holiday.models import SchoolHoliday, SchoolWeakOff
from django.core.exceptions import ValidationError
from schools.models import Subject
import random
import pdb


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
            activity_qs = ActivityComplete.objects.filter(child=child['child']['id'],period=period_detail['period'],
                                activity=period_detail['activity'])
            child['is_completed'] = activity_qs[0].is_completed
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

    
def get_range_of_days_in_session(start_date,academic_session):
    total_working_days = calculate_no_of_working_days_for_child(academic_session,start_date)
    return total_working_days




def calculate_no_of_working_days_for_child(academic_session,start_date):

    total_week_offs = SchoolWeakOff.objects.filter(
                                            academic_session=academic_session
                                            ).count()

    total_school_holidays = SchoolHoliday.objects.filter(
                                            academic_session=academic_session
                                            ).count()

    date_diff = academic_session.session_till - start_date
    total_days = date_diff.days

    total_working_days = total_days - (total_week_offs + total_school_holidays)

    return total_working_days



def get_subject_plan(subject_list,child,range_of_working_days):
    for subject in subject_list:
        subject = Subject.objects.get(pk=subject)
        plan_list = []
        if subject.type == 'Group':
            plan_record = Plan.objects.filter(
                                        subject=subject
                                    )
            
            if plan_record:
                plan = plan_record[0]
            else:
                plan = None
               
            child_sub_plan = ChildSubjectPlan.objects.create(
                                                            child=child,
                                                            subject=subject,
                                                            plan=plan
                                                            )
                
        else:
            plan_record = Plan.objects.filter(
                                        subject=subject,
                                        range_from__lte=range_of_working_days,
                                        range_to__gte=range_of_working_days
                                      )
            if plan_record:
                plan = plan_record[0]
            else:
                plan = None
        
            child_sub_plan = ChildSubjectPlan.objects.create(
                                                            child=child,
                                                            subject=subject,
                                                            plan=plan
            
                                                      )

        plan_list.append(child_sub_plan.id)
    return plan_list
            
        
# def update_subject_plan()
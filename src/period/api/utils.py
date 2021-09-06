from math import fabs
from plan.models import Plan, SubjectSchoolGradePlan
import traceback
from django.db.models import Count
from django.core.serializers import serialize
from django.db.models import Q
from django.core.exceptions import ValidationError

import json
import pdb
from datetime import datetime, timedelta, date, time
import calendar
import logging

from holiday.models import*
from kreedo.conf.logger import*
from .serializer import*
from ..models import *
# from holiday.api.serializer import *

""" Create Log for Utils"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)

logger.info("UTILS Period CAlled ")



class PeriodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'

    def create(self, validated_data):
        try:
            p_qs = Period.objects.filter(start_date=validated_data['start_date'], end_date=validated_data['end_date'],
                                     start_time=validated_data['start_time'], end_time=validated_data['end_time']).count()
            if p_qs == 0:
                print("###################",validated_data)
                data = super(PeriodCreateSerializer, self).create(validated_data)
                return data
            else:
                print("ALready Created")
                return ValidationError("Alreday Created")


        except Exception as ex:
            print("ERROR", ex)
            print("@@@@@", traceback.print_exc())
            raise ValidationError(ex)


""" Get All List """


def school_holiday(grade_dict):

    try:
        if SchoolHoliday.objects.filter(holiday_from__gte=grade_dict['start_date'], holiday_till__lte=grade_dict['end_date'], academic_session=grade_dict['acad_session'], ).exists():
            school_holiday_count = SchoolHoliday.objects.filter(
                holiday_from__gte=grade_dict['start_date'], holiday_till__lte=grade_dict['end_date'], academic_session=grade_dict['acad_session']).count()

            return school_holiday_count

        else:
            print("Holiday List Not Exist")
            return 0

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)


def weekday_count(grade, week_off):
    try:
        start_date = datetime.strptime(grade['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(grade['end_date'], '%Y-%m-%d')
        week = {}
        for i in range((end_date - start_date).days):
            day = calendar.day_name[(
                start_date + timedelta(days=i+1)).weekday()]
            week[day] = week[day] + 1 if day in week else 1
        return calculate_total_week_off_days(week, week_off)

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)


def calculate_total_week_off_days(week, week_off):
    total_weekoff_days = 0

    for wee in week_off:
        if wee['monday'] == True:
            total_weekoff_days = total_weekoff_days + week['Monday']

        if wee['tuesday'] == True:
            total_weekoff_days = total_weekoff_days + week['Tuesday']

        if wee['wednesday'] == True:
            total_weekoff_days = total_weekoff_days + week['Wednesday']

        if wee['thursday'] == True:
            total_weekoff_days = total_weekoff_days + week['Thursday']

        if wee['friday'] == True:
            total_weekoff_days = total_weekoff_days + week['Friday']

        if wee['saturday'] == True:
            total_weekoff_days = total_weekoff_days + week['Saturday']

        if wee['sunday'] == True:
            total_weekoff_days = total_weekoff_days + week['Sunday']

    return total_weekoff_days


""" Get Weak-off List """

def weakoff_list(grade_dict):
    try:
        if SchoolWeakOff.objects.filter(academic_session=grade_dict['acad_session']).exists():
            week_off_list = SchoolWeakOff.objects.filter(
                academic_session=grade_dict['acad_session'])

            qs_json = json.loads(serialize('json', week_off_list))
            response_data = []
            for qs in qs_json:
                response_data.append(qs['fields'])
            print("response_data--->2", response_data)
            return response_data
        else:
            print("Weak-Off List Not Exist")
            return []

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ex


def total_working_days(grade_dict, count_weekday):
    try:
        from_date = datetime.strptime(grade_dict['start_date'], '%Y-%m-%d')
        to_date = datetime.strptime(grade_dict['end_date'], '%Y-%m-%d')
        result = to_date - from_date
        resultant_data = (result.days + 1) - count_weekday
        return resultant_data

    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError(ex)


def create_period(grade, section, start_date, end_date, acad_session):
    try: 
        grade_dict = {
                "grade": grade,
                "section": section,
                "start_date": start_date,
                "end_date": end_date,
                "acad_session": acad_session
        }
        print(grade, section, start_date, end_date, acad_session)
        from_date = datetime.strptime(start_date, '%Y-%m-%d')
        to_date = datetime.strptime(end_date, '%Y-%m-%d')
        delta = to_date - from_date  # as timedelta
        for i in range(delta.days + 1):
            day = from_date + timedelta(days=i)
            day_according_to_date = check_date_day(str(day.date()))
            week_off = weakoff_list(grade_dict)[0]
            day_according_to_date = day_according_to_date.lower()
            for key, value in week_off.items():
                if key == day_according_to_date and value == False:
                    schoolHoliday_count = SchoolHoliday.objects.filter(Q(holiday_from=day.date()) | Q(
                        holiday_from=day.date()), academic_session=acad_session).count()
                    
                    if schoolHoliday_count == 0:
                        period_list = PeriodTemplateDetail.objects.filter(
                             day=day_according_to_date.upper())
                        print("@@@@@@@@@@@@",period_list)
                        period_dict = {}
 
                        for period in period_list:
                            period_dict['period_template_detail']=period.id
                            period_dict['academic_session'] = [acad_session]
                            period_dict['name'] = period.name
                            # period_dict['description'] =  period.subject.name
                            period_dict['subject'] = period.subject.id
                            period_dict['room'] = period.room.id
                            period_date = day.date()
                            period_time = period.start_time
                            period_dict['start_date'] = period_date
                            period_dict['end_date'] = period_date
                            period_dict['start_time'] = period.start_time
                            period_dict['end_time'] = period.end_time
                            period_dict['type'] = period.type
                            period_dict['is_active'] = True

                            p_qs = Period.objects.filter(start_date=period_dict['start_date'], end_date=period_dict[
                                                         'end_date'], start_time=period_dict['start_time'], end_time=period_dict['end_time']).count()
                            if p_qs == 0:
                                print("#####",p_qs)
                                period_serializer = PeriodCreateSerializer(
                                    data=period_dict)
                                if period_serializer.is_valid():
                                    period_serializer.save()

                                else:
                                    print("PERIOD-Serializer",period_serializer.errors)
                                    raise ValidationError(
                                        period_serializer.errors)
                            else:
                                print("error in period")
                        period_qs = PeriodTemplateToGrade.objects.filter(academic_session=acad_session,
                                        start_date=start_date, end_date=end_date).update(is_applied='True')
                        
                        print("#PERIOD-----------#", period_qs)
                       
                        
        data = "Period Created"
        return data
    except Exception as ex:
        print(traceback.print_exc())
        logger.debug(ex)
        logger.info(ex)

        raise ValidationError(ex)


def check_date_day(date):
    day_name = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = datetime.strptime(date, '%Y-%m-%d').weekday()
    return day_name[day]


def get_seconds_removed(time):
    if time:
        time_list = time.split(":")
        time = ":".join(time_list[:2])
        return time
    else:
        return time


"""Period Activity Association"""
def period_group_activity_association(academic_session):

    # subject_plan_based_on_grades = SubjectSchoolGradePlan.objects.filter(
    #                                                         school=academic_session.school,
    #                                                         grade=academic_session.grade
    #                                                                     )

    # """ For now considering all the periods have group plan"""
    # for subject_plan in subject_plan_based_on_grades:
    #     period_list = Period.objects.filter(
    #                                         academic_session=academic_session,
    #                                         subject=subject_plan.subject,
    #                                         # subject__type='Group'

    #                                         )
    #     period_count = period_list.count()
    #     release_activity_list = []
    #     optional_activity_release_list = []
    #     for period in period_list:
    #         print("activity_list",release_activity_list)
    #         print("opti_list",optional_activity_release_list)
    #         # if period.subject.type == 'Individual':
    #         #     """ Individual Plan Implementation Logic"""
    #         #     pass
    #         if period.subject.type == 'Group':
    #             """ Group Plan Imlementation Logic """
    #             mandatory_activities = subject_plan.plan.plan_activity.filter(
    #                                                                         is_optional=False,
    #                                                                         ).exclude(
    #                                                                         id__in=release_activity_list
    #                                                                         ).order_by('sort_no')
    #             optional_activities = subject_plan.plan.plan_activity.filter(
    #                                                                         is_optional=True,
    #                                                                         ).exclude(
    #                                                                         id__in=optional_activity_release_list
    #                                                                         ).order_by('sort_no')

    #             mandatory_activity_count = subject_plan.plan.plan_activity.filter(
    #                                                                         is_optional=False
    #                                                                         ).count()
    #             print("mand_act",mandatory_activities)
    #             # pdb.set_trace()
    #             if mandatory_activity_count <= period_count:
    #                 if mandatory_activity_count < period_count:
    #                     """ When period count is greater than mandatory activity count """
    #                     if mandatory_activities:
    #                         mandatory_activities = list(mandatory_activities)
    #                         activity = mandatory_activities[0].activity
    #                         period.activity_to_be_release.add(activity)
    #                         period.save()
    #                         release_activity_list.append(mandatory_activities[0].id)
    #                         # pdb.set_trace()
    #                         mandatory_activities.pop(0)
    #                     else:
    #                         optional_activities = list(optional_activities)
    #                         activity = optional_activities[0].activity
    #                         period.activity_to_be_release.add(activity)
    #                         period.save()
    #                         optional_activity_release_list.append(optional_activities[0].id)
    #                         # pdb.set_trace()
    #                         optional_activity_release_list.pop(0)


    #                 else:
    #                     """ One mandatory activity per period """
    #                     mandatory_activities = list(mandatory_activities)
    #                     activity = mandatory_activities[0].activity
    #                     period.activity_to_be_release.add(activity)
    #                     period.save()
    #                     release_activity_list.append(mandatory_activities[0].id)
    #                     # pdb.set_trace()
    #                     mandatory_activities.pop(0)
    #             else:

    #                 message = "Period count is less than mandatory activity count"    
    #                 print(message)
                
    #         else:
    #             """Individual Plan Activity release logic"""
    #             pass

    

    period_list_based_on_session = Period.objects.filter(
                                                        academic_session=academic_session,
                                                        subject__type='Group'
                                                        )
    subject_list_based_on_period = []

    """ subject list """
    for period in period_list_based_on_session:
        if period.subject in subject_list_based_on_period:
            continue
        else:
            subject_list_based_on_period.append(period.subject)

    print("subject list",subject_list_based_on_period)

    for subject in subject_list_based_on_period:
        subject_based_plan = get_subject_based_plan(subject,academic_session.grade)
        # pdb.set_trace()
    period_based_on_subject = period_list_based_on_session.filter(subject=subject)

    # pdb.set_trace()
    for period in period_based_on_subject:
        # period.activity_to_be_done = []
        # period.save()

        plan_mandatory_activities = subject_based_plan.plan_activity.filter(
                                                                is_optional=False
                                                                ).order_by('sort_no')
        plan_optional_activities  = subject_based_plan.plan_activity.filter(
                                                                is_optional=True
                                                                ).order_by('sort_no')
        
        for plan_activity in plan_mandatory_activities:
            # pdb.set_trace()
            record_aval = period_based_on_subject.filter(
                                                activity_to_be_release=plan_activity.activity
                                                        )
            if record_aval:
                continue
            else:
                print("period",period)
                print("activity",plan_activity.activity)
                period.activity_to_be_release.add(plan_activity.activity)
                period.save()
                break
        
        # for plan_activity in plan_optional_activities:
        #     # pdb.set_trace()
        #     record_aval = period_based_on_subject.filter(
        #                                         activity_to_be_release=plan_activity.activity
        #                                                 )
        #     if record_aval:
        #         continue
        #     else:
        #         print("period",period)
        #         print("activity",plan_activity.activity)
        #         period.activity_to_be_release.add(plan_activity.activity)
        #         period.save()
        #         break
        






def get_subject_based_plan(subject,grade):

    plan = Plan.objects.filter(subject=subject,
                                grade=grade
                            )
    # pdb.set_trace()
    if plan:
        return plan[0]
    return "No Plan Found"                       













# period_count = period_based_on_subject.count()

#         mandatory_activities = period_based_on_subject.plan_activity.filter(
#                                                                         is_optional=False,
#                                                                         ).exclude(
#                                                                         id__in=release_activity_list
#                                                                         ).order_by('sort_no')
#         optional_activities = period_based_on_subject.plan_activity.filter(
#                                                                     is_optional=True,
#                                                                     ).exclude(
#                                                                     id__in=optional_activity_release_list
#                                                                     ).order_by('sort_no')

#         mandatory_activity_count = period_based_on_subject.plan_activity.filter(
#                                                                     is_optional=False
#                                                                     ).count()
#         print("mand_act",mandatory_activities)
#         # pdb.set_trace()
#         if mandatory_activity_count <= period_count:
#             if mandatory_activity_count < period_count:
#                 """ When period count is greater than mandatory activity count """
#                 if mandatory_activities:
#                     mandatory_activities = list(mandatory_activities)
#                     activity = mandatory_activities[0].activity
#                     period.activity_to_be_release.add(activity)
#                     period.save()
#                     release_activity_list.append(mandatory_activities[0].id)
#                     # pdb.set_trace()
#                     mandatory_activities.pop(0)
#                 else:
#                     optional_activities = list(optional_activities)
#                     activity = optional_activities[0].activity
#                     period.activity_to_be_release.add(activity)
#                     period.save()
#                     optional_activity_release_list.append(optional_activities[0].id)
#                     # pdb.set_trace()
#                     optional_activity_release_list.pop(0)



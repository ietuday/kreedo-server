from child.models import Block
from math import fabs
from schools.models import *
import traceback

from django.db.models.query_utils import PathInfo
from plan.models import Plan, SubjectSchoolGradePlan
import traceback
from django.db.models import Count
from django.core.serializers import serialize
from django.db.models import Q
from django.core.exceptions import ValidationError
from activity.models import *

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
                print("###################", validated_data)
                data = super(PeriodCreateSerializer,
                             self).create(validated_data)
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


def create_period(grade, section, start_date, end_date, acad_session, period_template):
    try:
        grade_dict = {
            "grade": grade,
            "section": section,
            "start_date": start_date,
            "end_date": end_date,
            "acad_session": acad_session,
            "period_template": period_template
        }
        print(grade, section, start_date, end_date, acad_session)
        from_date = datetime.strptime(start_date, '%Y-%m-%d')
        to_date = datetime.strptime(end_date, '%Y-%m-%d')
        delta = to_date - from_date  # as timedelta
        print("grade", grade_dict)
        period_qs = PeriodTemplateToGrade.objects.filter(academic_session=acad_session,
                                                         start_date=start_date, end_date=end_date, period_template=period_template)

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", period_qs)
        if period_qs:
            period_qs[0].period_status = "PENDING"
            period_qs[0].save()

        for i in range(delta.days + 1):
            day = from_date + timedelta(days=i)
            day_according_to_date = check_date_day(str(day.date()))
            week_off = weakoff_list(grade_dict)[0]
            day_according_to_date = day_according_to_date.lower()
            print(week_off)
            for key, value in week_off.items():
                if key == day_according_to_date and value == False:
                    schoolHoliday_count = SchoolHoliday.objects.filter(Q(holiday_from=day.date()) | Q(
                        holiday_from=day.date()), academic_session=acad_session).count()

                    if schoolHoliday_count == 0:
                        period_list = PeriodTemplateDetail.objects.filter(
                            day=day_according_to_date.upper(), period_template=period_template)

                        period_dict = {}

                        for period in period_list:
                            print("period.subject.id----", period.subject.id)
                            print("acad_session-----", acad_session)
                            print("SectionSubjectTeacher---",
                                  SectionSubjectTeacher.objects.all())
                            teacher_id = SectionSubjectTeacher.objects.filter(
                                subject=period.subject.id, academic_session=acad_session)[0]
                            print("teacher_id---", teacher_id.teacher)
                            print(period)
                            # pdb.set_trace()
                            period_dict['period_template_detail'] = period.id
                            period_dict['academic_session'] = [acad_session]
                            period_dict['name'] = period.name
                            # period_dict['description'] =  period.subject.name
                            period_dict['subject'] = period.subject.id
                            period_dict['teacher'] = [teacher_id.teacher]
                            period_dict['room'] = period.room.id
                            period_date = day.date()
                            period_time = period.start_time
                            period_dict['start_date'] = period_date
                            period_dict['end_date'] = period_date
                            period_dict['start_time'] = period.start_time
                            period_dict['end_time'] = period.end_time
                            period_dict['type'] = period.type
                            period_dict['is_active'] = True

                            print("period_dict-----------", period_dict)
                            p_qs = Period.objects.filter(start_date=period_dict['start_date'], end_date=period_dict[
                                                         'end_date'], start_time=period_dict['start_time'], end_time=period_dict['end_time'], period_template_detail=period.id, room=period.room.id).count()
                            if p_qs == 0:
                                period_serializer = PeriodCreateSerializer(
                                    data=period_dict)
                                if period_serializer.is_valid():
                                    period_serializer.save()

                                else:
                                    print("PERIOD-Serializer",
                                          period_serializer.errors)
                                    raise ValidationError(
                                        period_serializer.errors)
                            else:
                                print("Period Already Created")
        period_to_grade_qs = PeriodTemplateToGrade.objects.filter(academic_session=acad_session,
                                                                  start_date=start_date, end_date=end_date, period_template=period_template)
        if period_to_grade_qs:
            period_to_grade_qs[0].is_applied = True
            period_to_grade_qs[0].period_status = "COMPLETE"
            period_to_grade_qs[0].save()

        return "Period Creating....."
    except Exception as ex:
        print("%%%%%%%55", ex)
        print("@@@@@@@", traceback.print_exc())
        period_qs = PeriodTemplateToGrade.objects.filter(academic_session=acad_session,
                                                         start_date=start_date, end_date=end_date, period_template=period_template)
        if period_qs:
            period_qs[0].period_status = "FAILED"
            period_qs[0].save()

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


# """Period Activity Association"""
# def period_group_activity_association(academic_session):

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



"""Period  Group Activity Association"""
def period_group_activity_association(academic_session):   
    try:
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
        
        period_based_on_subject = period_list_based_on_session.filter(subject=subject)

        plan_mandatory_activities = subject_based_plan.plan_activity.filter(
                                                                    is_optional=False
                                                                    ).order_by('sort_no')
        plan_optional_activities  = subject_based_plan.plan_activity.filter(
                                                                    is_optional=True
                                                                    ).order_by('sort_no')

        activity_release_rec = []
        # pdb.set_trace()
        for period in period_based_on_subject:
            # period.activity_to_be_release.clear()
            # period.save()

            # continue
            mandatory_activities = plan_mandatory_activities.exclude(
                                                                    id__in=activity_release_rec
                                                                        )
            print("mand act",mandatory_activities)
            if mandatory_activities:
                """ Mandatory activity release logic """
                for plan_activity in mandatory_activities:
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
                        activity_release_rec.append(plan_activity.id)
                        break
            else:
                """ Optional Activity Release logic """
                for plan_activity in plan_optional_activities:
                
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
                        activity_release_rec.append(plan_activity.id)
                        break
            

    except Exception as ex:
        print("ex",ex)
        print("traceback",traceback.print_exc())


    


def get_subject_based_plan(subject,grade):

    plan = Plan.objects.filter(subject=subject,
                                grade=grade
                            )
    if plan:
        return plan[0]
    raise Exception("No Plan Found")                       



""" Period Individual Sequantial Activity Release"""

def period_individual_seq_activity_association(academic_session): 
    try:
        child_plans = ChildPlan.objects.filter(academic_session=academic_session)
    
        for child_plan in child_plans:

            period_list_based_on_child = Period.objects.filter(
                                                            start_date__gte=child_plan.curriculum_start_date,
                                                            academic_session=academic_session,
                                                            subject__type='Individual',
                                                            )
            
            subject_plan_qs = child_plan.subject_plan.all()
            subject_list_based_on_period = []
    
            """ subject list """
            for period in period_list_based_on_child:
                if period.subject in subject_list_based_on_period:
                    continue
                else:
                    subject_list_based_on_period.append(period.subject)
            
            print('subject_list',subject_list_based_on_period)
            for subject in subject_list_based_on_period:
                    
            
                    subject_based_plan = subject_plan_qs.filter(
                                                            subject=subject,
                                                            child=child_plan.child
                                                            )
                    if subject_based_plan:
                        subject_based_plan = subject_based_plan[0]
                        print('subjct_plan',subject_based_plan)
                    else:
                        continue

                    period_based_on_subject = period_list_based_on_child.filter(subject=subject)
                    if subject_based_plan.plan.sub_type == 'Sequential':
                        plan_mandatory_activities = subject_based_plan.plan.plan_activity.filter(
                                                                        is_optional=False
                                                                        ).order_by('sort_no')

                        plan_optional_activities  = subject_based_plan.plan.plan_activity.filter(
                                                                                is_optional=True
                                                                                ).order_by('sort_no')

                        print("subject",subject)
                        # pdb.set_trace()
                        activity_release_rec = []
                        for period in period_based_on_subject:
                            print("period",period)
                            mandatory_activities = plan_mandatory_activities.exclude(
                                                                                id__in=activity_release_rec
                                                                                    )

                            # pdb.set_trace()
                            if mandatory_activities:
                                for plan_activity in mandatory_activities:
                                    print("inside",period)
                                    record_aval = PeriodIndividualActivity.objects.filter(
                                                                        child=child_plan.child,
                                                                        activity=plan_activity.activity,
                                                                        # period=period
                                                                            )
                                    
                                    if record_aval:
                                        continue
                                    else:
                                        print("period",period)
                                        print("activity",plan_activity.activity)
                                        child_indiv_activity = PeriodIndividualActivity.objects.create(
                                                                                                child=child_plan.child,
                                                                                                period=period, 
                                                                                                )
                                        

                                        child_indiv_activity.activity.add(plan_activity.activity)
                                        child_indiv_activity.save()
                                        print("activity added to period")
                                        period.individual_activities.add(child_indiv_activity)
                                        period.save()
                                        activity_release_rec.append(plan_activity.id)
                                        break
                                        
                            else:
                                    for plan_activity in plan_optional_activities:
                                    
                                        record_aval = PeriodIndividualActivity.objects.filter(
                                                                            child=child_plan.child,
                                                                            activity=plan_activity.activity,
                                                                            # period=period
                                                                                )
                                        
                                        if record_aval:
                                            continue
                                        else:
                                            print("period",period)
                                            print("activity",plan_activity.activity)
                                            child_indiv_activity = PeriodIndividualActivity.objects.create(
                                                                                                    child=child_plan.child,
                                                                                                    period=period, 
                                                                                                    )
                                            

                                            child_indiv_activity.activity.add(plan_activity.activity)
                                            child_indiv_activity.save()
                                            print("activity added to period")
                                            period.individual_activities.add(child_indiv_activity)
                                            period.save()
                                            activity_release_rec.append(plan_activity.id)
                                            break
                    else:
                        print("randamized")
                        plan_activities = subject_based_plan.plan.plan_activity.filter(
                                                                        is_optional=False
                                                                        ).order_by('sort_no')
                        no_of_blocks = get_no_of_blocks(period_based_on_subject)
                        activity_per_block = get_activity_per_block(no_of_blocks,plan_activities)
                        print("blocks",no_of_blocks)
                        print("act/block",activity_per_block)
                        no_of_blocks = 4
                        period_per_block = 2
                        pstart = 0
                        pend = period_per_block
                        astart = 0
                        aend = activity_per_block
                        for count in range(1,no_of_blocks+1):
                            print('s,e',pstart,pend)
                            if count == no_of_blocks:
                                print("@@")
                                period_for_block = period_based_on_subject[pstart:]
                                activity_for_block = plan_activities[astart:]
                                print(f"period for block {count}",period_for_block)
                                print(f"activity for block {count}",activity_for_block)
                                activities = [plan_act.activity for plan_act in activity_for_block]
                                print("activit",activities)
                            else:
                                period_for_block = period_based_on_subject[pstart:pend]
                                activity_for_block = plan_activities[astart:aend]
                                pstart += period_per_block
                                pend = pstart + period_per_block
                                astart += activity_per_block
                                aend = astart + activity_per_block
                                print(f"period for block {count}",period_for_block)
                                print(f"activity for block {count}",activity_for_block)
                                activities = [plan_act.activity for plan_act in activity_for_block ]
                                print("activit",activities)
                            """ Create Block"""
                            block = Block.objects.create(
                                                        block_no=count,
                                                        child_plan=child_plan,
                                                        is_active=True
                                                        )
                            block.period.set(period_for_block)
                            block.activity.set(activities)
                            block.save()
                            print(f"block {count} created")

                                

    except Exception as ex:
                print("ex",ex)
                print("traceback",traceback.print_exc())

                                




""" def to find no. of blocks"""
def get_no_of_blocks(period_based_on_subject):
    no_of_periods = 121
    no_of_blocks = no_of_periods // 20
    # pdb.set_trace()
    if no_of_periods % 20 == 0:
        return no_of_blocks
    else:
        no_of_blocks = no_of_periods // 20
        return no_of_blocks+1



""" def to find no. of activities per block """
def get_activity_per_block(no_of_blocks,plan_activities):
    activity_count = plan_activities.count()
    print("activity count",activity_count)
    activity_per_block = activity_count // no_of_blocks
    return activity_per_block






def validation_time_for_period_template_detail():
    try:
        print("@@@@@@@@")
    except Exception as ex:
        raise ValidationError(ex)

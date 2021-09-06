
from period.models import Period
from period.api.utils import get_subject_based_plan
from activity.models import Activity, ActivityComplete


def check_mandatory_act_done(activity_data):
    activity  = Activity.objects.filter(pk=activity_data['activity'])
    period = Period.objects.get(pk=activity_data['period'])
    if activity.type == 'Group':
        plan = get_subject_based_plan(period.subject,period.grade)

        get_plan_activity = plan.plan_activity.filter(activity=activity)
        if get_plan_activity:
            dependent_activity = get_plan_activity[0].dependent_on
            if dependent_activity:
                activity_complete_record = ActivityComplete.objects.filter(
                                                            child=activity_data['child'],
                                                            activity=dependent_activity.id,
                                                            is_completed=True
                                                                            )
                if activity_complete_record:
                    return True
                else:
                    return False


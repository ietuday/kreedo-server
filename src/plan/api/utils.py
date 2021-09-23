from plan.models import *
from schools.models import Subject
import pdb


def update_subject_plan(subject_list,child,range_of_working_days):

    subjects = subject_list['subjects']
    plan_list = []
    for sub in subjects:
        print('sub',sub)
        record_aval = ChildSubjectPlan.objects.filter(
                                                        subject=sub,
                                                        child=child
                                                    )
       
        if record_aval:
            subject_plan_obj = record_aval[0]
            plan = get_plan(sub,range_of_working_days)
            subject_plan_obj.plan = plan
            subject_plan_obj.save()
            plan_list.append(subject_plan_obj)       
            
        else:
            
            plan = get_plan(sub,range_of_working_days)
            subject = Subject.objects.get(pk=sub['subject'])
            
            subject_plan_obj = ChildSubjectPlan.objects.create(
                                child=child,
                                plan=plan[0],
                                subject = subject
                                                    )
            plan_list.append(subject_plan_obj)
        
    deletedSubjects = subject_list['deletedSubjects']
    for subject_id in deletedSubjects:
        subject_plan_obj = ChildSubjectPlan.objects.filter(
                            child=child,
                            subject=subject_id
        )
        subject_plan_obj.delete()
        print("object deleted")
    return plan_list

            



def get_plan(subject_id,range_of_working_days):
    subject = Subject.objects.get(pk=subject_id)
    print("range",range_of_working_days)
    if subject.type == 'Group':
        plan_record = Plan.objects.filter(
                                    subject=subject
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
    return plan
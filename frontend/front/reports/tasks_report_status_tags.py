from django.template import Library

register = Library()


@register.assignment_tag()
def get_tasks_report_total_status(tasks_report):
    """

    :type tasks_report: dict
    :rtype: dict
    """
    total_status = {}
    for obj in tasks_report:
        if obj.status not in total_status.keys():
            total_status[obj.status] = 1
        else:
            total_status[obj.status] += 1

    total_status['SUCCESSFUL'] = 10
    total_status['FAILED'] = 4

    return total_status
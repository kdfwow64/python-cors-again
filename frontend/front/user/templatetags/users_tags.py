from django.template import Library

register = Library()


@register.assignment_tag()
def group_permission(perm_list):
    """

    :type perm_list: list
    :rtype: list
    """
    grouped_dict = {}

    for perm in perm_list:
        if perm['object'] not in grouped_dict.keys():
            grouped_dict[perm['object']] = []
        grouped_dict[perm['object']].append(perm)
    return grouped_dict
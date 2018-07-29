from django.template import Library

register = Library()


@register.assignment_tag()
def get_tasks_report_total_status(tasks_report):
    """

    :type tasks_report: dict
    :rtype: dict
    """
    total_status = {'failed': 0, 'new': 0, 'ongoing': 0, 'queued': 0, 'successful': 0}
    for obj in tasks_report:
        status = obj['status'].lower()
        if status not in total_status.keys():
            total_status[status] = 1
        else:
            total_status[status] += 1

    return total_status


def show_diff(seqm):
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append("<font color='green'>" + seqm.b[b0:b1] + "</font>")
        elif opcode == 'delete':
            output.append("<font color='red'>" + seqm.a[a0:a1] + "</font>")
        elif opcode == 'replace':
            output.append("<font color='red'>" + seqm.a[a0:a1] + "</font><font color='green'>" + seqm.b[b0:b1] + "</font>")
        else:
            output.append("<font>" + seqm.a[a0:a1] + "</font>")
    return ''.join(output)


@register.filter()
def get_diff_display(from_value, to_value):
    """

    :type from_value: str
    :type to_value: str
    :rtype: str
    """
    import difflib

    sm = difflib.SequenceMatcher(None, from_value, to_value)
    return show_diff(sm)


@register.assignment_tag()
def get_item(dictionary, key):
    """

    :type dictionary: dict
    :type key: str
    :rtype:
    """
    if isinstance(dictionary, dict) and key in dictionary.keys():
        return dictionary.get(key)
    return ''


@register.filter()
def display_diff(diff_str):
    """

    :type diff_str: str
    :rtype: str
    """
    output = []
    for line in diff_str.splitlines():
        if line.strip() != '':
            if line.startswith('+'):
                output.append("<font class='diff-add'>" + line.replace('+', '').strip() + "</font>")
            elif line.startswith('-'):
                output.append("<font class='diff-del'>" + line.replace('-', '').strip() + "</font>")
            else:
                output.append("<font>" + line + "</font>")
    return '<br>'.join(output)


@register.filter()
def split_lines(the_str):
    """

    :type the_str: str
    :rtype: str
    """
    return '<br>'.join(the_str.splitlines())


@register.filter()
def display_result(result, job):
    """

    :type result: dict
    :type job: dict
    :rtype: bool
    """
    config = {}
    if 'configuration' in result['result'].keys():
        config = result['result']['configuration']
    if 'configurations' in result['result'].keys():
        config = result['result']['configurations']

    if len(config) > 0:
        if job['agent_type'] == 'configuration_differ_postcheck':
            if 'diff' in config.keys() and config['diff'] != '':
                return True
        else:
            return True
    return False
from django import template


register = template.Library()


@register.filter
def tagvalues(incident, key) -> list:
    """Return values of tags with key KEY for incident INCIDENT

    There can be multiple tags with the same key
    """
    tags = incident.deprecated_tags
    return [str(tag.value) for tag in tags if tag.key == key]


@register.filter
def is_acked_by(incident, context=None) -> bool:
    """
    If ack_group is None, return True if incident is acked by any group
    If ack_group is not None, return True if incident is acked by given ack_group
    """

    if not context:
        is_acked = incident.acked
    else:
        if context.ack is None:
            is_acked = incident.acked
        else:
            is_acked = context.ack in incident.acks.active().group_names()

    return is_acked

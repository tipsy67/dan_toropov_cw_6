from django import template
register = template.Library()


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


@register.filter
def verbose_names(obj):
    def check_field(field):
        if field.many_to_one or field.many_to_many or field.one_to_one or field.one_to_many:
            return False
        return True
    fields = obj._meta.get_fields(include_parents=False, include_hidden=False)

    return (x.verbose_name for x in fields if check_field(x))

@register.filter
def is_list_not_empty(obj_list):
    if obj_list is None or len(obj_list) == 0:
        return False
    return True
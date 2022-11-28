from django import template
from django.contrib.admin.templatetags import admin_list

register = template.Library()


@register.inclusion_tag('admin/custom_pagination.html', takes_context=True)
def custom_pagination(context, cl):
    pagination = admin_list.pagination(cl)

    # TODO: Hacky way. Find a better way to do it.
    for cn in context:
        if "query_params" in cn:
            pagination['query_params'] = cn["query_params"]
            break

    return pagination

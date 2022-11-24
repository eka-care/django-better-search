from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .utils import format_data


class SeparateSearchAdmin(admin.ModelAdmin):
    change_list_template = "admin/custom_change_list.html"
    advanced_search_fields = {}
    search_form_data = None

    def changelist_view(self, request, extra_context=None):
        """"""
        if hasattr(self, "search_form"):
            self.advanced_search_fields = {}
            self.extract_advanced_search_terms(request)
            self.search_form_data = self.search_form(initial=self.get_request_query_values(request))
            extra_context = {
                "separate_search_fields": self.search_form_data,
                "query_params": self.get_request_query_values(request),
            }

        return super().changelist_view(request, extra_context=extra_context)

    def extract_advanced_search_terms(self, request):
        """
        allow to extract field values from request
        """
        request.GET._mutable = True  # pylint: disable=protected-access

        request_form_data = self.search_form(request.GET)
        if request_form_data is not None:
            for key in request_form_data.fields.keys():
                temp = request.GET.pop(key, None)
                if temp and (type(temp) == list and temp[0]):  # there is a field but it's empty so it's useless
                    self.advanced_search_fields[key] = temp

        request.GET._mutable = False  # pylint: disable=protected-access

    def get_queryset(self, request):
        """
        override django admin 'get_queryset'
        """
        queryset = super().get_queryset(request)

        return queryset.filter(self.advanced_search_query(request))

    def advanced_search_query(self, request):
        """
        Get form and mount filter query if form is not none
        """
        query = Q()

        if self.search_form_data is None:
            return query

        for field, form_field in self.search_form_data.fields.items():
            has_field_value, field_value = self.get_request_field_value(field)
            if has_field_value:
                query &= self.get_field_value(field, form_field, field_value, has_field_value, request)

        return query

    def get_request_field_value(self, field):
        """
        check if field has value passed on request
        """
        if field in self.advanced_search_fields:
            return True, self.advanced_search_fields[field][0]

        return False, None

    def get_field_value_json(self, field, form_field, field_value):
        field_name = form_field.widget.attrs.get("filter_field", field)
        field_filter = field_name + form_field.widget.attrs.get("filter_method", "")

        field_value = format_data(form_field, field_value)

        return {field_filter: field_value}

    def get_field_value_default(self, field, form_field, field_value, has_field_value, request):
        """
        mount default field value
        """
        if has_field_value:
            field_name = form_field.widget.attrs.get("filter_field", field)

            try:
                field_val_json = self.get_field_value_json(field, form_field, field_value)
                return Q(**field_val_json)
            except ValidationError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(f"Filter in field '{field_name}' ignored, because value '{field_value}' isn't valid"),
                )
            except Exception:  # pylint: disable=broad-except
                messages.add_message(
                    request, messages.ERROR, _(f"Filter in field '{field_name}' ignored, error has occurred.")
                )

        return Q()

    def get_field_value(self, field, form_field, field_value, has_field_value, request):
        """
        allow to override default field query
        """
        if hasattr(self, ("search_" + field)):
            return getattr(self, "search_" + field)(
                field, field_value, form_field, request, self.advanced_search_fields
            )

        return self.get_field_value_default(field, form_field, field_value, has_field_value, request)

    def get_request_query_values(self, request):
        resp = {}
        request_form_data = self.search_form(request.GET)

        for field, form_field in request_form_data.fields.items():
            has_field_value, field_value = self.get_request_field_value(field)
            if has_field_value:
                field_value_json = self.get_field_value_json(field, form_field, format_data(form_field, field_value))
                resp = {**resp, **field_value_json}

        return resp

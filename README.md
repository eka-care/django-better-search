# django-better-search
[![Downloads](https://pepy.tech/badge/django-better-search)](https://pepy.tech/project/django-better-search)
[![Downloads](https://pepy.tech/badge/django-better-search/month)](https://pepy.tech/project/django-better-search/month)
[![Downloads](https://pepy.tech/badge/django-better-search/week)](https://pepy.tech/project/django-better-search/week)

[![PyPI version](https://badge.fury.io/py/django-better-search.svg)](https://badge.fury.io/py/django-better-search)

<i>This repo is heavily influenced by [django-admin-search](https://github.com/shinneider/django-admin-search) and copies some of the components as well.</i>

This repo implements search on Django admin page differently. It generates different search boxes for separate fields and doesn't treat all of those fields as string.

## Requirements

This app is tested using following:

* Django >= 3.2
* Python >= 3.9

## Installation

This repo is published [on Pypi](https://pypi.org/project/django-better-search/). You can install it from there using following:

```
pip install django-better-search
```

## Usage

<i>Note:</i> <b>This project is not yet ready for production use</b>.

1) Add `django_separate_search` in your `INSTALLED_APPS`. Example:

```
INSTALLED_APPS = [
    ...
    "django_separate_search",
    ...
]
```

2) Create a search form to have search fields on your admin page. Example:

```
from django.forms import CharField, Form, IntegerField


class UserSearchForm(Form):
    name = CharField(required=False, label="User's Name", help_text="Some help_text")
    age = IntegerField(required=False, label="User's Age", help_text="Another help_text")
    ...
```

3) Use the search form in your AppAdmin in your `admin.py`. Example:

```
from django_separate_search.admin import SeparateSearchAdmin


class UserAdmin(SeparateSearchAdmin):
    ...
    search_form = UserSearchForm
    ...
```

This will render your search-form fields on the list-view admin page.

4) If you want to implement search on a custom field, you will have to implement <b>search_`<field_name>`</b>. Example:

```
class UserAdmin(SeparateSearchAdmin):
    ...

    def search_<field_name>(self, field, field_value, form_field, request, param_values):
        query = Q()
        // Implement your query

        return query
```

## Images

This is how search will look in admin view-list:
    ![modal](https://user-images.githubusercontent.com/58887170/201068717-7abec72f-547e-478d-8f8a-cdc256763ee8.png)

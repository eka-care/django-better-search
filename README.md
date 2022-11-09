# django-better-search
<i>This repo is heavily influenced by [django-admin-search](https://github.com/shinneider/django-admin-search) and copies some of the components as well.</i>

This repo implements search on Django admin page differently. It generates different search boxes for separate fields and doesn't treat all of those fields as string.

## Requirements
This app requires the following:

* Django >= 3.2

## Usage

<i>Note:</i> <b>This project is not yet ready for production use</b>.

1) Create a search form to have search fields on your admin page. Example:

```
from django.forms import CharField, Form, IntegerField


class UserSearchForm(Form):
    name = CharField(required=False, label="User's Name", help_text="Some help_text")
    age = IntegerField(required=False, label="User's Age", help_text="Another help_text")
    ...
```

2) Use the search form in your AppAdmin in your `admin.py`. Example:

```
from django_separate_search.admin import SeparateSearchAdmin


class UserAssessmentAdmin(SeparateSearchAdmin):
    ...
    search_form = UserSearchForm
    ...
```

This will render your search-form fields on the listview admin page.

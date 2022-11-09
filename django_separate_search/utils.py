from django.forms import BooleanField, ChoiceField, ModelChoiceField, TextInput


def format_data(value, key_value):
    """
    Return data converted by form type
    """
    result = None
    if isinstance(value, (ChoiceField, ModelChoiceField)):
        value.clean(key_value)
        result = key_value

    elif isinstance(value, TextInput):
        result = str(key_value)

    elif isinstance(value, BooleanField):
        # in case you have doubts (because I find it very strange)
        # see a ticket https://code.djangoproject.com/ticket/31049
        result = bool(key_value)

    else:
        result = value.clean(key_value)

    return result

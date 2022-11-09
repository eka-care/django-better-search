from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoSeparateSearchConfig(AppConfig):  # Our app config class
    name = 'django_separate_search'
    verbose_name = _('Django Separate Search')

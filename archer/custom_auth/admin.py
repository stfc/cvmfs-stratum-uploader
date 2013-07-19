from django.contrib import admin
from archer.custom_auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django import forms


class CustomUserChangeForm(UserChangeForm):
    username = forms.RegexField(
        label=_("Username"), max_length=200, regex=r"^[\w.@+-=/ ]+$",
        help_text=_("Required. 200 characters or fewer. Letters, digits and "
                    "@/./+/-/_/=/ // only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_/=/ // characters.")})


class CustomUserCreationForm(UserCreationForm):
    username = forms.RegexField(label=_("Username"), max_length=200,
                                regex=r'^[\w.@+-=/ ]+$',
                                help_text=_("Required. 200 characters or fewer. Letters, digits and "
                                            "@/./+/-/_/=/ // only."),
                                error_messages={
                                    'invalid': _("This value may contain only letters, numbers and "
                                                 "@/./+/-/_/=/ // characters.")})


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm


admin.site.register(User, CustomUserAdmin)
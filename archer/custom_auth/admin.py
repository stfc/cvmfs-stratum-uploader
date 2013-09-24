from django.contrib import admin
from django.contrib.admin import ModelAdmin
from archer.custom_auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django import forms
from guardian.admin import GuardedModelAdmin


class CustomUserChangeForm(UserChangeForm):
    username = forms.RegexField(
        label=_("Username"), max_length=200, regex=r"^[\w.@+-=/ ]+$",
        help_text=_("Required. 200 characters or fewer. Letters, digits and "
                    "@/./+/-/_/=/ // only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_/=/ // characters.")},
        widget=forms.Textarea(attrs={'rows': '2', 'cols': '100'})
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.RegexField(label=_("Username"), max_length=200,
                                regex=r'^[\w.@+-=/ ]+$',
                                help_text=_("Required. 200 characters or fewer. Letters, digits and "
                                            "@/./+/-/_/=/ // only."),
                                error_messages={
                                    'invalid': _("This value may contain only letters, numbers and "
                                                 "@/./+/-/_/=/ // characters.")},
                                widget=forms.Textarea(attrs={'rows': '2', 'cols': '100'})
    )
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta:
        model = User
        fields = ("username",)


class CustomUserAdmin(UserAdmin, ModelAdmin):
    add_form_template = 'admin/custom_auth/user/add_form.html'
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    readonly_fields = ('last_login', 'date_joined', )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',),
        }),
    )


admin.site.register(User, CustomUserAdmin)
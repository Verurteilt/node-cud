from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
######################################

from nodejs.models import NodeUser
User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = NodeUser
        fields = ('email', 'twitter', 'first_name', 'last_name', 'birth',
                  'consumer_key', 'consumer_secret', 'access_token', 'access_token_secret')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="Passwords are not stored in plain text if you want to change the password go to <a href='password/'>Change password</a>")

    class Meta:
        model = NodeUser
        fields = ('email', 'twitter', 'first_name', 'last_name', 'birth', 'consumer_key', 'consumer_secret',
                  'access_token', 'access_token_secret', 'is_active', 'is_admin', 'is_superuser', 'profile_picture')

    def clean_password(self):
        return self.initial['password']


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
                (None, {'fields': ('email', 'password')}),
                ('Personal info', {'fields': ('birth', 'first_name', 'last_name', 'twitter', 'consumer_key',
                                   'consumer_secret', 'access_token', 'access_token_secret', 'profile_picture')}),
                ('Permissions', {'fields': ('is_admin', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
                    (None, {'classes': ('wide',), 'fields': ('email', 'twitter', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class LoginForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=True)
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=True)
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
    password_confirmation = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}), required=True)

    def clean_password_confirmation(self):
        print self
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirmation'):
            self._errors['password_confirmation'] = self.error_class([('Passwords must match.')])


class TweetForm(forms.Form):
    tweet = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': "Tweet", 'maxlength': "140"}), required=True)


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birth', 'twitter', 'consumer_key', 'consumer_secret',
                  'access_token_secret', 'access_token', 'profile_picture')
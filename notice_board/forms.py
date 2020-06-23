from django import forms
from .models import UserProfileInfo, Action, Improvement
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models import Q


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')


class InputActionForm(forms.ModelForm):
    title = forms.CharField(max_length=250, help_text="Enter Title...")
    text = forms.CharField(widget=forms.Textarea)
    due = forms.DateField()
    assigned = forms.CharField(max_length=250, help_text="Assign To...")
    #user_list = User.objects.all()
    #assigned = forms.MultipleChoiceField(choices=user_list, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Action
        fields = ['title', 'text', 'due', 'assigned']


class EditActionForm(forms.ModelForm):
    title = forms.CharField(max_length=250, help_text="Enter Title...")
    text = forms.CharField(widget=forms.Textarea)
    due = forms.DateField()
    assigned = forms.CharField(max_length=250, help_text="Assign to...")
    radioButtonChoices = [('True', 'complete'), ('False', 'complete')]
    complete = forms.ChoiceField(choices=radioButtonChoices, widget=forms.RadioSelect)
    #user_list = User.objects.all()
    #assigned = forms.MultipleChoiceField(choices=user_list, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Action
        fields = ('title', 'text', 'due', 'assigned')


class InputImprovementForm(forms.ModelForm):
    title = forms.CharField(max_length=250, help_text="Enter Title...")
    text = forms.CharField(widget=forms.Textarea)
    due = forms.DateField()
    assigned = forms.CharField(max_length=250, help_text="Assign To...")
    #user_list = User.objects.all()
    #assigned = forms.MultipleChoiceField(choices=user_list, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Improvement
        fields = ('title', 'text', 'due', 'assigned')


class EditImprovementForm(forms.ModelForm):
    title = forms.CharField(max_length=250, help_text="Enter Title...")
    text = forms.CharField(widget=forms.Textarea)
    due = forms.DateField()
    assigned = forms.CharField(max_length=250, help_text="Assign to...")
    radioButtonChoices = [('True', 'complete'), ('False', 'complete')]
    complete = forms.ChoiceField(choices=radioButtonChoices, widget=forms.RadioSelect)
    #user_list = User.objects.all()
    #assigned = forms.MultipleChoiceField(choices=user_list, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Improvement
        fields = ('title', 'text', 'due', 'assigned')


class RestorePasswordForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError('You entered an invalid email address.')

        if not user.is_active:
            raise ValidationError('This account is not active.')

        return email


class RestorePasswordViaEmailOrUsernameForm(forms.Form):
    email_or_username = forms.CharField(label='Email or Username')

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError('You entered an invalid email address or username.')

        if not user.is_active:
            raise ValidationError('This account is not active.')

        return email_or_username


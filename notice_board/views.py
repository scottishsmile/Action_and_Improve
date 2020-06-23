from django.shortcuts import render
from .models import Action, Improvement
from .forms import UserForm, InputActionForm, InputImprovementForm, EditActionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RestorePasswordForm, RestorePasswordViaEmailOrUsernameForm
from django.views.generic import View, FormView
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from .utils import send_reset_password_email
from django.shortcuts import get_object_or_404, redirect
from django.utils.encoding import force_bytes
from datetime import datetime
from rest_framework import generics, permissions
from .serializers import ActionSerializer, ImprovementSerializer, ImprovementOwners, ActionOwners
from django.contrib.auth.models import User


def index(request):
    all_actions = Action.objects.all()
    all_improvements = Improvement.objects.all()
    context = {'all_actions': all_actions, 'all_improvements': all_improvements, }
    return render(request, 'notice_board/index.html', context)


def action(request):
    all_actions = Action.objects.all()
    context = {'all_actions': all_actions, }
    return render(request, 'notice_board/action.html', context)


def action_detail(request, action_id,):
        action_404 = get_object_or_404(Action, pk=action_id)                # Test to see if action object is in the database. if not then display 404 error page.

        action = Action.objects.filter(pk=action_id)
        action_id = action_id

        # Edit Post Form
        if request.method == 'POST':
            form = EditActionForm(request.POST)
            if form.is_valid():
                action_id = action_id
                title = form.cleaned_data['title']
                text = form.cleaned_data['text']
                due = form.cleaned_data['due']
                assigned = form.cleaned_data['assigned']
                complete = form.cleaned_data['complete']
                edit_action = Action.objects.get(pk=action_id)
                edit_action.title = title
                edit_action.text = text
                edit_action.due = due
                edit_action.assigned = assigned
                edit_action.complete = complete
                edit_action.save()
                print('Action Edited!')
            else:
                print('Action Edit Error!')
                print('Form Error - ' + str(form.errors))

        # Put object into session so it can be passed to change_act_to_imp
        # That way we can save this object as an improvement then delete the action
        request.session['action_id'] = action_id

        context = {'action': action, 'action_id': action_id}
        return render(request, 'notice_board/action_detail.html', context)


def action_add(request):
    if request.method == 'POST':
        form = InputActionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            due = form.cleaned_data['due']
            created = datetime.now()
            assigned = form.cleaned_data['assigned']
            owner = request.user                         # Get the currently logged in user from django
            new_action = Action(title=title, text=text, due=due, created=created, assigned=assigned, owner=owner)
            new_action.save()
            print('Action Saved!')
        else:
            print('Action Add Error!')
            print('Form Error - ' + str(form.errors))
    return render(request, 'notice_board/action_add.html', {})


def action_print(request):
    all_actions = Action.objects.all()
    context = {'all_actions': all_actions, }
    return render(request, 'notice_board/action_print.html', context)


def change_act_to_imp(request):
    # Changes an action to an improvement and then deletes the action.
    # Uses a session to store the action. Session saved in def action_detail
    action_to_change = request.session.get('action_id', None)
    old_action = Action.objects.get(pk=action_to_change)

    # Create new improvement using action details
    create_improvement = Improvement(title=old_action.title, text=old_action.text, due=old_action.due, created=old_action.created, assigned=old_action.assigned, owner=old_action.owner)
    create_improvement.save()

    # Delete Old Action
    old_action.delete()

    return render(request, 'notice_board/action_changed.html', {})


def action_delete(request):
    # Deletes an action
    # Uses a session to store the action. Session saved in def action_detail
    action_to_delete = request.session.get('action_id', None)
    get_action = Action.objects.get(pk=action_to_delete)            # Use the session id number as the primary key to find the object
    get_action.delete()
    return render(request, 'notice_board/action_deleted.html', {})


# API Stuff

# Creates API main page
class api_actions(generics.ListCreateAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Creates API detail page
class api_actions_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# API User Authentication
class action_owners_list(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ActionOwners

class action_owners_detail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ActionOwners



def improvement_add(request):
    if request.method == 'POST':
        form = InputImprovementForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            due = form.cleaned_data['due']
            created = datetime.now()
            assigned = form.cleaned_data['assigned']
            owner = request.user  # Get the currently logged in user from django
            new_improvement = Improvement(title=title, text=text, due=due, created=created, assigned=assigned, owner=owner)
            new_improvement.save()
            print('Improvement Saved!')
        else:
            print('Improvement Add Error!')
            print('Form Error - ' + str(form.errors))
    return render(request, 'notice_board/improvement_add.html', {})


def improvement(request):
    all_improvements = Improvement.objects.all()
    context = {'all_improvements': all_improvements}
    return render(request, 'notice_board/improvement.html', context)


def improvement_detail(request, improvement_id):
    improvement_404 = get_object_or_404(Improvement, pk=improvement_id)  # Test to see if improvement object is in the database. if not then display 404 error page.

    improvement = Improvement.objects.filter(pk=improvement_id)
    improvement_id = improvement_id

    # Edit Post Form
    if request.method == 'POST':
        form = EditActionForm(request.POST)
        if form.is_valid():
            improvement_id = improvement_id
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            due = form.cleaned_data['due']
            assigned = form.cleaned_data['assigned']
            complete = form.cleaned_data['complete']
            edit_improvement = Improvement.objects.get(pk=improvement_id)
            edit_improvement.title = title
            edit_improvement.text = text
            edit_improvement.due = due
            edit_improvement.assigned = assigned
            edit_improvement.complete = complete
            edit_improvement.save()
            print('Improvement Edited!')
        else:
            print('Improvement Edit Error!')
            print('Form Error - ' + str(form.errors))

    # Put object into session so it can be passed to change_imp_to_act
    # That way we can save this object as an action and then delete the improvement
    request.session['improvement_id'] = improvement_id

    context = {'improvement': improvement, 'improvement_id': improvement_id, }
    return render(request, 'notice_board/improvement_detail.html', context)


def improvement_print(request):
    all_improvements = Improvement.objects.all()
    context = {'all_improvements': all_improvements}
    return render(request, 'notice_board/improvement_print.html', context)


def change_imp_to_act(request):
    # Changes an improvement to an action and then deletes the improvement
    # Uses a session to store the improvement. Session saved in def improvement_detail
    imp_to_change = request.session.get('improvement_id', None)
    old_improvement = Improvement.objects.get(pk=imp_to_change)

    # Create new action using improvement details
    create_action = Action(title=old_improvement.title, text=old_improvement.text, due=old_improvement.due, created=old_improvement.created, assigned=old_improvement.assigned, owner=old_improvement.owner)
    create_action.save()

    # Delete Old Improvement
    #imp_to_change.delete()
    old_improvement.delete()

    return render(request, 'notice_board/improvement_changed.html', {})


def improvement_delete(request):
    # Deletes an improvement
    # Uses a session to store the improvement. Session saved in def improvement_detail
    improvement_to_delete = request.session.get('improvement_id', None)
    get_imp = Improvement.objects.get(pk=improvement_to_delete)         # Use the session id number as the primary key to find the object
    get_imp.delete()
    return render(request, 'notice_board/improvement_deleted.html', {})


# API Stuff

# Creates API main page
class api_improvements(generics.ListCreateAPIView):
    queryset = Improvement.objects.all()
    serializer_class = ImprovementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Create API detail page
class api_improvements_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Improvement.objects.all()
    serializer_class = ImprovementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# API User Authentication
class improvement_owners_list(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ImprovementOwners

class improvement_owners_detail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ImprovementOwners


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('notice_board:index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    context = {'user_form': user_form, 'registered': registered}
    return render(request, 'notice_board/registration.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('notice_board:index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'notice_board/login.html', {})


class ChangePasswordView(PasswordChangeView):
    template_name = 'notice_board/password_reset_form.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        return render(self.request, 'notice_board/password_was_changed.html', {})


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect('notice_board/index.html')

        return super().dispatch(request, *args, **kwargs)


class RestorePasswordView(GuestOnlyView, FormView):
    template_name = 'notice_board/reset_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return RestorePasswordViaEmailOrUsernameForm

        return RestorePasswordForm

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

        send_reset_password_email(self.request, user.email, token, uid)

        return render(self.request, 'notice_board/reset_password.html', {})



from django.urls import path, include
from . import views
from .views import ChangePasswordView, RestorePasswordView
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'notice_board'

urlpatterns = [
    path('', views.index, name='index'),
    path('action/', views.action, name='action'),
    path('action/action_add', views.action_add, name='action_add'),
    path('action/<int:action_id>/', views.action_detail, name='action_detail'),
    path('action_print/', views.action_print, name='action_print'),
    path('change_act_to_imp/', views.change_act_to_imp, name='change_act_to_imp'),
    path('action_delete/', views.action_delete, name='action_delete'),
    path('improvement/', views.improvement, name='improvement'),
    path('improvement/<int:improvement_id>/', views.improvement_detail, name='improvement_detail'),
    path('improvement/improvement_add', views.improvement_add, name='improvement_add'),
    path('improvement_print/', views.improvement_print, name='improvement_print'),
    path('change_imp_to_act/', views.change_imp_to_act, name='change_imp_to_act'),
    path('improvement_delete/', views.improvement_delete, name='improvement_delete'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('restore_password/', RestorePasswordView.as_view(), name='restore_password'),
    path('api/actions/', views.api_actions.as_view(), name="api_actions"),
    path('api/actions/<int:pk>/', views.api_actions_detail.as_view(), name="api_actions_detail"),
    path('api/actions/users/', views.action_owners_list.as_view(), name="action_owners_list"),
    path('api/actions/users/<int:pk>/', views.action_owners_detail.as_view(), name="action_owners_detail"),
    path('api/improvements/', views.api_improvements.as_view(), name="api_improvements"),
    path('api/improvements/<int:pk>/', views.api_improvements_detail.as_view(), name="api_improvements_detail"),
    path('api/improvements/users/', views.improvement_owners_list.as_view(), name="improvement_owners_list"),
    path('api/improvements/users/<int:pk>/', views.improvement_owners_detail.as_view(), name="improvement_owners_detail"),
]

# Allows DRY format for the url pattern
urlpatterns = format_suffix_patterns(urlpatterns)

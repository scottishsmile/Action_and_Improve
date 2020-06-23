from django.contrib import admin
from .models import Action, Improvement, User, UserProfileInfo


admin.site.register(Action),
admin.site.register(Improvement),
admin.site.register(UserProfileInfo),
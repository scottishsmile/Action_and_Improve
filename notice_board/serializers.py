from rest_framework import serializers
from .models import Action, Improvement
from django.contrib.auth.models import User

# Displays the fields on the API page
class ActionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Action
        fields = ('pk', 'title', 'text', 'created', 'due', 'assigned', 'complete', 'owner',)


# User Authentication
class ActionOwners(serializers.ModelSerializer):
    actions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Action.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'actions')


# Displays the fields on the API page
class ImprovementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Improvement
        fields = ('pk', 'title', 'text', 'created', 'due', 'assigned', 'complete', 'owner', )


# User Authentication
class ImprovementOwners(serializers.ModelSerializer):
    improvements = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Improvement.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'improvements')


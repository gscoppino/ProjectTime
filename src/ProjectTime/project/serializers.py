""" Model serializers for use in handling request data and producing responses.
"""

from rest_framework import serializers
from ProjectTime.project.models import Project, Charge

class ProjectSerializer(serializers.ModelSerializer): # pylint: disable=too-many-ancestors
    """ Serializer for projects
    """
    class Meta: # pylint: disable=too-few-public-methods
        model = Project
        fields = '__all__'

class ChargeSerializer(serializers.ModelSerializer): # pylint: disable=too-many-ancestors
    """ Serializer for charges
    """
    class Meta: # pylint: disable=too-few-public-methods
        model = Charge
        fields = '__all__'

""" Model viewsets for providing REST interfaces to Django models.
"""

from rest_framework import viewsets
from ProjectTime.project.models import Project, Charge
from ProjectTime.project.serializers import ProjectSerializer, ChargeSerializer

class ProjectViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """ Viewset for projects
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filterset_fields = ('active',)

class ChargeViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """ Viewset for charges
    """
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    filterset_fields = ('project', 'start_time', 'closed',)

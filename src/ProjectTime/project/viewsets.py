from rest_framework import viewsets
from ProjectTime.project.models import Project, Charge
from ProjectTime.project.serializers import ProjectSerializer, ChargeSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filterset_fields = ('active',)

class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    filterset_fields = ('project', 'start_time', 'closed',)

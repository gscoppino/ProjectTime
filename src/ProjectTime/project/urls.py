from django.urls import path
from ProjectTime.project.views import DashboardView, ProjectCreateView, ProjectListView


urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('project', ProjectListView.as_view(), name='project-list'),
    path('project/create', ProjectCreateView.as_view(), name='project-create'),
]

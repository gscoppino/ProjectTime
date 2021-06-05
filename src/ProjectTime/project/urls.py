from django.urls import path

from ProjectTime.project.views import (ChargeCloseView, ChargeCreateView,
                                       ChargeListView, ChargeUpdateView,
                                       DashboardView, ProjectCreateView,
                                       ProjectListView, ProjectUpdateView)
from ProjectTime.timezone.views import TimezoneView

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('set-timezone', TimezoneView.as_view(success_url='dashboard'), name='set-timezone'),
    path('project', ProjectListView.as_view(), name='project-list'),
    path('project/create', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update', ProjectUpdateView.as_view(), name='project-update'),
    path('charge', ChargeListView.as_view(), name='charge-list'),
    path('charge/create', ChargeCreateView.as_view(), name='charge-create'),
    path('charge/<int:pk>/update', ChargeUpdateView.as_view(), name='charge-update'),
    path('charge/<int:pk>/close', ChargeCloseView.as_view(), name='close-charge'),
]

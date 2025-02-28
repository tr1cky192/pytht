from django.urls import path
from .views import *

urlpatterns = [
    path('hours_journal/', AccountingHoursTeacherView.as_view(), name="hours_journal"),
    path('search/', SearchingResultView.as_view(), name='search'),
    path('teacher_hours/<int:pk>/', TeacherHoursAdminJournal.as_view(), name="teacher_hours"),
    path('teacher_hours/current/', TeacherHoursJournal.as_view(), name="teacher_hours_current"),

]
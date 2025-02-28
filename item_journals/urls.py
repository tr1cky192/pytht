from django.urls import path
from .views import *
from . import views
from index.views import EducationPlanView

urlpatterns = [
    path('journal/<str:item>/<str:group_code>/<str:subgroup_name>/', ItemJournalView.as_view(), name='item_journal'),
    path('subgroup_journal/<str:item>/<str:group_code>/<str:subgroup_name>/', ItemJournalView.as_view(), name='subgroup_journal_view'),
    path('pass_journal/<str:item>/<str:group_code>/<str:subgroup_name>/', PassJournalView.as_view(), name='pass_journal'),
    path('student_journal/', StudentJournalView.as_view(), name='student_journal'),
    path('pass_student_journal/', PassStudentJournalView.as_view(), name='pass_student_journal'),
    path('json_data/', GetMarkJsonView.as_view(), name="json_data"),
    path('json_lecture_data/', GetLectureJsonView.as_view(), name="lecture_json_data"),
    path('delete_mark/', DeleteMarkView.as_view(), name='delete_mark'),
    path('update_mark/', UpdateMarkView.as_view(), name='update_mark'),
    path('update_lecture/', UpdateLectureView.as_view(), name='update_lecture'),
    path('delete_lecture/', DeleteLectureView.as_view(), name='delete_lecture'),
    path('worked_out_json/',WorkedOutChanges.as_view(), name='worked_out'),
    path('operations_history/<str:item>/<str:group_code>/<str:journal>/', SearchJournalView.as_view(), name="search_journal"),
    path('clear_history/<str:item>/<str:group_code>/<str:journal>/<str:subgroup_name>/', ClearHistoryForUserView.as_view(), name="clear_journal"),
    path('curator_journal/', CuratorJournalView.as_view(), name='curator_journal'),
    path('curator/student_plan/<int:student_id>/<str:rounded>/', EducationPlanView.as_view(), name='curator_student_plan'),
    path('export_student_file/', ExportThemesFileTemplateView.as_view(), name='themes_file_export'),
    path('import_themes/', ImportThemesView.as_view(), name='import_themes'),
]

import json
from unittest.mock import patch, MagicMock

from django.http import HttpResponse
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from leave_journals.models import OperationLog
from user.models import User
from .views import ItemJournalView, SearchJournalView, PassJournalView
from .models import CollageGroups, Subject, Curator, Subgroup, Student, ClassModel, StudentsProgress, Teacher, \
    WorkedOutLogs
from datetime import datetime
from django.utils import timezone


class ItemJournalViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.current_month = datetime.now().month
        self.group = CollageGroups.objects.create(group_code='test_group')
        self.subject = Subject.objects.create(item_name='test_subject')
        self.curator = Curator.objects.create(group=self.group, user=User.objects.create(username='curator'))
        self.teacher = Teacher.objects.create(teacher_full_name='Test Teacher')
        self.subgroup1 = Subgroup.objects.create(name='A', parent_group=self.group)
        self.subgroup2 = Subgroup.objects.create(name='a', parent_group=self.group)
        self.subgroup3 = Subgroup.objects.create(name='B', parent_group=self.group)
        self.student1 = Student.objects.create(student_full_name='Student One', group=self.group)
        self.student1.subgroups.add(self.subgroup1, self.subgroup2)
        self.student2 = Student.objects.create(student_full_name='Student Two', group=self.group)
        self.student2.subgroups.add(self.subgroup1, self.subgroup2, self.subgroup3)
        self.class_model = ClassModel.objects.create(subject=self.subject, group=self.group, sub_group=self.subgroup1,
                                                     date_class=datetime.now())
        self.progress1 = StudentsProgress.objects.create(student=self.student1, mark='A', class_model=self.class_model)
        self.progress2 = StudentsProgress.objects.create(student=self.student2, mark='B', class_model=self.class_model)

        self.user = User.objects.create_user(username='testuser', password='12345', email="test@gmail.com")

    @patch('item_journals.views.render')
    def test_get_item_journal_view(self, mock_render):
        self.client.login(username='testuser', password='12345')
        mock_render.return_value = HttpResponse(status=200)

        url = reverse('item_journal', args=['test_subject', 'test_group', 'A'])
        request = self.factory.get(url, {'month': self.current_month})
        request.user = self.user

        response = ItemJournalView.as_view()(request, item='test_subject', group_code='test_group', subgroup_name='A')
        self.assertEqual(response.status_code, 200)

        template_used = mock_render.call_args[0][1]
        self.assertEqual(template_used, 'item_journals/admin_journal.html')

        context = mock_render.call_args[0][2]
        self.assertIn('students_for_item', context)
        self.assertEqual(len(context['students_for_item']), 2)

        json_data = json.loads(context['data'])
        self.assertEqual(json_data["lectures_count"], 1)
        self.assertIn('progress', json_data)


class SearchJournalViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        self.group = CollageGroups.objects.create(group_code="G123")
        self.subject = Subject.objects.create(item_name="Math")
        self.operation = OperationLog.objects.create(
            journal="mark", group=self.group, subject=self.subject, operation_date=timezone.now(), created_by=self.user,
            operation="some operation"
        )

    def tearDown(self):
        self.user.delete()
        self.group.delete()
        self.subject.delete()
        self.operation.delete()

    def test_get_request_without_query(self):
        response = self.client.get(reverse('search_journal', kwargs={
            'item': 'Math',
            'group_code': 'G123',
            'journal': 'mark',
        }))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/history_search_result.html')
        self.assertEqual(len(response.context['history']), 0)

    @patch('haystack.query.SearchQuerySet')
    def test_get_request_with_query(self, mock_search):
        mock_search().filter().autocomplete.return_value = [MagicMock(object=self.operation)]

        response = self.client.get(reverse('search_journal', kwargs={
            'item': 'Math',
            'group_code': 'G123',
            'journal': 'mark'
        }), {'q': 'some operation'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/history_search_result.html')
        self.assertEqual(len(response.context['history']), 1)
        self.assertEqual(response.context['history'][0], self.operation)

    @patch('haystack.query.SearchQuerySet')
    def test_non_existent_group_or_subject(self, mock_search):
        mock_search().filter().autocomplete.return_value = [MagicMock(object=self.operation)]

        response = self.client.get(reverse('search_journal', kwargs={
            'item': 'Math',
            'group_code': 'G123',
            'journal': 'mark'
        }), {'q': 'non existing operation'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/history_search_result.html')
        self.assertEqual(len(response.context['history']), 0)
        self.assertFalse(response.context['history'])


class DeleteOperationLogsTest(TestCase):
    def SetUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        self.group = CollageGroups.objects.create(group_code="G123")
        self.subject = Subject.objects.create(item_name="Math")
        self.operation = OperationLog.objects.create(operation="operation", operation_date=timezone.now(),
                                                     group=self.group, subject=self.subject, created_by=self.user)

    def clear_history_test(self):
        response = self.client.get(reverse('clear_history', kwargs={
            'item': 'Math',
            'group_code': 'G123',
            'journal': 'mark',
            'subgroup': 'all',
        }))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'item_journals/admin_journal.html')

        self.operation.hidden_users.add(self.user)
        self.assertEqual(len(response.context['history']), 0)
        self.assertFalse(response.context['history'])


class PassJournalViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.factory = RequestFactory()

        self.group = CollageGroups.objects.create(group_code='testgroup')
        self.subject = Subject.objects.create(item_name='testsubject')
        self.subgroup = Subgroup.objects.create(name='A', parent_group=self.group)
        self.subgroup1 = Subgroup.objects.create(name='B', parent_group=self.group)
        self.student = Student.objects.create(student_full_name='Test Student', group=self.group)
        self.student.subgroups.add(self.subgroup, self.subgroup1)
        self.curator = Curator.objects.create(user=self.user, group=self.group)
        self.class_model = ClassModel.objects.create(subject=self.subject, date_class=timezone.now(), group=self.group,
                                                     sub_group=self.subgroup)
        self.progress = StudentsProgress.objects.create(student=self.student, subject=self.subject,
                                                        class_model=self.class_model, mark='Н')

        self.worked_out_logs = WorkedOutLogs.objects.create(mark_id=self.progress, absent_reason='Reason')

    @patch('item_journals.views.render')
    def test_get_pass_journal_view(self, mock_render):
        self.client.login(username='testuser', password='12345')
        mock_render.return_value = HttpResponse(status=200)

        url = reverse('pass_journal', args=['testsubject', 'testgroup', 'A'])
        request = self.factory.get(url, {'month': datetime.now().month})
        request.user = self.user

        response = PassJournalView.as_view()(request, item='testsubject', group_code='testgroup', subgroup_name='A')
        self.assertEqual(response.status_code, 200)

        template_used = mock_render.call_args[0][1]
        self.assertEqual(template_used, 'item_journals/pass_journal_admin.html')

        context = mock_render.call_args[0][2]
        self.assertIn('students_for_item', context)
        self.assertEqual(len(context['students_for_item']), 1)

        json_data = json.loads(context['data'])
        self.assertEqual(json_data["lectures_count"], 1)
        self.assertIn('progress', json_data)


class WorkedOutChangesTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.class_model = ClassModel.objects.create(
            id=1, type_of_class="Lecture", theme_of_class="Math", date_class=datetime.now().date()
        )
        self.student = Student.objects.create(id=1, student_full_name="John Doe")
        self.progress = StudentsProgress.objects.create(
            id=1, class_model=self.class_model, student=self.student, mark=None
        )

        self.url = reverse('worked_out')

    @patch('item_journals.models.WorkedOutLogs.save', autospec=True)
    @patch('leave_journals.models.OperationLog.save', autospec=True)
    def test_post_worked_out(self, mock_operation_log_save, mock_worked_out_log_save):
        data = {
            "absent_id": self.progress.id,
            "absent_reason": "Sick",
            "worked_on": 5,
            "before_worked": False
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'success')

        mock_worked_out_log_save.assert_called_once()
        mock_operation_log_save.assert_called_once()

        self.progress.refresh_from_db()
        self.assertEqual(self.progress.mark, '5')

    def test_post_no_data(self):
        data = {
            "absent_id": self.progress.id,
            "absent_reason": "",
            "worked_on": None,
            "before_worked": None
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'No data')

import json
from collections import defaultdict
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from haystack.query import SearchQuerySet
from django.shortcuts import get_object_or_404
from item_journals.models import StudentsProgress, ClassModel, Student, Subject, CollageGroups, Teacher


class AccountingHoursTeacherView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()

        context = {
            'teachers': all_teachers,
        }

        return render(request, 'accounting_hours/accounting_hours_journal_admin.html', context)


class SearchingResultView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            searching_request = request.GET.get('q')
            searching_results = SearchQuerySet().autocomplete(content_auto=searching_request)

            teachers = [result.object for result in searching_results]
        else:
            teachers = False

        return render(request, 'accounting_hours/accounting_hours_journal_admin.html', {'teachers': teachers})


class TeacherHoursAdminJournal(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk, *args, **kwargs):
        month = int(request.GET.get('month', datetime.now().month))
        year = datetime.now().year

        ua_months = [
            'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
            'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'
        ]

        current_month_name = ua_months[month - 1]
        previous_month = (month - 1) if month > 1 else 12
        next_month = (month + 1) if month < 12 else 1

        teacher = Teacher.objects.filter(id=pk).first()
        subjects_by_teacher = Subject.objects.filter(
            subjectteachergroup__teacher=teacher
        ).distinct()
        lectures = ClassModel.objects.filter(date_class__month=month, date_class__year=year).order_by('date_class')

        subject_by_teacher_dict = defaultdict(list)
        hours = 0
        minutes = 0
        for subject in subjects_by_teacher:
            lectures = ClassModel.objects.filter(subject=subject, date_class__month=month,
                                                 date_class__year=year).order_by('date_class')
            for lecture in lectures:
                minutes = len(lectures) * 45
                hours = minutes / 60
                subject_dict = {
                    'type': lecture.type_of_class,
                    'lesson_date': lecture.date_class,
                    'theme': lecture.theme_of_class,
                    'hours': hours,
                    'minutes': minutes,
                }
                subject_by_teacher_dict[subject].append(subject_dict)

        context = {
            'current_month': month,
            'current_month_name': current_month_name,
            'previous_month': previous_month,
            'previous_month_name': ua_months[previous_month - 1],
            'next_month': next_month,
            'next_month_name': ua_months[next_month - 1],
            "subjects": subjects_by_teacher,
            "subject_by_teacher": dict(subject_by_teacher_dict),
            "is_journal": False,
        }

        return render(request, 'accounting_hours/teacher_admin_hours.html', context)


class TeacherHoursJournal(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):
        month = int(request.GET.get('month', datetime.now().month))
        year = datetime.now().year

        ua_months = [
            'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
            'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'
        ]

        current_month_name = ua_months[month - 1]
        previous_month = (month - 1) if month > 1 else 12
        next_month = (month + 1) if month < 12 else 1

        teacher = get_object_or_404(Teacher, user=request.user)
        subjects_by_teacher = Subject.objects.filter(
            subjectteachergroup__teacher=teacher
        ).distinct()

        subject_by_teacher_dict = defaultdict(list)
        for subject in subjects_by_teacher:
            lectures = ClassModel.objects.filter(subject=subject, date_class__month=month,
                                                 date_class__year=year).order_by('date_class')
            for lecture in lectures:
                minutes = len(lectures) * 45
                hours = minutes / 60
                subject_dict = {
                    'type': lecture.type_of_class,
                    'lesson_date': lecture.date_class,
                    'theme': lecture.theme_of_class,
                    'hours': hours,
                    'minutes': minutes,
                }
                subject_by_teacher_dict[subject].append(subject_dict)

        context = {
            'current_month': month,
            'current_month_name': current_month_name,
            'previous_month': previous_month,
            'previous_month_name': ua_months[previous_month - 1],
            'next_month': next_month,
            'next_month_name': ua_months[next_month - 1],
            "subjects": subjects_by_teacher,
            "subject_by_teacher": dict(subject_by_teacher_dict),
        }

        return render(request, 'accounting_hours/teacher_admin_hours.html', context)

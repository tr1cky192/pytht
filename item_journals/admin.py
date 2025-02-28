from django.contrib import admin

from django.contrib.auth.models import Group

from user.models import User
from .models import Student, WorkedOutLogs, Subject, StudentsProgress, ClassModel, CollageGroups, Teacher, \
    SubjectTeacherGroup, Curator, Subgroup, ThemeForLesson, TypeForLesson
from .forms import StudentModelForm

# Register your models here.
admin.site.site_header = "Система адміністрації"
admin.site.index_title = "Таблиці"
admin.site.site_title = "Адміністрація"


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_full_name', 'user')
    search_fields = ['teacher_full_name']

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user",)
        form = super(TeacherAdmin, self).get_form(request, obj, **kwargs)
        return form


class WorkedOutAdmin(admin.ModelAdmin):
    list_display = ('absent_reason', 'worked_on', 'before_worked_out', 'date_worked_out')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('mark_id', 'is_worked_out', 'date_updated', 'date_created')
        form = super(WorkedOutAdmin, self).get_form(request, obj, **kwargs)
        return form


class LectureAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('identifier', 'date_created', 'sub_group')
        form = super(LectureAdmin, self).get_form(request, obj, **kwargs)
        return form


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_full_name', 'user', 'course_number', 'group')
    form = StudentModelForm
    filter_horizontal = ('subgroups',)
    search_fields = ['student_full_name', 'course_number']

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('user',)
        form = super(StudentAdmin, self).get_form(request, obj, **kwargs)
        return form


class StudentProgressAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = (
            'subject', 'date_of_progress', 'date_of_edit_progress', 'mark_element_id', 'lesson_date',
            'is_valuable', 'multi_mark_value', 'subgroup')
        form = super(StudentProgressAdmin, self).get_form(request, obj, **kwargs)
        return form


class CuratorAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            try:
                teachers_group = Group.objects.get(name='teachers')
                kwargs["queryset"] = teachers_group.user_set.all()
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SubjectTeacherGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ("groups",)


admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
admin.site.register(StudentsProgress, StudentProgressAdmin)
admin.site.register(ClassModel, LectureAdmin)
admin.site.register(CollageGroups)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(WorkedOutLogs, WorkedOutAdmin)
admin.site.register(SubjectTeacherGroup, SubjectTeacherGroupAdmin)
admin.site.register(Curator, CuratorAdmin)
admin.site.register(Subgroup)
admin.site.register(ThemeForLesson)
admin.site.register(TypeForLesson)

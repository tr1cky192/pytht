from django.db import models
from user.models import User


class CustomIntegerField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(CustomIntegerField, self).formfield(**defaults)


class Curator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    group = models.OneToOneField('CollageGroups', on_delete=models.CASCADE, related_name='curator_relation',
                                 verbose_name="Група", blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'куратор'
        verbose_name_plural = 'куратори'
        db_table = 'curators'

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.group.group_code if self.group else "Без групи"}'

    @property
    def first_name(self):
        return self.user.first_name if self.user else ''

    @property
    def last_name(self):
        return self.user.last_name if self.user else ''


class CollageGroups(models.Model):
    group_code = models.CharField(max_length=100, null=True, verbose_name="Назва групи")

    class Meta:
        db_table = 'collage_groups'
        verbose_name = 'група коледжу'
        verbose_name_plural = 'групи коледжу'

    def __str__(self):
        return self.group_code


class Subgroup(models.Model):
    name = models.CharField(max_length=15, verbose_name="Назва підгрупи")
    parent_group = models.ForeignKey(CollageGroups, on_delete=models.CASCADE, related_name='subgroups',
                                     verbose_name="Батьківська група")

    class Meta:
        unique_together = ('name', 'parent_group')
        db_table = 'subgroups'
        verbose_name = 'підгрупа'
        verbose_name_plural = 'підгрупи'

    def __str__(self):
        return f'{self.name} - {self.parent_group}'


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Користувач")
    teacher_full_name = models.CharField(max_length=150, verbose_name="Повне ім'я викладача")

    class Meta:
        verbose_name = 'викладач'
        verbose_name_plural = 'викладачі'
        db_table = 'teachers'

    def __str__(self):
        return self.teacher_full_name

    @property
    def first_name(self):
        return self.user.first_name if self.user else ''

    @property
    def last_name(self):
        return self.user.last_name if self.user else ''


class Subject(models.Model):
    item_name = models.CharField(max_length=250, unique=True, verbose_name="Назва предмету")

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предмети'
        db_table = 'subjects'

    def __str__(self):
        return self.item_name

    def get_teachers_for_group(self, group):
        return Teacher.objects.filter(subjectteachergroup__groups=group, subjectteachergroup__subject=self)

    def get_teachers_for_subgroup(self, subgroup):
        return Teacher.objects.filter(subjectteachergroup__group=subgroup.parent_group,
                                      subjectteachergroup__subject=self)


class SubjectTeacherGroup(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Викладач")
    groups = models.ManyToManyField(CollageGroups, blank=True, verbose_name="Групи", related_name="grps")

    class Meta:
        unique_together = ('teacher', 'subject')
        verbose_name = 'викладач для групи предмета'
        verbose_name_plural = 'викладачі для груп предметів'
        db_table = 'subject_teacher_group'

    def __str__(self):
        groups_str = ', '.join([group.group_code for group in self.groups.all()])  # Iterate over groups
        name = f'{self.subject.item_name}-({groups_str})--{self.teacher.teacher_full_name}'
        return name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    student_full_name = models.CharField(max_length=150, verbose_name="Повне ім'я")
    group = models.ForeignKey(CollageGroups, related_name='students', on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name="Група")
    subgroups = models.ManyToManyField(Subgroup, related_name="subgrs", blank=True, verbose_name="Підгрупи")
    course_number = models.IntegerField(null=True, blank=True, verbose_name="Курс студента")

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенти'
        db_table = 'students'

    def __str__(self):
        return self.student_full_name


class ClassModel(models.Model):
    theme_of_class = models.CharField(max_length=150, verbose_name="Тема заняття")
    type_of_class = models.CharField(max_length=50, null=True, verbose_name="Тип заняття")
    date_class = models.DateField(null=True, verbose_name="Дата заняття")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, verbose_name="Предмет")
    identifier = models.CharField(max_length=10, unique=True, null=True)
    group = models.ForeignKey(CollageGroups, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Група")
    teacher_for_change = models.CharField(max_length=100, null=True, blank=True, verbose_name="Викладач на заміну")
    sub_group = models.ForeignKey(Subgroup, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'classes'
        verbose_name = 'заняття'
        verbose_name_plural = 'заняття'

    def __str__(self):
        return f'{self.type_of_class}-{str(self.date_class)}'


class StudentsProgress(models.Model):
    mark = models.CharField(null=True, blank=True, max_length=5, verbose_name="Оцінка")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, verbose_name="Студент")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    class_model = models.ForeignKey(ClassModel, on_delete=models.CASCADE, null=True, verbose_name="Лекція")
    date_of_progress = models.DateTimeField(auto_now_add=True, null=True)
    date_of_edit_progress = models.DateTimeField(auto_now=True, null=True)
    mark_element_id = models.CharField(max_length=50, null=True)
    lesson_date = models.DateField(null=True)
    is_valuable = models.BooleanField(default=True)
    multi_mark_value = models.CharField(max_length=2, blank=True, default="11")
    subgroup = models.ForeignKey(Subgroup, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'progress'
        verbose_name = 'успішність студентів'
        verbose_name_plural = 'успішність студентів'

    def __str__(self):
        return f'{self.mark} - {self.student.student_full_name} для {self.class_model}'


class ExcelFileChanges(models.Model):
    file_name = models.CharField(max_length=70)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class WorkedOutLogs(models.Model):
    absent_reason = models.CharField(max_length=50, blank=True, verbose_name="Причина відсутності")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_worked_out = models.BooleanField(default=False)
    worked_on = models.IntegerField(blank=True, null=True, verbose_name="Відпрацьовано на")
    before_worked_out = models.CharField(blank=True, max_length=2, null=True, verbose_name="Перед відпрацюванням")
    date_worked_out = models.DateField(null=True, verbose_name="Дата відпрацювання")
    mark_id = models.ForeignKey(StudentsProgress, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'worked_out'
        verbose_name = 'відпрацювання'
        verbose_name_plural = 'відпрацювання'

    def __str__(self):
        return f'Відпрацювання N{self.id}'


class TypeForLesson(models.Model):
    type_name = models.CharField(max_length=50, verbose_name="Назва типу", unique=True)

    class Meta:
        db_table = "types"
        verbose_name = "тип для заняття"
        verbose_name_plural = "типи для заняття"

    def __str__(self):
        return self.type_name


class ThemeForLesson(models.Model):
    theme_name = models.CharField(max_length=100, verbose_name="Назва теми")
    item = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Предмет")
    for_type = models.ForeignKey(TypeForLesson, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Для типу")

    class Meta:
        unique_together = ('theme_name', 'item', 'for_type')
        db_table = "themes"
        verbose_name = "тема для заняття"
        verbose_name_plural = "теми для заняття"

    def __str__(self):
        return self.theme_name

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Student, SubjectTeacherGroup

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        group = cleaned_data.get('group')
        subgroups = cleaned_data.get('subgroups')

        for subgroup in subgroups:
            if group and subgroup and group != subgroup.parent_group:
                raise ValidationError({
                    'subgroups': _("Ви не можете обрати підгрупу, яка не належить до обраної вами групи"),
                })

        return cleaned_data

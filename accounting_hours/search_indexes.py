from haystack import indexes
from item_journals.models import Teacher
from leave_journals.models import OperationLog

class TeacherSearchIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    teacher_full_name = indexes.CharField(model_attr="teacher_full_name")

    content_auto = indexes.EdgeNgramField(model_attr="teacher_full_name")

    class Meta:
        model = Teacher
        fields = ["teacher_full_name"]

    def get_model(self):
        return Teacher

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class OperationSearchIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    operation = indexes.CharField(model_attr="operation")
    created_by = indexes.CharField(model_attr="created_by")
    operation_date = indexes.CharField(model_attr="operation_date")

    content_auto = indexes.EdgeNgramField(model_attr="operation")

    class Meta:
        model = Teacher
        fields = ["operation", "operation_date"]

    def get_model(self):
        return OperationLog

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
from django_filters import FilterSet
from .models import Course


class CourseFilter(FilterSet):
    class Meta:
        model = Course
        fields = {
            'category': ['exact'],
            'author': ['exact'],
            'level': ['exact'],
            'type_course': ['exact'],
            'certificate': ['exact'],
            'price': ['gt', 'lt'],
        }

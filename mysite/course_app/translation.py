from .models import (Teacher, Category, Course, Lesson,
                     Assignment, Exam, Question, Option)
from modeltranslation.translator import TranslationOptions,register


@register(Teacher)
class TeacherTranslationOptions(TranslationOptions):
    fields = ('bio', 'subjects')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('course_name', 'description')


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Assignment)
class AssignmentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Exam)
class ExamTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Option)
class OptionTranslationOptions(TranslationOptions):
    fields = ('variant',)

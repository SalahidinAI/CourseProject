from django.contrib import admin
import nested_admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin


class GeneralMedia:
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Teacher)
class TeacherAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Course)
class CourseAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Lesson)
class LessonAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Assignment)
class AssignmentAdmin(TranslationAdmin, GeneralMedia):
    pass


class OptionInline(TranslationInlineModelAdmin, nested_admin.NestedStackedInline, GeneralMedia):
    model = Option
    extra = 1


class QuestionInline(TranslationInlineModelAdmin, nested_admin.NestedStackedInline, GeneralMedia):
    inlines = [OptionInline]
    model = Question
    extra = 1


@admin.register(Exam)
class ExamAdmin(nested_admin.NestedModelAdmin, TranslationAdmin, GeneralMedia):
    inlines = [QuestionInline]


admin.site.register(UserProfile)
admin.site.register(GeneralCoursePrice)
admin.site.register(Network)
admin.site.register(Student)
admin.site.register(Certificate)
admin.site.register(CourseReview)
admin.site.register(TeacherRating)
admin.site.register(History)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
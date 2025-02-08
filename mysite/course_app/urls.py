from rest_framework import routers
from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.SimpleRouter()
router.register(r'user', UserProfileViewSet, basename='user_list')
router.register(r'history', HistoryViewSet, basename='history_list')
router.register(r'cart', CartItemViewSet, basename='cart_list')
router.register(r'favorite', FavoriteItemViewSet, basename='favorite_list')

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', UserRegisterSerializer.as_view(), name='teacher_register'),
    path('teacher/register/', TeacherRegisterView.as_view(), name='teacher_register'),
    path('student/register/', StudentRegisterView.as_view(), name='student_register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),

    path('teacher/', TeacherListAPIView.as_view(), name='teacher_list'),
    path('teacher/<int:pk>/', TeacherDetailAPIView.as_view(), name='teacher_detail'),
    path('teacher_list/', TeacherOwnListAPIView.as_view(), name='teacher_own_list'),
    path('teacher_list/<int:pk>/', TeacherOwnEditAPIView.as_view(), name='teacher_own_edit'),

    path('student/', StudentListAPIView.as_view(), name='student_own_list'),
    path('student/<int:pk>/', StudentEditAPIView.as_view(), name='student_own_edit'),

    path('course/', CourseListAPIView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailAPIView.as_view(), name='course_detail'),
    path('course/create/', CourseTeacherCreateAPIView.as_view(), name='course_teacher_create'),
    path('course_list/', CourseTeacherListAPIView.as_view(), name='course_teacher_list'),
    path('course_list/<int:pk>/', CourseTeacherEditAPIView.as_view(), name='course_teacher_edit'),

    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_teacher_create'),
    path('lesson_list/', LessonTeacherListAPIView.as_view(), name='lesson_teacher_list'),
    path('lesson_list/<int:pk>/', LessonTeacherDetailAPIView.as_view(), name='lesson_teacher_list'),

    path('assignment/', AssignmentListAPIView.as_view(), name='assignment_list'),
    path('assignment/<int:pk>/', AssignmentDetailAPIView.as_view(), name='assignment_detail'),
    path('assignment/create/', AssignmentCreateAPIView.as_view(), name='assignment_teacher_create'),
    path('assignment_list/', AssignmentTeacherListAPIView.as_view(), name='assignment_teacher_list'),
    path('assignment_list/<int:pk>/', AssignmentTeacherDetailAPIView.as_view(), name='assignment_teacher_detail'),

    path('certificate/create/', CertificateCreateAPIView.as_view(), name='certificate_create'),
    path('course_review/', CourseReviewCreateAPIView.as_view(), name='course_review_create'),
    path('network/create/', NetworkCreateAPIView.as_view(), name='network_create'),

    path('exam/', ExamListAPIView.as_view(), name='exam_list'),
    path('exam/<int:pk>/', ExamDetailAPIView.as_view(), name='exam_detail'),
    path('exam/create/', ExamTeacherCreateAPIView.as_view(), name='exam_teacher_create'),
    path('exam_list/', ExamTeacherListAPIView.as_view(), name='exam_teacher_list'),
    path('exam_list/<int:pk>/', ExamTeacherEditAPIView.as_view(), name='exam_teacher_edit'),

    path('question/create/', QuestionTeacherCreateAPIView.as_view(), name='question_teacher_create'),
    path('question_list/', QuestionTeacherListAPIView.as_view(), name='question_teacher_list'),
    path('question_list/<int:pk>/', QuestionTeacherEditAPIView.as_view(), name='question_teacher_edit'),

    path('option/create/', OptionTeacherCreateAPIView.as_view(), name='option_teacher_create'),
    path('option_list/', OptionTeacherListAPIView.as_view(), name='option_teacher_list'),
    path('option_list/<int:pk>/', OptionTeacherEdit.as_view(), name='option_teacher_edit'),
]

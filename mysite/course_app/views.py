from .serializers import *
from .models import *
from .paginations import Pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import CourseFilter
from .permissions import *
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegisterSerializer(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeacherRegisterView(generics.CreateAPIView):
    serializer_class = TeacherRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentRegisterView(generics.CreateAPIView):
    serializer_class = StudentRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class TeacherListAPIView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherListSerializer
    permission_classes = [CheckStudent]
    pagination_class = Pagination


class TeacherDetailAPIView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherDetailSerializer
    permission_classes = [CheckStudent]


class TeacherOwnListAPIView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return Teacher.objects.filter(id=self.request.user.id)


class TeacherOwnEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [CheckTeacherOrAdminEdit]


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)


class StudentEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [CheckStudentEdit]


class NetworkCreateAPIView(generics.CreateAPIView):
    serializer_class = NetworkSerializer
    permission_classes = [CheckTeacher]


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = Pagination


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    pagination_class = Pagination


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CourseFilter
    search_fields = ['course_name']
    ordering_fields = ['updated_at', 'price']


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class CourseTeacherCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [CheckTeacher]


class CourseTeacherListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    pagination_class = Pagination
    permission_classes = [CheckTeacher]

    def get_queryset(self):
        return Course.objects.filter(author=self.request.user)


class CourseTeacherEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CheckTeacher, CheckTeacherCourseEdit]


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonListSerializer
    pagination_class = Pagination


class LessonDetailAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonTeacherListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonListSerializer
    permission_classes = [CheckTeacher]
    pagination_class = Pagination

    def get_queryset(self):
        return Lesson.objects.filter(course__author=self.request.user)


class LessonTeacherDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [CheckTeacher, CheckTeacherLessonEdit]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [CheckTeacher]


class AssignmentListAPIView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentListSerializer
    pagination_class = Pagination


class AssignmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentDetailSerializer


class AssignmentTeacherListAPIView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentListSerializer
    permission_classes = [CheckTeacher]
    pagination_class = Pagination

    def get_queryset(self):
        return Assignment.objects.filter(course__author=self.request.user)


class AssignmentTeacherDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [CheckTeacher, CheckTeacherLessonEdit]


class AssignmentCreateAPIView(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [CheckTeacher]


class ExamListAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamListSerializer
    pagination_class = Pagination


class ExamDetailAPIView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamDetailSerializer


class ExamTeacherListAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamListSerializer
    permission_classes = [CheckTeacher]
    pagination_class = Pagination

    def get_queryset(self):
        return Exam.objects.filter(course__author=self.request.user)


class ExamTeacherEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [CheckTeacher, CheckTeacherLessonEdit]


class ExamTeacherCreateAPIView(generics.CreateAPIView):
    serializer_class = ExamSerializer
    permission_classes = [CheckTeacher]


class QuestionTeacherListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    permission_classes = [CheckTeacher]
    pagination_class = Pagination

    def get_queryset(self):
        return Question.objects.filter(exam__course__author=self.request.user)


class QuestionTeacherEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CheckTeacher, CheckQuestionTeacherEdit]


class QuestionTeacherCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [CheckTeacher]


class CertificateCreateAPIView(generics.CreateAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [CheckTeacher]


class OptionTeacherListAPIView(generics.ListAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionListSerializer
    permission_classes = [CheckTeacher]
    pagination_class = Pagination

    def get_queryset(self):
        return Option.objects.filter(question__exam__course__author=self.request.user)


class OptionTeacherEdit(generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [CheckTeacher, CheckOptionTeacherEdit]


class OptionTeacherCreateAPIView(generics.CreateAPIView):
    serializer_class = OptionSerializer
    permission_classes = [CheckTeacher]


class CourseReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [CheckStudent]


class TeacherRatingCreateAPIView(generics.CreateAPIView):
    serializer_class = TeacherRatingSerializer
    permission_classes = [CheckStudent]


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializers = self.get_serializer(cart)
        return Response(serializers.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [CheckStudent]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Favorite.objects.get_or_create(user=self.request.user)
        serializers = self.get_serializer(cart)
        return Response(serializers.data)


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer
    permission_classes = [CheckStudent]

    def get_queryset(self):
        return FavoriteItem.objects.filter(favorite__user__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Favorite.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

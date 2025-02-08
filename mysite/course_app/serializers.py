from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'age', 'profile_picture')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class TeacherRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('username', 'first_name', 'last_name', 'bio', 'work_days', 'subjects',
                  'age','email', 'phone_number', 'password', 'profile_picture', 'experience')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Teacher.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('user', 'level')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Student.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'


class TeacherSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name']


class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'bio']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'bio', 'work_days', 'subjects', 'experience']


class StudentSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'level']


class StudentSimpleSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Student
        fields = ['user']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name']


class CourseListSerializer(serializers.ModelSerializer):
    avg_stars = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    author = TeacherSimpleSerializer(many=True)
    discount = serializers.SerializerMethodField()
    change_price = serializers.SerializerMethodField()
    count_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_image', 'level', 'type_course', 'author',
                  'avg_stars', 'count_people', 'count_lesson', 'discount', 'old_price', 'discount_price',
                  'change_price']

    def get_discount(self, obj):
        return f'{obj.discount}%'

    def get_avg_stars(self, obj):
        return obj.get_avg_stars()

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_discount_price(self, obj):
        return obj.get_discount_price()

    def get_change_price(self, obj):
        return obj.get_change_price()

    def get_count_lesson(self, obj):
        return obj.get_count_lesson()


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'video', 'content']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class AssignmentDetailSerializer(serializers.ModelSerializer):
    course = CourseNameSerializer()
    students = StudentSimpleSerializer()
    due_date = serializers.DateField(format('%d %B %Y'))

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'course', 'students']


class AssignmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title']


class AssignmentCourseSerializer(serializers.ModelSerializer):
    students = StudentSimpleSerializer()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'students']


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class ExamListSerializer(serializers.ModelSerializer):
    course = CourseNameSerializer()

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course', 'end_time']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class OptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['variant', 'option_check']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionListSerializer(serializers.ModelSerializer):
    question_option = OptionListSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['title', 'score', 'question_option']


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class CertificateCourseSerializer(serializers.ModelSerializer):
    student = StudentSimpleSerializer()

    class Meta:
        model = Certificate
        fields = ['student', 'certificate_url', 'issued_date']


class CourseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = '__all__'


class CourseReviewGetSerializer(serializers.ModelSerializer):
    user = StudentSimpleSerializer()

    class Meta:
        model = CourseReview
        fields = ['user', 'parent', 'text', 'star']


class TeacherRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherRating
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    course = CourseNameSerializer()
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source='course')

    class Meta:
        model = CartItem
        fields = ['course', 'course_id']



class CartSerializer(serializers.ModelSerializer):
    user = StudentSimpleSerializer()
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class FavoriteItemSerializer(serializers.ModelSerializer):
    course = CourseNameSerializer()
    favorite_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source='course')

    class Meta:
        model = FavoriteItem
        fields = ['course', 'favorite_id']


class FavoriteSerializer(serializers.ModelSerializer):
    user = StudentSimpleSerializer()
    favorite_items = FavoriteItemSerializer(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'favorite_items']


class TeacherDetailSerializer(serializers.ModelSerializer):
    experience = serializers.SerializerMethodField()
    teacher_avg_rating = serializers.SerializerMethodField()
    teacher_courses = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'bio', 'subjects', 'experience', 'work_days',
                  'teacher_avg_rating', 'teacher_courses']

    def get_experience(self, obj):
        if obj.experience == 1:
            return f'{obj.experience} year'
        return f'{obj.experience} years'

    def get_teacher_avg_rating(self, obj):
        return obj.get_teacher_avg_rating()


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_course = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'category_course']


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer(many=True, read_only=True)
    author = TeacherSimpleSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%d %B %Y %H:%M')
    updated_at = serializers.DateTimeField(format('%d %B %Y %H:%M'))
    avg_stars = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    course_lesson = LessonCourseSerializer(many=True, read_only=True)
    course_assignment = AssignmentCourseSerializer(many=True, read_only=True)
    course_certificate = CertificateCourseSerializer(many=True, read_only=True)
    course_review = CourseReviewGetSerializer(many=True, read_only=True)
    discount_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    change_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['course_name', 'category', 'description',  'course_image', 'level', 'type_course', 'author',
                  'discount', 'old_price', 'discount_price', 'change_price', 'created_at', 'updated_at', 'certificate', 'avg_stars', 'count_people',
                  'course_lesson', 'course_assignment', 'certificate', 'course_certificate',
                  'course_review']

    def get_discount(self, obj):
        return f"{obj.discount}%"

    def get_avg_stars(self, obj):
        return obj.get_avg_stars()

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_discount_price(self, obj):
        return obj.get_discount_price()

    def get_change_price(self, obj):
        return obj.get_change_price()


class ExamDetailSerializer(serializers.ModelSerializer):
    course = CourseNameSerializer()
    exam_question = QuestionListSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course', 'end_time', 'exam_question']

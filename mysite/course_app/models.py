from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError


ROLE_CHOICES = (
    ('teacher', 'teacher'),
    ('student', 'student'),
)


LEVEL_CHOICES = (
    ('easy', 'easy'),
    ('middle', 'middle'),
    ('advanced', 'advanced'),
)


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                           MaxValueValidator(60)],
                                           null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_image/', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Network(models.Model):
    network_name = models.CharField(max_length=32)
    network_link = models.URLField()
    title = models.CharField(max_length=64, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}, {self.network_name}'


class Teacher(UserProfile):
    bio = models.TextField()
    DAYS_CHOICES = (
        ('MON', 'MON'),
        ('TUE', 'TUE'),
        ('WED', 'WED'),
        ('THU', 'THU'),
        ('FRI', 'FRI'),
        ('SAT', 'SAT'),
    )
    work_days = MultiSelectField(choices=DAYS_CHOICES, max_length=16, max_choices=6)
    subjects = models.TextField()
    experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(30)])
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='teacher')

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'

    def __str__(self):
        return f'{self.first_name} {self.role}'

    def get_teacher_avg_rating(self):
        total_ratings = self.teacher_ratings.all()
        stars = [i.star for i in total_ratings]
        return round(sum(stars) / len(stars), 1)


class Student(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_student')
    level = models.CharField(choices=LEVEL_CHOICES, max_length=16)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f'{self.user} {self.role}'


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class GeneralCoursePrice(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.price}'


class Course(models.Model):
    course_name = models.CharField(max_length=64)
    course_image = models.ImageField(upload_to='course_images', null=True, blank=True)
    description = models.TextField()
    category = models.ManyToManyField(Category, related_name='category_course')
    author = models.ManyToManyField(Teacher, related_name='teacher_courses')
    level = models.CharField(choices=LEVEL_CHOICES, max_length=16)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    old_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    TYPE_CHOICES = (
        ('free', 'free'),
        ('paid', 'paid'),
    )
    type_course = models.CharField(choices=TYPE_CHOICES, max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    certificate = models.BooleanField(default=True)
    admin_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.course_name}'

    def get_avg_stars(self):
        all_reviews = self.course_review.all()
        if all_reviews.exists():
            all_stars = [i.star for i in all_reviews if i.star]
            return round(sum(all_stars) / len(all_stars), 1)
        return 0

    def get_count_people(self):
        return self.course_review.count()

    def get_discount_price(self):
        general_price = GeneralCoursePrice.objects.first()
        if general_price:
            return general_price.price
        return round(self.price / 100 * (100 - self.discount), 2)
        # return round(self.price * (1 - (self.discount / 100)), 2)

    def get_change_price(self):
        return self.price - self.admin_price

    def get_count_lesson(self):
        return self.course_lesson.count()


class Lesson(models.Model):
    title = models.CharField(max_length=64)
    video_url = models.URLField(null=True, blank=True)
    video = models.FileField(upload_to='course_videos', null=True, blank=True)
    content = models.FileField(upload_to='course_documents', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lesson')

    def __str__(self):
        return f'{self.course} {self.title}'

    def clean(self):
        super().clean()
        if not self.video_url and not self.video and not self.content:
            raise ValidationError('Choose minimum one of (video_url, video, content)!')


class Assignment(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_assignment')
    students = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Exam(models.Model):
    title = models.CharField(max_length=32)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    end_time = models.DurationField()

    def __str__(self):
        return f'{self.title} {self.course}'


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_question')
    title = models.CharField(max_length=64)
    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])

    def __str__(self):
        return f'{self.exam} {self.title}'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_option')
    variant = models.CharField(max_length=64)
    option_check = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.variant} {self.option_check}'


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_certificate')
    issued_date = models.DateField(auto_now_add=True)
    certificate_url = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f'{self.student} {self.course}'


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_review')
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    star = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)

    def __str__(self):
        return f'{self.user} {self.course}'

    def clean(self):
        super().clean()
        if not self.text and not self.star:
            raise ValidationError('Choose minimum one of (text, star)!')


class TeacherRating(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_ratings')
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    star = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'{self.user} {self.teacher}'


class History(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} {self.course}'


class Cart(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        total_price = sum(
            i.course.get_discount_price() or 0
            for i in self.cart_items.all()
        )
        return total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cart} {self.course}"


class Favorite(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='favorite_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.favorite} {self.course}'


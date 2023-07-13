from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import User

from django.contrib.auth.models import Group

from .models import Achievement, AchTeacher, AchStudent, \
    AchievementAchTeacher, CurrentAchievementAchStudent, FinishedAchievementAchStudent, AchievementAchStudent
from .views import index
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set its log level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the console handler
formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

'''
Run all tests with: python manage.py test ach_admin
Run specific test with: python manage.py test ach_admin.tests.AchievementModelTests
'''

"""
Tests for models:
"""


class AchievementModelTests(TestCase):

    def setUp(self):
        """
        Set up test environment.
        """
        image_path = os.path.join(os.path.dirname(__file__), "static/images/img.png")
        image_file = open(image_path, "rb")
        image_data = image_file.read()
        image_file.close()
        image = SimpleUploadedFile("img.png", image_data, content_type="image/png")
        self.achievement = Achievement.objects.create(title="Test Achievement", icon=image)
        self.user1 = User.objects.create_user(email="user1@innopolis.university", password="password1")
        self.user2 = User.objects.create_user(email="user2@innopolis.university", password="password2")

    def unique_achievement_name(self):
        """
        Tests if database does not accept non-unique achievement titles.
        """
        # check for not unique names
        titles = ["achievement", "achievement"]
        for title in titles:
            achievement = Achievement(title=title)
            achievement.save()
            self.assertIs(Achievement.objects.filter(title=title).count(), 1)
        logger.info(f"unique_achievement_name test: passed")

    def test_achievement_ach_teacher_relation(self):
        """
        Testing the custom Many-to-Many relation between Achievement and AchTeacher.
        """
        # Create Users
        user1 = self.user1
        user2 = self.user2

        # Create AchTeachers
        teacher1 = AchTeacher.objects.create(user=user1, club_name="Club 1")
        teacher2 = AchTeacher.objects.create(user=user2, club_name="Club 2")

        # Create an Achievement
        achievement = self.achievement

        # Create AchievementAchTeacher instances
        achievement_ach_teacher1 = AchievementAchTeacher.objects.create(
            achievement=achievement, ach_teacher=teacher1
        )
        achievement_ach_teacher2 = AchievementAchTeacher.objects.create(
            achievement=achievement, ach_teacher=teacher2
        )

        # Check the relationship from Achievement to AchievementAchTeacher
        self.assertEqual(achievement.achievementachteacher_set.count(), 2)
        self.assertIn(achievement_ach_teacher1, achievement.achievementachteacher_set.all())
        self.assertIn(achievement_ach_teacher2, achievement.achievementachteacher_set.all())

        # Check the relationship from AchTeacher to AchievementAchTeacher
        self.assertEqual(teacher1.achievementachteacher_set.count(), 1)
        self.assertEqual(teacher2.achievementachteacher_set.count(), 1)
        self.assertEqual(teacher1.achievementachteacher_set.first().achievement, achievement)
        self.assertEqual(teacher2.achievementachteacher_set.first().achievement, achievement)

        logger.info(f"test_achievement_ach_teacher_relation test: passed")

    def test_mark_student_as_finished_method(self):
        user1 = self.user1
        # Create Group "Students" and register into it the two users
        group = Group.objects.create(name="Students", verbose_name="Students")
        group.user_set.add(user1)
        student1 = AchStudent.objects.create(user=user1)
        achievement = self.achievement
        # Create CurrentAchievementAchStudent instances
        current_achievement_ach_student1 = AchievementAchStudent.objects.create(
            achievement=achievement, ach_student=student1, status="subscribed")
        # Mark student as finished
        achievement.mark_student_as_finished(student1)

        # Check if the student is marked as finished
        # find that student in the list of finished students and confirm its status is "finished"
        self.assertEqual(achievement.achievementachstudent_set.get(ach_student=student1).status, "finished")

    def test_mark_student_as_subscribed_method(self):
        user1 = self.user1
        # Create Group "Students" and register into it the two users
        group = Group.objects.create(name="Students", verbose_name="Students")
        group.user_set.add(user1)
        student1 = AchStudent.objects.create(user=user1)
        achievement = self.achievement
        # Create CurrentAchievementAchStudent instances
        current_achievement_ach_student1 = AchievementAchStudent.objects.create(
            achievement=achievement, ach_student=student1, status="finished")
        # Mark student as subscribed
        achievement.mark_student_as_subscribed(student1)

        # Check if the student is marked as subscribed
        # find that student in the list of subscribed students and confirm its status is "subscribed"
        self.assertEqual(achievement.achievementachstudent_set.get(ach_student=student1).status, "subscribed")

    def test_achievement_ach_student_relation(self):
        """
        Testing the custom Many-to-Many relation between Achievement and AchStudent
        """
        # Create Users
        user1 = self.user1
        user2 = self.user2
        # Create Group "Students" and register into it the two users
        group = Group.objects.create(name="Students", verbose_name="Students")
        group.user_set.add(user1)
        group.user_set.add(user2)
        # Create AchStudents
        student1 = AchStudent.objects.create(user=user1)
        student2 = AchStudent.objects.create(user=user2)
        # Create an Achievement
        achievement = self.achievement
        # Create CurrentAchievementAchStudent instances
        current_achievement_ach_student1 = CurrentAchievementAchStudent.objects.create(
            achievement=achievement, ach_student=student1
        )
        current_achievement_ach_student2 = CurrentAchievementAchStudent.objects.create(
            achievement=achievement, ach_student=student2
        )
        # Check the relationship from Achievement to CurrentAchievementAchStudent
        self.assertEqual(achievement.currentachievementachstudent_set.count(), 2)
        self.assertIn(current_achievement_ach_student1, achievement.currentachievementachstudent_set.all())
        self.assertIn(current_achievement_ach_student2, achievement.currentachievementachstudent_set.all())
        # Check the relationship from AchStudent to CurrentAchievementAchStudent
        self.assertEqual(student1.currentachievementachstudent_set.count(), 1)
        self.assertEqual(student2.currentachievementachstudent_set.count(), 1)
        self.assertEqual(student1.currentachievementachstudent_set.first().achievement, achievement)
        self.assertEqual(student2.currentachievementachstudent_set.first().achievement, achievement)

        logger.info(f"test_achievement_ach_student_relation test: passed")


"""
Tests for views:
"""


class AchievementViewTest(TestCase):

    def setUp(self):
        """
        Set up test environment.
        """
        self.factory = RequestFactory()
        image_path = os.path.join(os.path.dirname(__file__), "static/images/img.png")
        image_file = open(image_path, "rb")
        image_data = image_file.read()
        image_file.close()
        image = SimpleUploadedFile("img.png", image_data, content_type="image/png")
        self.achievement = Achievement.objects.create(title="Test Achievement", icon=image)
        self.user1 = User.objects.create_user(email="user1@innopolis,university", password="password1")
        self.user2 = User.objects.create_user(email="user2@innopolis,university", password="password2")

    def test_index_view(self):
        """
        Test if index view is working correctly.
        Ensures that the view returns a successful response and contains the previously inserted achievement's title.
        Also, it tests if a teacher can see achievement assigned specifically to him/her.
        """
        url = reverse("ach_admin:index")
        user = self.user1
        teacher1 = AchTeacher.objects.create(user=user, club_name="Club 1")

        achievement = self.achievement

        # Create AchievementAchTeacher instances
        achievement_ach_teacher1 = AchievementAchTeacher.objects.create(
            achievement=achievement, ach_teacher=teacher1
        )

        request = self.factory.get(url)
        request.user = user
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.achievement.title)

        logger.info(f"index_view test: passed")

    def test_index_view_no_achievements(self):
        """
        Tests if index view is working correctly when no achievements are present for registered teacher.
        """
        Achievement.objects.all().delete()  # Delete all achievements
        url = reverse("ach_admin:index")
        user = self.user1
        teacher1 = AchTeacher.objects.create(user=user, club_name="Club 1")
        request = self.factory.get(url)
        request.user = user
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No achievements are available")  # Expect a message indicating no achievements

        logger.info(f"index_view_no_achievements test: passed")

    def test_achievement_model_str(self):
        """
        Test if __str__ method of Achievement model is working correctly.
        """
        achievement = Achievement.objects.create(title="Achievement")
        self.assertEqual(str(achievement), "Achievement")

        logger.info(f"achievement_model_str test: passed")

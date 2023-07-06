from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import User
from sport.models import Semester

# import Group from Authentification and Authorization
from django.contrib.auth.models import Group

from .models import Achievement, AchTeacher, AchStudent, \
    AchievementAchTeacher, CurrentAchievementAchStudent, FinishedAchievementAchStudent
from .views import index
from django.core.files.uploadedfile import SimpleUploadedFile
import os

'''
Run all tests with: python manage.py test ach_admin
Run specific test with: python manage.py test ach_admin.tests.AchievementModelTests
'''

"""
Tests for models:
"""


class AchievementModelTests(TestCase):

    def unique_achievement_name(self):
        """
        unique_achievement_name() returns False for achievements whose name
        is not unique.
        """
        # check for not unique names
        titles = ["achievement", "achievement"]
        for title in titles:
            achievement = Achievement(title=title)
            achievement.save()
            self.assertIs(Achievement.objects.filter(title=title).count(), 1)

    def test_achievement_ach_teacher_relation(self):
        """
        testing the custom relation between Achievement and AchTeacher
        """
        # Create Users
        user1 = User.objects.create_user(email="user1@gmail.com", password="password1")
        user2 = User.objects.create_user(email="user2@gmail.com", password="password2")

        # Create AchTeachers
        teacher1 = AchTeacher.objects.create(user=user1, club_name="Club 1")
        teacher2 = AchTeacher.objects.create(user=user2, club_name="Club 2")

        # Create an Achievement
        achievement = Achievement.objects.create(title="Test Achievement")

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

    # TODO: make the test work
    # def test_achievement_ach_student_relation(self):
    #     """
    #     testing the custom relation between Achievement and AchStudent
    #     """
    #     # Create Semester
    #     semester = Semester.objects.create(name="Test Semester")
#
    #     # Create Users
    #     user1 = User.objects.create_user(email="user1@gmail.com", password="password1")
    #     user2 = User.objects.create_user(email="user2@gmail.com", password="password2")
#
    #     # Create Group "Students" and register into it the two users
    #     group = Group.objects.create(name="Students", semester=semester)
    #     group.user_set.add(user1)
    #     group.user_set.add(user2)
#
    #     # Create AchStudents
    #     student1 = AchStudent.objects.create(user=user1, grade=1)
    #     student2 = AchStudent.objects.create(user=user2, grade=2)
#
    #     # Create an Achievement
    #     achievement = Achievement.objects.create(title="Test Achievement", semester=semester)
#
    #     # Create CurrentAchievementAchStudent instances
    #     current_achievement_ach_student1 = CurrentAchievementAchStudent.objects.create(
    #         achievement=achievement, ach_student=student1
    #     )
    #     current_achievement_ach_student2 = CurrentAchievementAchStudent.objects.create(
    #         achievement=achievement, ach_student=student2
    #     )
#
    #     # Check the relationship from Achievement to CurrentAchievementAchStudent
    #     self.assertEqual(achievement.currentachievementachstudent_set.count(), 2)
    #     self.assertIn(current_achievement_ach_student1, achievement.currentachievementachstudent_set.all())
    #     self.assertIn(current_achievement_ach_student2, achievement.currentachievementachstudent_set.all())
#
    #     # Check the relationship from AchStudent to CurrentAchievementAchStudent
    #     self.assertEqual(student1.currentachievementachstudent_set.count(), 1)
    #     self.assertEqual(student2.currentachievementachstudent_set.count(), 1)
    #     self.assertEqual(student1.currentachievementachstudent_set.first().achievement, achievement)
    #     self.assertEqual(student2.currentachievementachstudent_set.first().achievement, achievement)
#

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

    def test_index_view(self):
        """
        Test if index view is working correctly.
        Ensures that the view returns a successful response and contains the previously inserted achievement's title.
        """
        url = reverse("ach_admin:index")
        request = self.factory.get(url)
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.achievement.title)

    def test_index_view_no_achievements(self):
        """
        Tests if index view is working correctly when no achievements are present.
        """
        Achievement.objects.all().delete()  # Delete all achievements
        url = reverse("ach_admin:index")
        request = self.factory.get(url)
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No achievements are available")  # Expect a message indicating no achievements

    def test_achievement_model_str(self):
        """
        Test if __str__ method of Achievement model is working correctly.
        """
        achievement = Achievement.objects.create(title="Achievement")
        self.assertEqual(str(achievement), "Achievement")

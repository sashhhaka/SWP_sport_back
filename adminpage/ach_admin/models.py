from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings
import uuid



# Create your models here.

# base models
# an achievement, coaches and student django models
# each coach has a list of achievements and an achievement can be assigned to multiple coaches (many-to-many)
# each achievement has a list of assigned students to them (many-to-many)
# achievement has a name, an image
# coach has a login, password, name, surname, club name, bool flag for him being an admin of the website
# student has login, password, name, surname

def get_achievement_icon_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'{settings.ACHIEVEMENT_FOLDER}/' \
           f'{instance.title}/{uuid.uuid4()}.{ext}'

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='achievements')
    assigned_coaches = models.ManyToManyField('AchTeacher', blank=True)
    subscribed_students = models.ManyToManyField('AchStudent', blank=True)
    finished_students = models.ManyToManyField('AchStudent', blank=True, related_name='finished_students')

    def __str__(self):
        return self.title

    # def student_set(self):
    #     return self.subscribed_students


class AchTeacher(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, default=None)
    club_name = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    assigned_achievements = models.ManyToManyField(Achievement, blank=True)

    def __str__(self):
        return self.user.email


class AchStudent(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, default=None)
    current_achievements = models.ManyToManyField(Achievement, blank=True, related_name='current_achievements')
    finished_achievements = models.ManyToManyField(Achievement, blank=True, related_name='finished_achievements')

    def __str__(self):
        return self.user.email


# test models
# A Question has a question and a publication date.
# A Choice has two fields: the text of the choice and a vote tally.
# Each Choice is associated with a Question.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    # modifies output by Question.objects.all()
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    # each Choice is related to a single Question (one Question to many Choice)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

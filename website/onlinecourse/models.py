
import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
from django.urls import reverse
import uuid


# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE,default='1')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False
    can_join = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description
    def get_absolute_url(self):
        return reverse('onlinecourse:course_details', args=[str(self.id)])

# Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    can_join_only = models.ManyToManyField(Course, blank=True)
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username + "," + \
               self.occupation


# Course model


# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    embded_video = models.BooleanField(default=False)
    video_link = models.URLField(null=True, blank=True)
    video_title = models.CharField(max_length=200, default="title", blank=True)
    demo = models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return f'{self.title} - {self.course.name} - {self.demo}'

# Enrollment model
# <HINT> Once a user enrolled a class, an enrollment entry should be created between the user and course
# And we could use the enrollment to track information such as exam submissions
class Enrollment(models.Model):
    student = 'student'
    assistant = 'assistant'
    manager = 'manager'
    roles = [
        (student, 'student'),
        (assistant, 'assistant'),
        (manager, 'manager'),
        
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    role = models.CharField(max_length=10, choices=roles, default=student)
    rating = models.FloatField(default=5.0)
    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.name}'
    # if enrollment deleted, delete all submissions
    def delete(self, *args, **kwargs):
        self.submission_set.all().delete()
        super().delete(*args, **kwargs)

# <HINT> Create a Question Model with:
    # Used to persist question content for a course
    # Has a One-To-Many (or Many-To-Many if you want to reuse questions) relationship with course
    # Has a grade point for each question
    # Has question content
    # Other fields and methods you would like to design
class Question(models.Model):
    # Foreign key to lesson
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    # question text
    question_text = models.TextField(max_length=300)
    # question grade/mark
    grade = models.IntegerField(default=10)
    

    # <HINT> A sample model method to calculate if learner get the score of the question
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_wrong = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()
        
        if all_answers == selected_correct - selected_wrong:
            return True

        #if all_answers == selected_correct:
            #return True
        #else: 
            #return False

        


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
    
# <HINT> The submission model
# One enrollment could have multiple submission
# One submission could have multiple choices
# One choice could belong to multiple submissions
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    score = models.IntegerField(default=0)
    # get the score of the submission
    def get_score(self):
        score = 0
        for choice in self.choices.all():
            if choice.is_correct:
                score += choice.question.grade
        self.score = score
        return score
    
    
    
    def __str__(self):
        return f'{self.enrollment.user.username} submitted in {self.enrollment.course.name} with score {self.score}' 
#    Other fields and methods you would like to design

class Number_of_Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    number_of_submission = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.enrollment.user.username} submitted in {self.enrollment.course.name} with number of submission {self.number_of_submission}'
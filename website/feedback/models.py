from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=5)

    def __str__(self):
        return self.acronym

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_student = models.BooleanField()
    is_teacher = models.BooleanField()

    prefix = models.CharField(max_length=10)
    deoartment = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    faculty = models.ForeignKey(Profile, related_name='courses_taught' ,on_delete=models.CASCADE)
    students = models.ManyToManyField(Profile, related_name='courses_taken')

    def __str__(self):
        return '[' + self.code + '] ' + self.name

class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    difficulty = models.PositiveSmallIntegerField()
    clarity = models.PositiveSmallIntegerField() 
    relevance = models.PositiveSmallIntegerField()
    assignments = models.PositiveSmallIntegerField()
    evaluation = models.PositiveSmallIntegerField()

    comments = models.TextField()
    
    def __str__(self):
        return 'Feedback on ' + str(self.course) + ' by ' + str(self.author)

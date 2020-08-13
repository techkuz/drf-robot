from django.db import models

SCHOOL_GRADE_CHOICES = [(i, i) for i in range(1, 13)]
STUDENT_AVERAGE_CHOICES = [(i, i) for i in range(0, 101)]


class Student(models.Model):
    first_name = models.TextField(blank=False, default=None)
    last_name = models.TextField(blank=False, default=None)
    student_id = models.IntegerField()
    date_of_birth = models.DateField()
    school_grade = models.IntegerField(choices=SCHOOL_GRADE_CHOICES)
    student_average = models.IntegerField(choices=STUDENT_AVERAGE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)



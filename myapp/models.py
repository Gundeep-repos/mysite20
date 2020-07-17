from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(blank=False, max_length=300, default="")
    def __str__(self):
        return f'Name: {self.name}, Category: {self.category}'


class Course(models.Model):

     topic = models.ForeignKey(Topic, related_name='courses',
     on_delete=models.CASCADE)
     name = models.CharField(max_length=200)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     for_everyone = models.BooleanField(default=True)
     description = models.TextField(max_length=300, null=True, blank=True)
     interested = models.PositiveIntegerField(default = 0)
     stages = models.PositiveIntegerField(default = 3)

     def __str__(self):
         return f'Topic: {self.topic}, Name: {self.name}, Price: {self.price}'
     def discount(self):
        disc = self.price * 0.10
        return disc

class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
    ('CG', 'Calgery'),
    ('MR', 'Montreal'),
    ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return f'School: {self.school}, City: {self.city}, Interest: {self.interested_in}'


class Order(models.Model):

    Order_Choice = [(0, 'Canceled'), (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, related_name='orders', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    levels = models.PositiveIntegerField(blank=True, null=True)
    order_status = models.IntegerField(default=1, choices=Order_Choice)
    order_date = models.DateField()

    def __str__(self):
        return f'Course: {self.course}, Student: {self.student},' \
               f' Level: {self.levels}, Order status: {self.order_date}, Date: {self.order_date}'

    def total_cost(self):
        totalPrice = 0
        for course in Order.objects.all()['course']:
            totalPrice += course.price
        return totalPrice





from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order

def  add_50_to_hours(modeladmin, request, queryset):
      for course in queryset:
         course.hours += 10
         course.save()
      add_50_to_hours.short_description="increased hours by 10"

def upper_case_name(modeladmin, request, queryset):
   st=Student()
   for st in queryset:
      st.first_name=st.first_name.upper()
      st.last_name=st.last_name.upper()
      st.save()
   upper_case_name.short_description=st.first_name+st.last_name
   
# http://127.0.0.1:8000/admin/myapp/course/
class CourseAdmin(admin.ModelAdmin):
   list_display=('name','topic','price','hours','for_everyone')
   actions=[add_50_to_hours]
   
class StudentAdmin(admin.ModelAdmin):
   fields= ('first_name', 'last_name', 'city')
   list_display=('first_name', 'last_name', 'city')
   actions=[upper_case_name]

# Register your models here.
admin.site.register(Topic)
admin.site.register(Student,StudentAdmin)
admin.site.register(Order)
admin.site.register(Course,CourseAdmin)
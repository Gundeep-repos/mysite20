# Import necessary classes
from django.http import HttpResponse
from .models import Topic, Course, Student, Order
# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of topics: ' + '</p>'
    response.write(heading1)
    for topic in top_list:
        para = '<p>'+ str(topic.id) + ': ' + str(topic) + '</p>'
        response.write(para)
    course_names = Course.objects.all().order_by('price')[:5]
    heading2 = '<h2>' + 'List of Top 5 Courses: ' + '</h2>'
    response.write(heading2)
    for course in course_names:
        course_details = '<p>' + str(course.id) + ': ' + str(course.name) + '</p>'
        response.write(course_details)
    return response


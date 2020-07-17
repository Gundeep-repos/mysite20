# Import necessary classes
from django.http import HttpResponse
from .models import Topic, Course, Student, Order
from django.shortcuts import get_list_or_404
from django.shortcuts import render


# Create your views here.


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of topics: ' + '</p>'
    # response.write(heading1)
    # for topic in top_list:
    #     para = '<p>'+ str(topic.id) + ': ' + str(topic) + '</p>'
    #     response.write(para)

    # #course list

    # course_list = Course.objects.all().order_by('-price')[:5]
    # heading2 = '<p>' + 'List of Courses: ' + '</p>'
    # response.write(heading2)
    # for course in course_list:
    #     if(course.for_everyone):
    #         forEveryone = 'This Course is For Everyone!'
    #     else:
    #         forEveryone = 'This Course is Not For Everyone!'
    #     para1 = '<p>' + str(course.name) + ':' + forEveryone + '</p>'
    #     response.write(para1)

    return render(request, 'myapp/index.html', {'top_list': top_list})

    '''Part 1
    2. C) Wr are passing the context variable 'top_list' to the index view
    '''


def about(request):
    # response = HttpResponse()
    # response.write('<h1>This is an E-learning Website! Search our Topics to find all available Courses</h1>')
    data="This is an E-learning Website! Search our Topics to find all available Courses"
    return render(request, 'myapp/about.html', {'data': data})
    '''Part 1
    4. C) Wr are passing the context variable 'data' to the about view
    '''


def detail(request, top_no):
    response = HttpResponse()
    topic_name = Topic.objects.get(id = top_no).name
    # response.write('<h1>List of Courses of Topic: ' + str(topic_name)+'</h1>')
    course_list = get_list_or_404(Course, topic=top_no)

    # for course in course_list:
    #     response.write('<p>'+str(course.name)+'</p>')
    return render(request, 'myapp/detail.html', {'topic_name': topic_name, 'course_list': course_list})
    '''Part 1
    5. C) Wr are passing the context variables 'topic_name' and 'course_list' to the detail view
    '''

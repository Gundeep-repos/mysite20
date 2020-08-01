# Import necessary classes
from django.http import HttpResponse,HttpResponseRedirect
from .models import Topic, Course, Student, Order
from json import dumps
import datetime
from django.shortcuts import get_list_or_404, get_object_or_404
from django.shortcuts import render
from .forms import OrderForm,InterestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
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

    if request.session.test_cookie_worked():
        print('The test cookie is working')
        request.session.delete_test_cookie()
        print('Test cookie Deleted also')

    last_logged = ''
    if request.session.has_key('last_connection'):
        last_logged = request.session['last_connection']
        print(last_logged)


    return render(request, 'myapp/index.html', {'top_list': top_list, 'last_logged': last_logged})

    '''Part 1
    2. C) Wr are passing the context variable 'top_list' to the index view
    '''


def about(request):

    # response = HttpResponse()
    # response.write('<h1>This is an E-learning Website! Search our Topics to find all available Courses</h1>')

    data="This is an E-learning Website! Search our Topics to find all available Courses"

    if request.session.has_key('about_visits'):
        count = request.session['about_visits']
        if count >= 1:
            count = count + 1
            request.session['about_visits'] = count
            final1 = count
            request.session.set_expiry(300)
    else:
        request.session['about_visits'] = 1
        final1 = 1
        request.session.set_expiry(300)

    response = render(request, 'myapp/about.html', {'data': data, 'visits': final1})
    # Test cookie
    request.session.set_test_cookie()
    return response

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


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def placeOrder(request):
    #PART 2 1d
    #return render(request, 'myapp/placeOrder.html')

    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:

                if order.course.price > 150:
                    print("--im here--")
                    discounted_price = order.course.discount()
                    order.course.save()

                    Course.objects.filter(name=str(order.course)).update(price=discounted_price)
                    # order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg,'courlist': courlist})

def courseDetail(request,cour_id):
    course = Course.objects.get(id=cour_id)
    top_list = Topic.objects.all().order_by('id')[:10]
    print(course)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            #interested = form.save(commit=False)
            if form.cleaned_data['interested']:
                course.interested = course.interested + 1
                course.save()
        return render(request, 'myapp/index.html', {'top_list': top_list})

    else:
        form = InterestForm()
    return render(request, 'myapp/coursedetail.html', {'form': form,'course': course})

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime,datetime.datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                response = HttpResponseRedirect(reverse('myapp:index'))
                request.session['last_connection'] = dumps(datetime.datetime.now(), default=json_serial)
                request.session.set_expiry(3600)
                return response

            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    del request.session['last_connection']
    # logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

@login_required
def myaccount(request):
    if Student.objects.get(id=request.user.id):
        id=Student.objects.filter(id=request.user.id)
        Firstname= request.user.first_name
        Lastname= request.user.last_name
        # Orders
        orders = Order.objects.get(student=request.user.id);
        # List of interested
        intrstlist=id.values_list('interested_in__name')
        context= {'First_name': Firstname,'Last_name':Lastname,'interested_list':intrstlist, 'orders': orders}
        return render(request, 'myapp/myaccount.html', context)
    else:
         context="You are not a registered student!"
         return render(request, 'myapp/myaccount.html', context)
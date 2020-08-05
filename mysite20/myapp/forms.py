from django import forms
from myapp.models import Order, Student

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('student', 'course', 'levels', 'order_date')
        widgets= {
            'student':forms.RadioSelect(attrs={'class':'radio'}),
            'order_date':forms.SelectDateWidget(attrs={'class':'years=date.today()'}),
        }
        labels ={
            'student': "Student Name",
            'order_date': "Order Date",
        }
class InterestForm(forms.Form):
     CHOICES= (('1', 'Yes',),('0', 'No',))
     interested= forms.CharField(widget=forms.RadioSelect(choices=CHOICES))
     levels= forms.IntegerField(initial=1)
     comments= forms.CharField(widget=forms.Textarea(), required =False, label ="Additional Comments")

class RegisterForm(forms.ModelForm):
    class Meta: 
        model=Student
        fields=('username', 'password', 'first_name', 'last_name', 'city', 'interested_in')
        widgets= {
            'username':forms.TextInput(),
            'password':forms.PasswordInput(),
            'first_name':forms.TextInput(),
            'last_name':forms.TextInput(),
            'city':forms.TextInput(),
        }
        labels ={
            'username':"Enter username",
            'password':"Enter password",
            'firstname':"Enter your firstname",
            'lastname':"Enter your lastname",
            'city':"Enter your city",
        }
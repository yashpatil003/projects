from django.shortcuts import render ,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection



# Create your views here.



def index(request):

    return render(request,"loginapp/index.html")




# localhost:8000/signup
def signup(request):
    
    if request.method=='POST':
        fn=request.POST.get('first_name')
        ln=request.POST.get('last_name')
        un=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1==pass2:
            if User.objects.filter(username=un).exists():
             messages.error(request,'user name already exists')
             return redirect('/signup')
                
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'already have email')
                    return redirect('/signup')
                else:
                    user=User.objects.create_user(username=un,password=pass1,first_name=fn,last_name=ln)
                    user.save()
                    messages.info(request,'sign up successfully')
                    return redirect('/login')
                    
            
        
        else:
            messages.error(request,'password not match')
            return redirect('/signup')

    return render(request,'loginapp/signup.html')

# request ==> [ POST {username=x  password=y }  , session={username:'x'} ] request object
#   employee ==> [ eid=1 name='sachin' ] Employee object

def login(request):

    if request.method=='POST':

        username=request.POST.get('username')
        password=request.POST["password"]

        print(username,password)

        user=auth.authenticate(username=username,password=password)

        print(connection.queries)

        print(user)

        if user is not None:

            auth.login(request,user)
            
            request.session['questionindex']=0 # add questionindex in session dictionary

            # [questionindex=0] session dictionary

            request.session['answers']={}
            request.session['score']=0
            request.session["username"]=username
        
            messages.success(request,'login successfully')
            
            return render(request,'examapp/subject.html')
        else:
            messages.error(request,'invalid credential')
            return redirect('/login')
        
    return render (request,'loginapp/login.html')


#https://docs.djangoproject.com/en/5.1/topics/auth/default/




@login_required(login_url="/login")
def dashboard(request):
    return render (request,'loginapp/dashboard.html')



def logout(request):
    auth.logout(request)
    return redirect("/")


def search(request):

    searchString=request.GET["searchString"]

    return redirect(f"https://www.google.co.in/search?q={searchString}")
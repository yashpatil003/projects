from django.shortcuts import render ,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection

from examapp.models import Question


# Create your views here.

def startTest(request):

    subjectname=request.GET["subject"]
    request.session['subject']=subjectname
    
    queryset=Question.objects.filter(subject=subjectname).values()
    questionlist=list(queryset)

    request.session['questionlist']=questionlist

    question=questionlist[0]

    return render(request,"examapp/question.html",{'question':question})
def nextQuestion(request):
  
    if 'op' in request.GET:

        allanswers=request.session['answers'] # {}

        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]

        print(allanswers)

    #allquestions=Question.objects.all()
    
    queryset=Question.objects.filter(subject=request.session['subject'])
    allquestions=list(queryset)


    if request.session['questionindex']<len(allquestions)-1:

        request.session['questionindex']=request.session['questionindex'] + 1 #2

        question=allquestions[request.session['questionindex']]
   
        if question.qno==3:
            isdisabled=True
        else:
            isdisabled=False

        return render(request,'examapp/question.html',{'question':question,'isdisabled':isdisabled})
    
    else:
        return render(request,'examapp/question.html',{'question':allquestions[len(allquestions)-1]})



# 0  1  2
def previousQuestion(request):
    
    if 'op' in request.GET:

        allanswers=request.session['answers'] # {}

        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]

        print(allanswers)


    #allquestions=Question.objects.all()
    
    queryset=Question.objects.filter(subject=request.session['subject'])
    allquestions=list(queryset)

    if request.session['questionindex']>0:

        request.session['questionindex']=request.session['questionindex'] - 1 

        question=allquestions[request.session['questionindex']]
        
        qno=question.qno

        submitteddetails=request.session['answers']

        print(f"submitted answers are  {submitteddetails}")

        if str(qno) in submitteddetails:
            questiondetails=submitteddetails[str(qno)]
            previousanswer=questiondetails[3]
            print(f"previousanswer is {previousanswer}")
        else:
            previousanswer=''

        return render(request,'examapp/question.html',{'question':question,'previousanswer':previousanswer})


    else:
        return render(request,'examapp/question.html',{'question':allquestions[0]})


def endexam(request):
            
    if 'answers' in request.session:

        if 'op' in request.GET:

            allanswers=request.session['answers'] # {}

            allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]

            print(f"inside if {allanswers}")

        dictionary=request.session['answers'] 
        
        listoflist=dictionary.values()

        print(listoflist)

        print(f"dictionary in endexam button is {dictionary}")

        for list in listoflist:
            
            if list[2]==list[3]:
                request.session['score']=request.session['score']+1
        
        finalscore=request.session['score']

        username=request.session["username"]

        auth.logout(request) # remove all keys from session dictionary

        return render(request,'examapp/score.html',{'username':username,'score': finalscore, 'listoflist':listoflist})
    
    else:
        messages.info(request,"login again")
        return render(request,'login.html')


    #[ [1,'what is 1+1?',2,2] , [2,'what is 2+2?',4,6] , [3,'what is 3+3?',6,3]  ]

    # {1:[1,'what is 1+1?',2,2] , 2:[2,'what is 2+2?',4,6],3:[3,'what is 3+3?',6,3]}



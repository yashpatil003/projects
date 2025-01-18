from django.urls import path
from . import views

urlpatterns=[

    path('nextQuestion/',views.nextQuestion),
    path('previousQuestion/',views.previousQuestion),
    
    path('endexam/',views.endexam),
    path('startTest/',views.startTest)

]
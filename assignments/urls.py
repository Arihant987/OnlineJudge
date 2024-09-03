# urls.py
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from assignments import views


urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('problem/<int:problem_id>/', views.problem_detail, name='problem_detail'), # submit waala button bhi yahin par i.e. in problem_detail 
]


'''
urlpatterns =  [
    path('',views.submit,name='submit'),
]

  isko upar wale mein views.submit ki jagah views.problem_detail
'''

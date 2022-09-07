from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'
urlpatterns = [

    path(route='', view=views.CourseListView, name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('<int:pk>/', views.CourseDetailView, name='course_details'),
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('<int:course_id>/<int:lesson_id>/submit/', views.submit, name='submit'),
    path('<int:course_id>/<int:lesson_id>/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),

]
from email import message
from multiprocessing import context
from django.db.models.enums import Choices
from django.shortcuts import render
from django.http import HttpResponseRedirect
# <HINT> Import any new Models here
from .models import Course, Enrollment, Lesson, Question, Choice, Submission,Learner
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
from django.contrib import messages
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            learner = Learner.objects.create(user=user)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled

def check_if_can_join(user, course):
    can_join = False
    if user.id is not None:
        # Check if user enrolled
        learner = Learner.objects.get(user=user)
        if course in learner.can_join_only.all():
            print(learner,course)
            can_join = True
    print(can_join)
    return can_join

# CourseListView
# class CourseListView(generic.ListView):
#     template_name = 'onlinecourse/course_list_bootstrap.html'
#     context_object_name = 'course_list'


#     def get_queryset(self):
#         user = self.request.user
#         courses = Course.objects.order_by('-total_enrollment')[:10]
#         for course in courses:
#             if user.is_authenticated:
#                 course.is_enrolled = check_if_enrolled(user, course)
#         return courses
def CourseListView(request):
    courses = Course.objects.order_by('-total_enrollment')[:10]
    
    for course in courses:
        if request.user.is_authenticated:
            course.is_enrolled = check_if_enrolled(request.user, course)
            can_join = check_if_can_join(request.user, course)
            if can_join:
                course.can_join = True
            else:
                course.can_join = False
    return render(request, 'onlinecourse/course_list_bootstrap.html', {'course_list': courses})


def CourseDetailView(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user = request.user
    is_enrolled = check_if_enrolled(user, course)
    can_join = check_if_can_join(request.user, course)
    if not is_enrolled and user.is_authenticated and can_join:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()
        return render(request, 'onlinecourse/course_detail_bootstrap.html', {'course': course})
    if not is_enrolled:
        messages.info(request, 'You are not enrolled in this course.')
    if not can_join:
        messages.info(request, 'You can only join this course if you have a subscription.')
    return redirect('onlinecourse:index')
    


def enroll(request, course_id):
    courses = Course.objects.order_by('-total_enrollment')[:10]
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    can_join = check_if_can_join(request.user, course)
    print(can_join)
    if not is_enrolled and user.is_authenticated and can_join:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()
        return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))
    if is_enrolled:
        messages.info(request, 'You are already enrolled in this course.')
    if not can_join:
        messages.info(request, 'You can only join this course if you have a subscription.')
    return redirect('onlinecourse:index')
    


# <HINT> Create a submit view to create an exam submission record for a course enrollment,
# you may implement it based on following logic:
         # Get user and course object, then get the associated enrollment object created when the user enrolled the course
         # Create a submission object referring to the enrollment
         # Collect the selected choices from exam form
         # Add each selected choice object to the submission object
         # Redirect to show_exam_result with the submission id
def submit(request, course_id, lesson_id):
    user = request.user
    course = Course.objects.get(pk=course_id)
    lesson = Lesson.objects.get(pk=lesson_id)
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = extract_answers(request)
    submission.choices.set(selected_choices)

    return HttpResponseRedirect(reverse(viewname='onlinecourse:show_exam_result', args=(course.id, lesson.id, submission.id)))

# <HINT> def extract_answers // A example method to collect the selected choices 
# from the exam form from the request object
def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)

    return submitted_answers
    
# <HINT> Create an exam result view to check if learner passed exam and show their question results and result for each question,
# you may implement it based on the following logic:
        # Get course and submission based on their ids
        # Get the selected choice ids from the submission record
        # For each selected choice, check if it is a correct answer or not
        # Calculate the total score
def show_exam_result(request, course_id, lesson_id, submission_id):
    context = {}

    course = Course.objects.get(pk=course_id)
    submission = Submission.objects.get(pk=submission_id)
    selected_choices = submission.choices.all()

    lesson = Lesson.objects.get(pk=lesson_id)
    questions = lesson.question_set.all()

    full_score = 0
    total_score = 0
    
    for question in questions:
        full_score += question.grade
    
        if question.is_get_score(selected_choices):
            total_score += question.grade   

    final_score = round((total_score/full_score)*100)
    
    context = {
        'course' : course,
        'lesson' : lesson,
        'selected_choices' : selected_choices,
        'grade' : final_score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)


    




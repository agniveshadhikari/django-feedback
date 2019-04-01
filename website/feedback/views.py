from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser, User
from feedback.models import Profile, Feedback, Course

def index(request):
    if isinstance(request.user, AnonymousUser):
        return HttpResponseRedirect('/accounts/login/')
    try:
        if request.user.profile.is_student:

            all_courses = request.user.profile.courses_taken.all()
            fb_submitted = Feedback.objects.filter(author=request.user.profile).all()
            courses_submitted = [fb.course for fb in fb_submitted]
            courses_not_submitted = list(set(all_courses).difference(courses_submitted))
            return render(
                request,
                'feedback/courses_enrolled.html',
                {
                    'profile': request.user.profile,
                    'submitted': courses_submitted,
                    'not_submitted': courses_not_submitted
                }
            )
        if request.user.profile.is_teacher:
            return render(
                request,
                'feedback/courses_taught.html',
                {
                    "name": request.user.first_name,
                    "courses": Course.objects.filter(faculty=request.user.profile)
                })
    except Profile.DoesNotExist:
        return HttpResponse('No role assigned')

def feedback(request):
    if request.method == 'GET':
        # Render form here
        course_name = request.GET.get('course')
        author = request.user.profile
        return render(
            request,
            'feedback/form.html',
            {
                'course': course_name,
                'author': author.user.username
            }
        )
    elif request.method == 'POST':
        # Process data here
        Feedback(
            course=Course.objects.get(name=request.POST.get('course')),
            author=User.objects.get(username=request.POST.get('author')).profile,
            difficulty=request.POST.get('difficulty'),
            clarity=request.POST.get('clarity'),
            relevance=request.POST.get('relevance'),
            assignments=request.POST.get('assignments'),
            evaluation=request.POST.get('evaluation'),
            comments=request.POST.get('comments')
        ).save()

        return HttpResponseRedirect('/feedback/')

def stats(request):
    if request.method == 'GET':
        if not request.user.profile.is_teacher:
            return HttpResponse('Students not allowed here')
        course_name = request.GET.get('course')
        feedbacks = Feedback.objects.filter(course=Course.objects.get(name=course_name))

        difficulty_scores = [0]*5
        clarity_scores = [0]*5
        relevance_scores = [0]*5
        assignments_scores = [0]*5
        evaluation_scores = [0]*5

        for fb in feedbacks:
            difficulty_scores[fb.difficulty-1] += 1
            clarity_scores[fb.clarity-1] += 1
            relevance_scores[fb.relevance-1] += 1
            assignments_scores[fb.assignments-1] += 1
            evaluation_scores[fb.evaluation-1] += 1 

        return render(
            request,
            'feedback/course_stats.html',
            {
                "course": Course.objects.get(name=course_name),
                "difficulty_scores": difficulty_scores[::-1],
                "clarity_scores": clarity_scores[::-1],
                "relevance_scores": relevance_scores[::-1],
                "assignments_scores": assignments_scores[::-1],
                "evaluation_scores": evaluation_scores[::-1],
                "course_name": course_name[::-1]
            }
        )


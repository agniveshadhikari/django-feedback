from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from feedback.models import Profile

def index(request):
    if isinstance(request.user, AnonymousUser):
        return HttpResponse('Please login first')
    try:
        if request.user.profile.is_student:
            return HttpResponse('You have taken: ' + ', '.join(map(str, request.user.profile.courses_taken.all())))
        if request.user.profile.is_teacher:
            return HttpResponse('Teacher homepage')
    except Profile.DoesNotExist:
        return HttpResponse('No role assigned')
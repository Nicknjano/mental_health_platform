from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Resource
from checkins.models import CheckIn
from datetime import date

@login_required
def resource_recommendations(request):
    # Get the user's latest check-in
    latest_checkin = CheckIn.objects.filter(user=request.user).order_by('-date').first()

    if not latest_checkin:
        return render(request, 'resources/recommendations.html', {
            'resources': [],
            'message': 'No check-in data found. Please complete a daily check-in to receive recommendations.'
        })

    # Determine categories based on check-in data
    categories = []
    if latest_checkin.stress_level >= 4:
        categories.append('stress')
    if latest_checkin.sleep_hours < 6:
        categories.append('sleep')
    if latest_checkin.mood <= 2:
        categories.append('mindfulness')

    # Fetch resources matching these categories
    recommended_resources = Resource.objects.filter(category__in=categories)

    return render(request, 'resources/recommendations.html', {
        'resources': recommended_resources,
        'message': 'Here are some resources based on your latest check-in.'
    })

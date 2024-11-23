from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CheckIn
from datetime import date

@login_required
def daily_checkin(request):
    if request.method == 'POST':
        mood = request.POST['mood']
        sleep_hours = request.POST['sleep_hours']
        stress_level = request.POST['stress_level']
        notes = request.POST.get('notes', '')
        
        # Prevent multiple check-ins per day
        if CheckIn.objects.filter(user=request.user, date=date.today()).exists():
            return render(request, 'checkins/checkin.html', {'error': 'You have already checked in today.'})
        
        # Save the check-in
        CheckIn.objects.create(
            user=request.user,
            mood=mood,
            sleep_hours=sleep_hours,
            stress_level=stress_level,
            notes=notes
        )
        return redirect('daily_checkin')  # Redirect to the same page after successful check-in
    
    return render(request, 'checkins/checkin.html')


from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CheckIn
from datetime import date
import json


@login_required
def analytics_dashboard(request):
    # Fetch data for mood, stress, and sleep
    mood_data = CheckIn.objects.filter(user=request.user).values_list('date', 'mood')
    stress_data = CheckIn.objects.filter(user=request.user).values_list('date', 'stress_level')
    sleep_data = CheckIn.objects.filter(user=request.user).values_list('date', 'sleep_hours')

    # Convert data to lists of tuples (dates and values)
    mood_data = list(mood_data)
    stress_data = list(stress_data)
    sleep_data = list(sleep_data)

    # Pass the data to the template
    return render(request, 'checkins/dashboard.html', {
        'mood_data': mood_data,
        'stress_data': stress_data,
        'sleep_data': sleep_data,
    })



from resources.models import Resource

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

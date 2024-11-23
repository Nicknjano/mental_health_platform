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

@login_required
def analytics_dashboard(request):
    checkins = CheckIn.objects.filter(user=request.user).order_by('date')
    mood_data = [(checkin.date, checkin.mood) for checkin in checkins]
    stress_data = [(checkin.date, checkin.stress_level) for checkin in checkins]
    sleep_data = [(checkin.date, checkin.sleep_hours) for checkin in checkins]

    context = {
        'mood_data': mood_data,
        'stress_data': stress_data,
        'sleep_data': sleep_data,
    }
    return render(request, 'checkins/dashboard.html', context)

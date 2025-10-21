from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import UserProfile, UploadedContent

def homepage(request):
    return render(request, 'education/homepage.html')







def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user, role=form.cleaned_data['role'])
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'education/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user_profile.role == 'student':
                return redirect('student_dashboard')
    return render(request, 'education/login.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

@login_required
def teacher_dashboard(request):
    if request.user.userprofile.role != 'teacher':
        return redirect('homepage')
    if request.method == 'POST':
        # Handle file uploads here
        pass
    return render(request, 'education/teacher_dashboard.html')

@login_required
def student_dashboard(request):
    if request.user.userprofile.role != 'student':
        return redirect('homepage')
    
    # Get user's watched videos count (you'll need to implement this logic)
    videos_watched = request.user.watched_videos.count() if hasattr(request.user, 'watched_videos') else 0
    
    # Get user's notes count (you'll need to implement this logic)
    notes_taken = request.user.notes.count() if hasattr(request.user, 'notes') else 0
    
    # Get user's streak (you'll need to implement this logic)
    streak_days = 7  # Example value, implement your own logic
    
    # Get user's achievements count (you'll need to implement this logic)
    achievements = 3  # Example value, implement your own logic
    
    # Sample recent activities (replace with actual data from your models)
    recent_activities = [
        {
            'type': 'video',
            'text': 'You completed watching "Introduction to Python"',
            'time': '2 hours ago',
            'badge': 'New'
        },
        {
            'type': 'note',
            'text': 'You took notes on "Data Structures"',
            'time': '1 day ago'
        },
        {
            'type': 'quiz',
            'text': 'You scored 85% on "Python Basics Quiz"',
            'time': '2 days ago',
            'badge': 'High Score!'
        },
        {
            'type': 'video',
            'text': 'You started "Web Development with Django"',
            'time': '3 days ago'
        }
    ]
    
    # Get recommended videos (you might want to implement a recommendation system)
    recommended_videos = VideoContent.objects.order_by('-created_at')[:4]
    
    context = {
        'stats': {
            'videos_watched': videos_watched,
            'notes_taken': notes_taken,
            'streak_days': streak_days,
            'achievements': achievements,
        },
        'recent_activities': recent_activities,
        'recommended_videos': recommended_videos,
    }
    
    return render(request, 'education/student/dashboard.html', context)
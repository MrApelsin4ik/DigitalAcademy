from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import Tasks, UserProfile, Directions


def logout_user(request):
    logout(request)
    return redirect('main')


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile(user=user, region=form.cleaned_data['region'],
                                       is_participant=form.cleaned_data['is_participant'],
                                       school_name=form.cleaned_data['school_name'],
                                       full_name=form.cleaned_data['full_name'], age=form.cleaned_data['age'],
                                       grade_or_course=form.cleaned_data['grade_or_course'],
                                       organization_name=form.cleaned_data['organization_name'],
                                       email=form.cleaned_data['email'])
            print(form.cleaned_data['is_participant'])
            user_profile.save()
            login(request, user)
            return redirect('main')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Ошибка в поле '{field}': {error}")
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')

    return render(request, 'login.html')


@login_required
def main(request):
    # Получаем профиль пользователя
    user_profile = UserProfile.objects.get(user=request.user)
    direction = Directions.objects.all()
    # Проверяем, является ли пользователь партнером
    if user_profile.is_participant:
        # Редирект для участника
        return redirect('tasklist')
    else:
        # Редирект для партнера
        return redirect('partner_profile')


@login_required
def partner_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':

        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        region = request.POST.get('region')
        school_name = request.POST.get('school_name')
        grade_or_course = request.POST.get('grade_or_course')
        organization_name = request.POST.get('organization_name')
        avatar = request.FILES.get('avatar')

        user = user_profile
        if email:
            user.email = email
        if full_name:
            user.full_name = full_name
        if age:
            user.age = age
        if region:
            user.region = region
        if school_name:
            user.school_name = school_name
        if grade_or_course:
            user.grade_or_course = grade_or_course
        if organization_name:
            user.organization_name = organization_name
        if avatar:
            user.avatar = avatar

        user.save()
        return redirect(partner_profile)
    else:
        user = request.user
        if not user_profile.avatar:
            user_profile.avatar = None

        context = {
            'username': user.username,
            'avatar': user_profile.avatar,
            'tasks': Tasks.objects.all(),
        }
        return render(request, 'partner_profile.html', context)


@login_required
def tasklist_view(request):
    tasks = Tasks.objects.all()
    directions = Directions.objects.all()
    return render(request, 'tasklist_page.html', {'tasks': tasks, 'directions': directions})

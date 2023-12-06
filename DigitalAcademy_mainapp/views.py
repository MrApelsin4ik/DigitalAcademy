from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import Tasks
from .models import UserProfile


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile(user=user, region=form.cleaned_data['region'], is_participant=form.cleaned_data['is_participant'], school_name=form.cleaned_data['school_name'], full_name=form.cleaned_data['full_name'], age = form.cleaned_data['age'], grade_or_course=form.cleaned_data['grade_or_course'], organization_name=form.cleaned_data['organization_name'], email=form.cleaned_data['email'])
            user_profile.save()
            login(request, user)
            return redirect('main')  # Redirect to a success page
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

    # Проверяем, является ли пользователь партнером
    if user_profile.is_participant:
        # Редирект для участника
        return redirect('partner_profile')
    else:
        # Редирект для партнера
        return redirect('tasklist')


def tasklist_view(request):
    tasks = Tasks.objects.all()
    return render(request, 'tasklist_page.html', {'tasks': tasks})

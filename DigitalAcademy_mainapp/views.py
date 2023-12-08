from random import randint

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from . import yagpt
from .forms import RegistrationForm
from .models import Tasks, UserProfile, Directions, TaskFile, DirectionTasks, OwnerTask, Solved, Wallet


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

def chat(request):
    if request.method == 'POST':
        message = request.POST['message']
        if message:
            response = yagpt.generate(message)
            return render(request, 'chat.html', {'response': response})
        else:
            return redirect('chat')
    else:
        return render(request, 'chat.html')


def wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    wallet_id = wallet.am

    return render(request, 'wallet.html', {'wallet': wallet_id})

@login_required
def participant_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':

        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        region = request.POST.get('region')
        school_name = request.POST.get('school_name')
        grade_or_course = request.POST.get('grade_or_course')
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
        if avatar:
            user.avatar = avatar

        user.save()
        return redirect(partner_profile)
    else:
        user = request.user
        user_tasks_ids = OwnerTask.objects.filter(user=user).values_list('task_id', flat=True)
        user_tasks = Tasks.objects.filter(id__in=user_tasks_ids)

        is_avatar = True
        if not user_profile.avatar:
            user_profile.avatar = None
            is_avatar = False
        context = {
            'username': user.username,
            'avatar': user_profile.avatar,
            'tasks': user_tasks,
            'is_avatar': is_avatar,
        }
    return render(request, 'participant_profile.html', context)

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.is_participant:
        # Редирект для участника
        return redirect('participant_profile')
    else:
        # Редирект для партнера
        return redirect('partner_profile')


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
        return redirect('tasklist')
    else:
        # Редирект для партнера
        return redirect('partner_profile')


def task(request):
    if request.method == "POST":
        task_id = request.POST['task_id']
        task = get_object_or_404(Tasks, id=task_id)
        name = request.POST['solution_name']
        description = request.POST['solution_description']

        # Create a new Solved instance with the  data
        solved = Solved.objects.create(user=request.user, task_id=task, name=name, description=description)

        return redirect('tasklist')


def task_detail(request, task_id):

    task = Tasks.objects.get(id=task_id)
    task_files = TaskFile.objects.filter(id=task_id)
    return render(request, 'task_detail.html', {'task': task, 'task_files': task_files, 'task_id': task_id})


@login_required
def add_project(request):

    return render(request, 'add_project.html', )


@login_required
def partner_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':

        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        region = request.POST.get('region')
        organization_name = request.POST.get('organization_name')
        avatar = request.FILES.get('avatar')

        user = user_profile
        if email:
            user.email = email
        if full_name:
            user.full_name = full_name
        if organization_name:
            user.organization_name = organization_name
        if avatar:
            user.avatar = avatar

        user.save()
        return redirect(partner_profile)
    else:
        user = request.user
        user_tasks_ids = OwnerTask.objects.filter(user=user).values_list('task_id', flat=True)
        user_tasks = Tasks.objects.filter(id__in=user_tasks_ids)

        is_avatar = True
        if not user_profile.avatar:
            user_profile.avatar = None
            is_avatar = False
        context = {
            'username': user.username,
            'avatar': user_profile.avatar,
            'tasks': user_tasks,
            'is_avatar': is_avatar,
        }
        return render(request, 'partner_profile.html', context)


@login_required
def make_task(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        selected_directions = request.POST.getlist('direction')

        # Create a new task
        new_task = Tasks(name=name, description=description, accelcoin_amount=randint(1, 70))
        new_task.save()

        task_file = TaskFile(task=new_task, file=file)
        task_file.save()

        for direction_id in selected_directions:
            DirectionTasks.objects.create(direction_id=direction_id, task_id=new_task.id)

        OwnerTask.objects.create(task_id=new_task, user=request.user)



    else:
        directions = Directions.objects.all()
        return render(request, 'make_task.html', {'directions': directions})

    return redirect('partner_profile')


@login_required
def tasklist_view(request):

    if request.method == 'POST':
        search_keyword = request.POST.get('search', '')
        selected_directions = request.POST.getlist('directions')  # Массив выбранных направлений

        tasks = Tasks.objects.all()

        # Фильтрация по направлениям
        if 'all' not in selected_directions:
            tasks = tasks.filter(directions__in=selected_directions)
        """
        # Поиск по названию задания
        if search_keyword:
            tasks = tasks.filter(name=search_keyword)
        """
        context = {
            'tasks': tasks,
            'directions': Directions.objects.all()  # передаем все направления для отображения фильтров
        }

        return render(request, 'tasklist_page.html', context)

    else:
        context = {
            'tasks': Tasks.objects.all(),
            'directions': Directions.objects.all()
        }
    return render(request, 'tasklist_page.html', context)



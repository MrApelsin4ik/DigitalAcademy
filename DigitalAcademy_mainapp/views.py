from django.shortcuts import render, redirect

from .forms import ParticipantRegistrationForm, PartnerRegistrationForm


def signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'participant':
            form = ParticipantRegistrationForm(request.POST)
        elif user_type == 'partner':
            form = PartnerRegistrationForm(request.POST)
        else:
            # Обработка некорректного значения user_type
            return redirect('registration')

        if form.is_valid():
            form.save()
            # Добавьте необходимую логику для успешной регистрации

    else:
        form = ParticipantRegistrationForm()  # или любая другая форма по умолчанию

    return render(request, 'signup.html', {'form': form})


def login(request):
    pass
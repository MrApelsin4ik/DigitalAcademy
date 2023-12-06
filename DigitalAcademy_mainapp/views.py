from django.shortcuts import render, redirect

from .forms import RegistrationForm


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')  # Redirect to a success page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Ошибка в поле '{field}': {error}")
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    pass

def main(request):
    pass
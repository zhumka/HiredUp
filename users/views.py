from django.contrib.auth import get_user_model, login, authenticate,logout
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from users.models import UserType, JobSeekerProfile, EmployerProfile

User = get_user_model()

def register_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        user_type = request.POST.get('user_type')  # Получаем user_type из POST параметра

        if form.is_valid():
            if user_type not in ['job_seeker', 'employer']:
                messages.error(request, "Пожалуйста, выберите корректный тип пользователя.")
                return render(request, 'users/register.html', {'form': form})

            user = form.save(commit=False)  # Не сохраняем сразу, чтобы добавить user_type
            user.is_active = False  # Деактивируем пользователя до подтверждения
            user.save()

            # Создаем запись в UserType для связи с пользователем
            UserType.objects.create(user=user, user_type=user_type)

            # Создаем профиль в зависимости от типа пользователя
            if user_type == 'job_seeker':
                JobSeekerProfile.objects.create(user=user)  # Создание профиля соискателя
            elif user_type == 'employer':
                EmployerProfile.objects.create(user=user)  # Создание профиля работодателя

            # Отправка письма для активации
            current_site = get_current_site(request)
            email_subject = 'Подтверждение вашего аккаунта'
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()

            return redirect('activation')

    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        return redirect(reverse('login'))
    else:
        messages.error(request, 'Срок действия ссылки истек или произошла ошибка.')
        return redirect('activation_complete')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Используем get вместо прямого доступа
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу или другую
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')

    return render(request, 'users/login.html')



# Страница логаута
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')  # Перенаправление на страницу логина

def activation_view(request):
    return render(request, 'users/activation_complete.html')

def activation_complete_view(request):
    return render(request, 'users/active.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def profile_view(request):
    user_type = request.user.user_type.user_type  # Получаем тип пользователя

    if user_type == 'employer':
        employer_profile = request.user.employer_profile
        return render(request, 'users/profile_employer.html', {'employer_profile': employer_profile})

    elif user_type == 'job_seeker':
        job_seeker_profile = request.user.job_seeker_profile
        return render(request, 'users/profile_jobseeker.html', {'job_seeker_profile': job_seeker_profile})

    else:
        messages.error(request, "Тип пользователя неопределен.")
        return redirect('login')  # Перенаправление на страницу логина, если тип пользователя неопределен


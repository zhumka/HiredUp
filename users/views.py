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
from users.models import UserType  # Добавьте импорт модели UserType

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

            messages.success(request, "Проверьте вашу почту, чтобы активировать ваш аккаунт.")
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
        messages.success(request, "Ваш аккаунт был успешно активирован.")
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
            messages.success(request, 'Вы успешно вошли в систему.')
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


@login_required
def profile_jobseeker_view(request):
    return render(request, 'users/profile_jobseeker.html')

@login_required
def profile_employer_view(request):
    return render(request, 'users/profile_employer.html')

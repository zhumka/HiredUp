from django.contrib.auth import get_user_model, login, authenticate,logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from work.forms import VacancyForm
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, EmployerProfileForm, JobSeekerProfileForm, ResumeForm
from users.models import UserType, JobSeekerProfile, EmployerProfile
from work.models import Application

User = get_user_model()

#Вьюшка регистрации
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


#Вьюшка активации аккаунта
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

#Вьюшка логина
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

#?
def activation_view(request):
    return render(request, 'users/activation_complete.html')
#?
def activation_complete_view(request):
    return render(request, 'users/active.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def profile_view(request):
    user_type = request.user.user_type.user_type  # Получаем тип пользователя

    if user_type == 'employer':
        employer_profile = request.user.employer_profile

        # Пример статистики для работодателя, которую можно будет позже расширить
        total_vacancies = Vacancy.objects.filter(employer=employer_profile).count()
        active_vacancies = Vacancy.objects.filter(employer=employer_profile, is_active=True).count()

        return render(request, 'users/profile_employer.html', {
            'employer_profile': employer_profile,
            'total_vacancies': total_vacancies,
            'active_vacancies': active_vacancies,
        })

    elif user_type == 'job_seeker':
        job_seeker_profile = request.user.job_seeker_profile

        # Проверяем, что поле resume не None
        if job_seeker_profile.resume is not None:
            experience = job_seeker_profile.resume.experience
            if experience is not None:
                if experience == 0:
                    experience_display = "без опыта работы"
                elif experience == 1:
                    experience_display = f"{experience} год"
                elif 2 <= experience % 10 <= 4 and not (11 <= experience % 100 <= 14):
                    experience_display = f"{experience} года"
                else:
                    experience_display = f"{experience} лет"
            else:
                experience_display = "опыт не указан"
        else:
            experience_display = "опыт не указан"

        # Статистика откликов для соискателя
        total_applications = Application.objects.filter(job_seeker=job_seeker_profile).count()
        accepted = Application.objects.filter(job_seeker=job_seeker_profile, status='accepted').count()
        rejected = Application.objects.filter(job_seeker=job_seeker_profile, status='rejected').count()
        pending = Application.objects.filter(job_seeker=job_seeker_profile, status='pending').count()

        # Передаем данные в шаблон
        return render(request, 'users/profile_jobseeker.html', {
            'job_seeker_profile': job_seeker_profile,
            'experience_display': experience_display,
            'total_applications': total_applications,
            'accepted': accepted,
            'rejected': rejected,
            'pending': pending,
        })

    else:
        messages.error(request, "Тип пользователя неопределен.")
        return redirect('login')


#Вьюшка страницы редактирования профилей.
@login_required
def edit_profile_view(request):
    user_type = request.user.user_type.user_type

    if user_type == 'employer':
        employer_profile = get_object_or_404(EmployerProfile, user=request.user)
        if request.method == 'POST':
            form = EmployerProfileForm(request.POST, request.FILES, instance=employer_profile)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = EmployerProfileForm(instance=employer_profile)
        return render(request, 'users/edit_profile_employer.html', {'form': form})

    elif user_type == 'job_seeker':
        job_seeker_profile = get_object_or_404(JobSeekerProfile, user=request.user)
        if request.method == 'POST':
            form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker_profile, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = JobSeekerProfileForm(instance=job_seeker_profile, user=request.user)  # Добавлено user=request.user
        return render(request, 'users/edit_profile_jobseeker.html', {'form': form})

    else:
        messages.error(request, "Тип пользователя неопределен.")
        return redirect('login')


from django.http import JsonResponse
from .models import Profession

#Эта вьюшка нужна для редактирования профиля соискателя, чтобы удобно было выбирать профессию
def load_professions(request):
    category_id = request.GET.get('category_id')
    professions = Profession.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(professions), safe=False)


#Вьюшка страницы редактирования резюме
@login_required
def resume_view(request):
    job_seeker_profile = request.user.job_seeker_profile

    # Если у соискателя уже есть резюме, загружаем его
    if job_seeker_profile.resume:
        form = ResumeForm(instance=job_seeker_profile.resume)
    else:
        form = ResumeForm()

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=job_seeker_profile.resume)
        if form.is_valid():
            resume = form.save(commit=False)  # Не сохраняем сразу
            resume.job_seeker_profile = job_seeker_profile  # Присваиваем резюме профилю соискателя
            resume.save()  # Теперь сохраняем резюме в БД
            job_seeker_profile.resume = resume  # Обновляем поле resume у профиля соискателя
            job_seeker_profile.save()  # Сохраняем профиль соискателя
            return redirect('profile')  # Перенаправление на страницу резюме

    return render(request, 'users/edit_resume.html', {'form': form})

@login_required
def create_vacancy_view(request):
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "Только работодатели могут создавать вакансии")
        return redirect('profile')

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.employer = request.user.employer_profile
            vacancy.save()
            return redirect('profile')
    else:
        form = VacancyForm()

    return render(request, 'users/create_vacancy.html', {'form': form})

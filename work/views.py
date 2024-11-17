from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from hiredup.wsgi import application
from work.models import Vacancy, JobCategory, Application


# Create your views here.
def home_view(request):
    # Получаем все категории профессий
    job_categories = JobCategory.objects.all()

    # Рекомендуемые вакансии (случайно отбираем 5 вакансий)
    recommended_vacancies = Vacancy.objects.filter(is_active=True).order_by('?')[:5]

    return render(request, 'work/home_page.html', {
        'job_categories': job_categories,
        'recommended_vacancies': recommended_vacancies,
    })

def vacancy_detail_view(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    experience = vacancy.experience_required
    if experience == 1:
        experience_display = f"{experience} год"
    elif 2 <= experience % 10 <= 4 and not (11 <= experience % 100 <= 14):
        experience_display = f"{experience} года"
    else:
        experience_display = f"{experience} лет"

    # Выводим данные вакансии на странице
    return render(request, 'work/vacancy_detail.html', {
        'vacancy': vacancy,
        'experience_display': experience_display
    })

@login_required
def apply_to_vacancy(request, vacancy_id):
    # Проверяем, является ли пользователь соискателем
    if request.user.user_type.user_type != 'job_seeker':
        messages.error(request, 'Только соискатели могут откликаться на вакансии.')
        return redirect('home')

    # Получаем вакансию
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    job_seeker_profile = request.user.job_seeker_profile

    # Проверяем, есть ли уже отклик на эту вакансию
    existing_application = Application.objects.filter(vacancy=vacancy, job_seeker=job_seeker_profile).first()

    if existing_application:
        messages.info(request, 'Вы уже откликнулись на эту вакансию.')
        return redirect('vacancy_detail', vacancy_id=vacancy.id)

    # Проверяем, есть ли у соискателя резюме
    if not job_seeker_profile.resume:
        messages.error(request, 'У вас нет резюме. Пожалуйста, добавьте резюме в свой профиль.')
        return redirect('edit_resume')

    # Создаем отклик на вакансию
    application = Application.objects.create(
        vacancy=vacancy,
        job_seeker=job_seeker_profile,
        created_at=timezone.now()
    )

    # Сообщение после успешного отклика
    messages.success(request, 'Вы успешно откликнулись на вакансию.')

    return redirect('vacancy_detail', vacancy_id=vacancy.id)

@login_required
def applications_view(request):
    if request.user.user_type.user_type == 'employer':
        employer_profile = request.user.employer_profile
        vacancies = Vacancy.objects.filter(employer=employer_profile)
        applications = Application.objects.filter(vacancy__in=vacancies)
        return render(request, 'work/applications_employer.html', {'applications': applications})
    elif request.user.user_type.user_type == 'job_seeker':
        job_seeker_profile = request.user.job_seeker_profile
        applications = Application.objects.filter(job_seeker=job_seeker_profile)
        return render(request, 'work/applications_job_seeker.html', {'applications': applications})
    else:
        return redirect('home')


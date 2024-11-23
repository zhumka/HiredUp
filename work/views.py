from django.http import HttpResponseRedirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django_filters.views import FilterView

from hiredup.wsgi import application
from work.models import Vacancy, JobCategory, Application
from .filters import VacancyFilter


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

@login_required
def application_detail_view(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    is_employer = request.user.user_type.user_type == 'employer'
    is_job_seeker = request.user.user_type.user_type == 'job_seeker'

    if is_employer:
        if application.vacancy.employer != request.user.employer_profile:
            return redirect('home')

        return render(request, 'work/application_detail.html', {
            'application': application,
            'vacancy': application.vacancy,
            'job_seeker':application.job_seeker,
            'is_employer': is_employer,
        })

    if is_job_seeker:
        return redirect('vacancy_detail', vacancy_id=application.vacancy.id)
    return redirect('home')

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Application

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Проверяем, что пользователь - работодатель
    if request.user.user_type.user_type != 'employer':
        return redirect('home')

    # Проверяем, что вакансия принадлежит работодателю, который делает запрос
    if application.vacancy.employer != request.user.employer_profile:
        return redirect('home')

    if request.method == 'POST':
        status = request.POST.get('status')

        if status in dict(Application.STATUS_CHOICES):
            # Если отклик уже принят или отклонен, блокируем возможность изменений
            if application.status in ['accepted', 'rejected']:
                messages.error(request, "Статус заявки уже был изменен. Невозможно повторно изменить статус.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # Если отклик принят, меняем статус вакансии на неактивный
            if status == 'accepted':
                application.vacancy.is_active = False
                application.vacancy.save()

            # Обновляем статус отклика
            application.status = status
            application.save()

            messages.success(request, f"Статус заявки изменен на {application.get_status_display()}")
        else:
            messages.error(request, "Недействительный статус.")

        # Перенаправляем обратно на страницу, с которой пришел запрос
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class VacancySearchView(FilterView):
    model = Vacancy
    template_name = 'work/search_results.html'
    filterset_class = VacancyFilter
    context_object_name = 'vacancies'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()

        # Если фильтры пустые, показывать только активные вакансии случайным образом
        if not self.request.GET:
            return queryset.filter(is_active=True).order_by('?')  # Сортировка активных вакансий случайным образом

        return queryset
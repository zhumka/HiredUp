from django.http import HttpResponseRedirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django_filters.views import FilterView

from hiredup.wsgi import application
from users.models import JobSeekerProfile
from work.models import Vacancy, JobCategory, Application
from .filters import VacancyFilter
from .forms import VacancyForm


def home_view(request):
    # Получаем все категории профессий
    job_categories = JobCategory.objects.all()

    # Рекомендованные вакансии (случайно выбираем 5 вакансий)
    recommended_vacancies = Vacancy.objects.filter(is_active=True).order_by('?')[:5]

    # Персонализированные вакансии для соискателей
    personalized_vacancies = []
    if request.user.is_authenticated and hasattr(request.user, 'job_seeker_profile'):
        # Обновляем профиль из базы
        job_seeker_profile = JobSeekerProfile.objects.select_related('profession').get(user=request.user)
        if job_seeker_profile.profession and job_seeker_profile.profession.category:
            personalized_vacancies = Vacancy.objects.filter(
                category=job_seeker_profile.profession.category,
                is_active=True
            ).order_by('?')[:5]

    # Рекомендации для работодателей (например, по популярным категориям)
    employer_recommended_vacancies = []
    if request.user.is_authenticated and hasattr(request.user, 'employer_profile'):
        # Рекомендуем вакансии по популярным категориям
        employer_recommended_vacancies = Vacancy.objects.filter(is_active=True).order_by('?')[:5]

    return render(request, 'work/home_page.html', {
        'job_categories': job_categories,
        'recommended_vacancies': recommended_vacancies,
        'personalized_vacancies': personalized_vacancies,
        'employer_recommended_vacancies': employer_recommended_vacancies,
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

from django.db.models import Q

class VacancySearchView(FilterView):
    model = Vacancy
    template_name = 'work/search_results.html'
    filterset_class = VacancyFilter
    context_object_name = 'vacancies'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по полю 'q', если оно передано в запросе
        query = self.request.GET.get('q', '')  # Получаем строку запроса по ключу 'q'
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(requirements__icontains=query))

        # Фильтрация вакансий по статусу активности
        queryset = queryset.filter(is_active=True)

        return queryset

@login_required
def edit_vacancy_view(request, vacancy_id):
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        messages.error(request, "Вакансия не найдена.")
        return redirect('profile')

    # Проверка, что пользователь является владельцем вакансии
    if vacancy.employer != request.user.employer_profile:
        messages.error(request, "Вы не можете редактировать эту вакансию.")
        return redirect('profile')

    if request.method == 'POST':
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            messages.success(request, "Вакансия успешно обновлена.")
            return redirect('profile')
    else:
        form = VacancyForm(instance=vacancy)

    return render(request, 'work/edit_vacancy.html', {'form': form, 'vacancy': vacancy})

@login_required
def employer_vacancies_view(request):
    if not hasattr(request.user, 'employer_profile'):
        messages.error(request, "Только работодатели могут просматривать вакансии")
        return redirect('profile')

    vacancies = Vacancy.objects.filter(employer=request.user.employer_profile)
    return render(request, 'work/employer_vacancies.html', {'vacancies': vacancies})

from django.shortcuts import render

from work.models import Vacancy, JobCategory


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

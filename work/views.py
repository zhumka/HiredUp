from django.shortcuts import render, get_object_or_404

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
import django_filters
from .models import Vacancy, JobCategory


class VacancyFilter(django_filters.FilterSet):
    salary_min = django_filters.NumberFilter(field_name='salary_min',lookup_expr='gte',label='Мин. зарплата')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte',label='Макс. зарпалата')
    experience_required = django_filters.NumberFilter(field_name='experience_required', lookup_expr='lte',label='Требуемый опыт')
    category = django_filters.ModelChoiceFilter(queryset=JobCategory.objects.all(), label='Категория')
    job_type = django_filters.ChoiceFilter(choices=Vacancy.JOB_TYPES, label='Тип работы')

    search = django_filters.CharFilter(method='filter_by_search', label='Ключевые слова')

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value)

    class Meta:
        model = Vacancy
        fields = ['search','salary_min', 'salary_max', 'experience_required', 'category', 'job_type']
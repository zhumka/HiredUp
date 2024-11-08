from django import forms
from .models import Vacancy

class VacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = [
            'title', 'requirements', 'responsibilities',
            'salary_min', 'salary_max', 'experience_required',
            'category', 'profession', 'location', 'job_type', 'is_active'
        ]

        # Кастомное поле для is_active, отображаемое как радиокнопки
        is_active = forms.BooleanField(
            required=False,
            widget=forms.RadioSelect(choices=[(True, 'Активная'), (False, 'Не активная')])
        )
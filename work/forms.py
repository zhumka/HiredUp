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

    # Кастомное поле для is_active с радиокнопками
    is_active = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Активная'), (False, 'Не активная')])
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Это создание новой вакансии
            self.fields['is_active'].initial = True  # Значение по умолчанию для новой вакансии
            self.fields['is_active'].widget = forms.HiddenInput()  # Скрыть поле для создания
        else:  # Это редактирование вакансии
            self.fields['is_active'].initial = self.instance.is_active  # Установить текущее значение для редактирования







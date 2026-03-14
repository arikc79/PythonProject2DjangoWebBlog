from django import forms
from django.core.exceptions import ValidationError
from workers.models import Worker, Resume, Contact


class WorkCreateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['name',
                  'salary',
                  'notes',
                  'photo']

        labels = {'name': "Ім'я",
                  'salary': 'Зарплата',
                  'notes': 'Примітки',
                  'photo': 'Фото',

                  }

        help_texts = {'name': "Введіть ім'я працівника",
                      'salary': 'Введіть зарплату працівника',
                      'notes': 'Додайте примітки про працівника',
                      'photo': 'Завантажте фото працівника (необов\'язково)',}

        widgets = {'name': forms.TextInput(attrs={'placeholder': 'Введіть ім\'я працівника',
                                                  'class': 'form-control'}),
                   'salary': forms.NumberInput(attrs={'min': 0,
                                                      'step': 0.01,
                                                      'class': 'form-control'}),
                   'notes': forms.Textarea(
                       attrs={'placeholder': 'Додайте примітки про працівника',
                              'class': 'form-control',
                              'rows': 4}),
                   'photo': forms.ClearableFileInput(attrs={'class': 'form-control',
                                                            'accept': 'image/*'}),}

    def clean_name(self):
        name = self.cleaned_data.get('name')

        words = name.split()

        if len(words) != 2:
            raise ValidationError(
                "Ім'я повинно складатися рівно з 2 слів (наприклад: Іван Петров)",
                code='invalid_word_count'
            )

        for word in words:
            if len(word) < 3:
                raise ValidationError(
                    'Кожне слово повинно містити хоча б 3 літери',
                    code='word_too_short'
                )

        if any(char.isdigit() for char in name):
            raise ValidationError(
                "Ім'я не повинно містити цифри",
                code='contains_digits'
            )

        return name


class WorkerSearchForm(forms.Form):
    name = forms.CharField(label="ім'я", required=False, widget=forms.TextInput(
        attrs={'placeholder': "Пошук за ім'ям", 'class': 'form-control search-input'}), )
    min_salary = forms.DecimalField(label='мінімальна зарплата', required=False, widget=forms.NumberInput(
        attrs={'min': 0, 'step': 0.01, 'class': 'form-control search-input', 'placeholder': 'Зарплата від...'}), )
    max_salary = forms.DecimalField(label='максимальна зарплата', required=False, widget=forms.NumberInput(
        attrs={'min': 0, 'step': 0.01, 'class': 'form-control search-input', 'placeholder': 'Зарплата до...'}), )

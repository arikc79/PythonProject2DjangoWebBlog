from django import forms
from django.core.exceptions import ValidationError
from workers.models import Worker, Resume, Contact


class WorkCreateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'salary', 'notes']

        labels = {'name': "Ім'я", 'salary': 'Зарплата', 'notes': 'Примітки',

                  }

        help_texts = {'name': "Введіть ім'я працівника", 'salary': 'Введіть зарплату працівника',
                      'notes': 'Додайте примітки про працівника', }

        widgets = {'name': forms.TextInput(attrs={'placeholder': 'Введіть ім\'я працівника', 'class': 'form-control'}),
                   'salary': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
                   'notes': forms.Textarea(
                       attrs={'placeholder': 'Додайте примітки про працівника', 'class': 'form-control', 'rows': 4}), }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        words = name.split()

        if len(words) != 2:
            raise ValidationError("Ім'я повинно складатися рівно з 2 слів (наприклад: Іван Петров)")

        for word in words:
            if len(word) < 3:
                raise ValidationError('Кожне слово повинно містити хоча б 3 літери')

        if any(char.isdigit() for char in name):
            raise ValidationError("Ім'я не повинно містити цифри")

        return name


class WorkerSearchForm(forms.Form):
    name = forms.CharField(label="ім'я", required=False, widget=forms.TextInput(
        attrs={'placeholder': "Пошук за ім'ям", 'class': 'form-control search-input'}), )
    min_salary = forms.DecimalField(label='мінімальна зарплата', required=False, widget=forms.NumberInput(
        attrs={'min': 0, 'step': 0.01, 'class': 'form-control search-input', 'placeholder': 'Зарплата від...'}), )
    max_salary = forms.DecimalField(label='максимальна зарплата', required=False, widget=forms.NumberInput(
        attrs={'min': 0, 'step': 0.01, 'class': 'form-control search-input', 'placeholder': 'Зарплата до...'}), )

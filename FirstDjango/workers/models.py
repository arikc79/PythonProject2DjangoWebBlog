from django.db import models


# Create your models here.
class Worker(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    salary = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} {self.name.upper()}) - {self.salary} грн.'


class Resume(models.Model):
    # worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='resumes')
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    discription = models.TextField()

    def __str__(self):
        return f'Resume  {self.worker.name.upper()}'


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Телефон'),
        ('telegram', 'Telegram'),

    ]

    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='contacts')
    type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.worker.name} - {self.get_type_display()}: {self.value}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакти'

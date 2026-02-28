from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from workers.models import Worker, Resume, Contact


# Create your views here.
# def all_workers_view(request):
#
#     context = {
#
#         'workers': Worker.objects.all()
#     }
#
#     return render(request, 'workers/workers_all.html', context)

class WorkersListView(ListView):
    model = Worker
    template_name = 'workers/workers_all.html'
    context_object_name = 'workers'


class WorkerDetailView(DetailView):
    model = Worker
    template_name = 'workers/worker_detail.html'
    context_object_name = 'worker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Деталі: {self.object.name}'
        return context


class WorkerCreateView(CreateView):
    model = Worker
    template_name = 'workers/worker_form.html'
    fields = ['name', 'salary', 'notes']

    def get_success_url(self):
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додати працівника'
        return context


class WorkerUpdateView(UpdateView):
    model = Worker
    template_name = 'workers/worker_form.html'
    fields = ['name', 'salary', 'notes']

    def get_success_url(self):
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редагувати працівника'
        return context


class WorkerDeleteView(DeleteView):
    model = Worker
    template_name = 'workers/worker_confirm_delete.html'
    success_url = reverse_lazy('all_workers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Видалити працівника'
        return context


class ResumeCreateView(CreateView):
    model = Resume
    template_name = 'workers/resume_form.html'
    fields = ['discription']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Створити резюме'
        context['worker'] = get_object_or_404(Worker, pk=self.kwargs['worker_pk'])
        return context

    def form_valid(self, form):
        form.instance.worker_id = self.kwargs['worker_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.worker.pk})


class ResumeUpdateView(UpdateView):
    model = Resume
    template_name = 'workers/resume_form.html'
    fields = ['discription']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редагувати резюме'
        context['worker'] = self.object.worker
        return context

    def get_success_url(self):
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.worker.pk})


class ResumeDeleteView(DeleteView):
    """View для видалення резюме робітника"""
    model = Resume
    template_name = 'workers/resume_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Видалити резюме'
        context['worker'] = self.object.worker
        return context

    def get_success_url(self):
        """Повертаємся на сторінку деталей робітника"""
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.worker.pk})


class ContactCreateView(CreateView):
    """View для створення контакту робітника"""
    model = Contact
    template_name = 'workers/contact_form.html'
    fields = ['type', 'value']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додати контакт'
        context['worker'] = get_object_or_404(Worker, pk=self.kwargs['worker_pk'])
        return context

    def form_valid(self, form):
        """Привʼязуємо контакт до робітника"""
        form.instance.worker_id = self.kwargs['worker_pk']
        return super().form_valid(form)

    def get_success_url(self):
        """Повертаємся на сторінку деталей робітника"""
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.worker.pk})

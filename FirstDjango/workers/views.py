from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404

from workers.models import Worker, Resume, Contact

from workers.forms import WorkCreateForm, WorkerSearchForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаємо пусту форму для потенційного локального пошуку
        context['search_form'] = WorkerSearchForm()
        return context


class WorkerDetailView(DetailView):
    model = Worker
    template_name = 'workers/worker_detail.html'
    context_object_name = 'worker'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Деталі: {self.object.name}'
        return context


class WorkerCreateView(LoginRequiredMixin, CreateView):
    # 1
    # model = Worker
    # fields = ['name', 'salary', 'notes']

    # 2
    model = Worker
    form_class = WorkCreateForm

    template_name = 'workers/worker_form.html'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додати працівника'
        return context


class WorkerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Worker
    template_name = 'workers/worker_form.html'
    fields = ['name', 'salary', 'notes']
    login_url = '/login/'

    def test_func(self):
        # ADMIN може редагувати всіх, звичайний користувач - тільки свого
        if self.request.user.is_superuser:
            return True
        # Перевіряємо чи це власник робітника
        return self.object.owner == self.request.user

    def get_success_url(self):
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редагувати працівника'
        return context


class WorkerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Worker
    template_name = 'workers/worker_confirm_delete.html'
    success_url = reverse_lazy('all_workers')
    login_url = '/login/'

    def test_func(self):
        # ADMIN може видаляти всіх, звичайний користувач - тільки свого
        if self.request.user.is_superuser:
            return True
        # Перевіряємо чи це власник робітника
        return self.object.owner == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Видалити працівника'
        return context


class ResumeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Resume
    template_name = 'workers/resume_form.html'
    fields = ['discription']
    login_url = '/login/'

    def test_func(self):
        # Тільки ADMIN (superuser) може створювати резюме
        return self.request.user.is_superuser

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


class ResumeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resume
    template_name = 'workers/resume_form.html'
    fields = ['discription']
    login_url = '/login/'

    def test_func(self):
        # Тільки ADMIN (superuser) може редагувати резюме
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редагувати резюме'
        context['worker'] = self.object.worker
        return context

    def get_success_url(self):
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.worker.pk})


class ResumeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View для видалення резюме робітника"""
    model = Resume
    template_name = 'workers/resume_confirm_delete.html'
    login_url = '/login/'

    def test_func(self):
        # Тільки ADMIN (superuser) може видаляти резюме
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Видалити резюме'
        context['worker'] = self.object.worker
        return context

    def get_success_url(self):
        """Повертаємся на сторінку деталей робітника"""
        return reverse_lazy('worker_detail', kwargs={'pk': self.object.worker.pk})


class ContactCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View для створення контакту робітника"""
    model = Contact
    template_name = 'workers/contact_form.html'
    fields = ['type', 'value']
    login_url = '/login/'

    def test_func(self):
        # Тільки ADMIN (superuser) може додавати контакти
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додати контакт'
        context['worker'] = get_object_or_404(Worker, pk=self.kwargs['worker_pk'])
        return context

    def form_valid(self, form):

        form.instance.worker_id = self.kwargs['worker_pk']
        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy('worker_detail', kwargs={'pk': self.object.worker.pk})


class WorkerSearchView(ListView):
    model = Worker
    template_name = 'workers/worker_search.html'
    context_object_name = 'workers'
    paginate_by = 10

    def get_queryset(self):
        # Якщо нема GET параметрів - повертаємо пустий список
        if not self.request.GET:
            return Worker.objects.none()

        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            # Пошук по імені
            name_query = form.cleaned_data.get('name', '').strip()
            if name_query:
                queryset = queryset.filter(name__icontains=name_query)

            # Пошук по мінімальній зарплаті
            min_salary = form.cleaned_data.get('min_salary')
            if min_salary:
                queryset = queryset.filter(salary__gte=min_salary)

            # Пошук по максимальній зарплаті
            max_salary = form.cleaned_data.get('max_salary')
            if max_salary:
                queryset = queryset.filter(salary__lte=max_salary)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаємо форму в шаблон для повторного відображення
        context['search_form'] = WorkerSearchForm(self.request.GET)
        context['title'] = 'Пошук працівників'
        # Додаємо флаг - чи виконувався пошук
        context['is_searched'] = bool(self.request.GET)
        return context


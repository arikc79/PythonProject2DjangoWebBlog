from django.shortcuts import render, redirect, get_object_or_404
from workers.models import Worker
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy


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


class WorkerUpdateView(UpdateView):
    model = Worker
    template_name = 'workers/worker_form.html'
    fields = ['name', 'salary', 'notes']
    success_url = reverse_lazy('all_workers')

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

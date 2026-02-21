from django.shortcuts import render
from workers.models import Worker


# Create your views here.
def all_workers_view(request):

    context = {

        'workers': Worker.objects.all()
    }

    return render(request, 'workers/workers_all.html', context)

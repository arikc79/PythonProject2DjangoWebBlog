from .models import Worker


def worker_count(request):
    context = {
        'worker_count': Worker.objects.count()

    }
    return context

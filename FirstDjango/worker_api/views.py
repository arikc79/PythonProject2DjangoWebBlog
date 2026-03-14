from rest_framework.decorators import api_view
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from workers.models import Resume, Worker

from .serializers import ResumeSerializer, WorkerSerializer


@api_view(["GET"])
def ping(request):
    return Response({"status": "ok", "service": "worker_api"})


class IsHRPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name="HR").exists()


class WorkerViewSet(ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class ResumeViewSet(ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsHRPermission]


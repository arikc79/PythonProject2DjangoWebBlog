from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ResumeViewSet, WorkerViewSet, ping

router = DefaultRouter()
router.register("workers", WorkerViewSet)
router.register("resumes", ResumeViewSet)

urlpatterns = [
    path("ping/", ping, name="worker-api-ping"),
    path("", include(router.urls)),

    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),


]

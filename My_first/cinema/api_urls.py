from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cinema.api_views import (
    CinemaStatsAPIView,
    FavoriteMovieViewSet,
    MovieViewSet,
    ReviewViewSet,
    SessionViewSet,
    TicketBookingViewSet,
    UserProfileViewSet,
)

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('sessions', SessionViewSet)
router.register('reviews', ReviewViewSet)
router.register('profiles', UserProfileViewSet)
router.register('favorites', FavoriteMovieViewSet)
router.register('bookings', TicketBookingViewSet)

urlpatterns = [
    path('stats/', CinemaStatsAPIView.as_view(), name='cinema-stats'),
    path('', include(router.urls)),
]


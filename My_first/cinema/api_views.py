from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import FavoriteMovie, Movie, Review, Session, TicketBooking, UserProfile
from cinema.serializers import (
    FavoriteMovieSerializer,
    MovieSerializer,
    ReviewSerializer,
    SessionSerializer,
    TicketBookingSerializer,
    UserProfileSerializer,
)


class BaseCinemaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MovieViewSet(BaseCinemaViewSet):
    queryset = Movie.objects.all().order_by('-created_at')
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()

        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)

        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(year=year)

        title = (self.request.query_params.get('title') or '').strip()
        if title:
            title_casefold = title.casefold()
            matched_ids = [
                movie.id
                for movie in queryset.only('id', 'title')
                if title_casefold in (movie.title or '').casefold()
            ]
            queryset = queryset.filter(id__in=matched_ids)

        return queryset.order_by('-created_at')


class SessionViewSet(BaseCinemaViewSet):
    queryset = Session.objects.select_related('movie').all().order_by('date')
    serializer_class = SessionSerializer


class ReviewViewSet(BaseCinemaViewSet):
    queryset = Review.objects.select_related('movie', 'user').all().order_by('-created_at')
    serializer_class = ReviewSerializer


class UserProfileViewSet(BaseCinemaViewSet):
    queryset = UserProfile.objects.select_related('user').all().order_by('user__username')
    serializer_class = UserProfileSerializer


class FavoriteMovieViewSet(BaseCinemaViewSet):
    queryset = FavoriteMovie.objects.select_related('movie', 'user').all().order_by('-created_at')
    serializer_class = FavoriteMovieSerializer


class TicketBookingViewSet(BaseCinemaViewSet):
    queryset = TicketBooking.objects.select_related('session', 'session__movie', 'user').all().order_by('-created_at')
    serializer_class = TicketBookingSerializer


class CinemaStatsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        average_rating = Review.objects.aggregate(average_rating=Avg('rating')).get('average_rating') or 0
        data = {
            'average_rating': round(average_rating, 1),
            'users_count': User.objects.count(),
            'movies_count': Movie.objects.count(),
        }
        return Response(data)

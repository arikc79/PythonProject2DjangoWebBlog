from django.urls import path
from cinema.views import (
    MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, MovieDeleteView,
    SessionListView, SessionCreateView, SessionDeleteView,
    UserProfileDetailView, ReviewUpdateView, ReviewDeleteView,
    book_session, cancel_booking, mark_booking_watched, toggle_favorite, FavoriteListView
)

urlpatterns = [
    # Movie URLs
    path('', MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movie/<int:pk>/edit/', MovieUpdateView.as_view(), name='movie_edit'),
    path('movie/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),

    # Session URLs
    path('sessions/', SessionListView.as_view(), name='session_list'),
    path('session/create/', SessionCreateView.as_view(), name='session_create'),
    path('movie/<int:movie_id>/session/create/', SessionCreateView.as_view(), name='session_create_for_movie'),
    path('session/<int:pk>/delete/', SessionDeleteView.as_view(), name='session_delete'),

    # Review URLs
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),

    # User profile URLs
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile_detail'),

    # Booking URLs
    path('session/<int:pk>/book/', book_session, name='book_session'),
    path('booking/<int:pk>/cancel/', cancel_booking, name='cancel_booking'),
    path('booking/<int:pk>/watched/', mark_booking_watched, name='mark_booking_watched'),

    # Favorite URLs
    path('movie/<int:pk>/favorite/', toggle_favorite, name='toggle_favorite'),
    path('favorites/', FavoriteListView.as_view(), name='favorite_list'),
]

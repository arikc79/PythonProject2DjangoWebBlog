from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from cinema.models import FavoriteMovie, Movie, Review, Session, TicketBooking, UserProfile


class CinemaModelTests(TestCase):
    def setUp(self):
        self.movie1 = Movie.objects.create(
            title='Movie One',
            description='Desc',
            year=2024,
            duration=120,
            genre='drama',
        )
        self.movie2 = Movie.objects.create(
            title='Movie Two',
            description='Desc 2',
            year=2023,
            duration=110,
            genre='comedy',
        )

    def test_session_conflict_in_same_hall_and_datetime(self):
        start = timezone.now() + timedelta(days=1)
        Session.objects.create(movie=self.movie1, date=start, hall_number=1, max_tickets=50)
        conflict = Session(movie=self.movie2, date=start, hall_number=1, max_tickets=50)

        with self.assertRaises(ValidationError):
            conflict.full_clean()

    def test_session_conflict_when_time_intervals_overlap(self):
        start = timezone.now() + timedelta(days=2)
        long_movie = Movie.objects.create(
            title='Long Movie',
            description='Long',
            year=2024,
            duration=130,
            genre='drama',
        )
        short_movie = Movie.objects.create(
            title='Short Movie',
            description='Short',
            year=2024,
            duration=90,
            genre='action',
        )

        Session.objects.create(movie=long_movie, date=start, hall_number=3, max_tickets=50)
        overlapping = Session(
            movie=short_movie,
            date=start + timedelta(minutes=60),
            hall_number=3,
            max_tickets=50,
        )

        with self.assertRaises(ValidationError):
            overlapping.full_clean()

    def test_session_allowed_when_starts_after_previous_end(self):
        start = timezone.now() + timedelta(days=3)
        long_movie = Movie.objects.create(
            title='Long Movie 2',
            description='Long 2',
            year=2024,
            duration=130,
            genre='drama',
        )
        short_movie = Movie.objects.create(
            title='Short Movie 2',
            description='Short 2',
            year=2024,
            duration=90,
            genre='action',
        )

        Session.objects.create(movie=long_movie, date=start, hall_number=4, max_tickets=50)
        not_overlapping = Session(
            movie=short_movie,
            date=start + timedelta(minutes=130),
            hall_number=4,
            max_tickets=50,
        )

        not_overlapping.full_clean()

    def test_booking_cannot_exceed_capacity(self):
        start = timezone.now() + timedelta(days=1)
        session = Session.objects.create(movie=self.movie1, date=start, hall_number=2, max_tickets=3)
        u1 = User.objects.create_user(username='u1', password='pass12345')
        u2 = User.objects.create_user(username='u2', password='pass12345')

        TicketBooking.objects.create(session=session, user=u1, tickets_count=2)
        overbook = TicketBooking(session=session, user=u2, tickets_count=2)

        with self.assertRaises(ValidationError):
            overbook.full_clean()


class ProfileAndFavoriteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='client', password='pass12345')
        self.movie = Movie.objects.create(
            title='Movie Fav',
            description='Fav desc',
            year=2022,
            duration=100,
            genre='action',
        )

    def test_profile_created_by_signal(self):
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_toggle_favorite_adds_movie(self):
        self.client.login(username='client', password='pass12345')
        response = self.client.post(
            reverse('toggle_favorite', kwargs={'pk': self.movie.pk}),
            {'next': reverse('movie_list')}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(FavoriteMovie.objects.filter(user=self.user, movie=self.movie).exists())

    def test_mark_booking_as_watched(self):
        session = Session.objects.create(
            movie=self.movie,
            date=timezone.now() - timedelta(hours=2),
            hall_number=5,
            max_tickets=20,
        )
        booking = TicketBooking.objects.create(session=session, user=self.user, tickets_count=1)

        self.client.login(username='client', password='pass12345')
        response = self.client.post(
            reverse('mark_booking_watched', kwargs={'pk': booking.pk}),
            {'next': reverse('session_list')}
        )

        booking.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(booking.is_watched)
        self.assertIsNotNone(booking.watched_at)

    def test_can_mark_future_booking_as_watched(self):
        session = Session.objects.create(
            movie=self.movie,
            date=timezone.now() + timedelta(hours=3),
            hall_number=6,
            max_tickets=20,
        )
        booking = TicketBooking.objects.create(session=session, user=self.user, tickets_count=1)

        self.client.login(username='client', password='pass12345')
        response = self.client.post(
            reverse('mark_booking_watched', kwargs={'pk': booking.pk}),
            {'next': reverse('session_list')}
        )

        booking.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(booking.is_watched)
        self.assertIsNotNone(booking.watched_at)


class CinemaApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='api_user', password='pass12345')
        self.movie = Movie.objects.create(
            title='API Movie',
            description='API Desc',
            year=2024,
            duration=115,
            genre='action',
        )
        self.session = Session.objects.create(
            movie=self.movie,
            date=timezone.now() + timedelta(days=1),
            hall_number=7,
            max_tickets=40,
        )
        Review.objects.create(
            movie=self.movie,
            user=self.user,
            text='Чудовий фільм',
            rating=8,
        )
        FavoriteMovie.objects.create(user=self.user, movie=self.movie)
        TicketBooking.objects.create(session=self.session, user=self.user, tickets_count=2)

    def test_api_movie_search_is_case_insensitive_and_partial(self):
        Movie.objects.create(
            title='Темний Лицар',
            description='Batman movie',
            year=2008,
            duration=152,
            genre='action',
        )
        Movie.objects.create(
            title='Комедія вечора',
            description='Comedy movie',
            year=2020,
            duration=100,
            genre='comedy',
        )

        response = self.client.get('/api/movies/?title=лиц')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_titles = [item['title'] for item in response.data]
        self.assertIn('Темний Лицар', returned_titles)
        self.assertNotIn('Комедія вечора', returned_titles)

    def test_api_root_contains_registered_routes(self):
        response = self.client.get('/api/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('movies', response.data)
        self.assertIn('sessions', response.data)
        self.assertIn('reviews', response.data)
        self.assertIn('profiles', response.data)
        self.assertIn('favorites', response.data)
        self.assertIn('bookings', response.data)

    def test_all_main_viewsets_are_available(self):
        endpoints = [
            '/api/movies/',
            '/api/sessions/',
            '/api/reviews/',
            '/api/profiles/',
            '/api/favorites/',
            '/api/bookings/',
        ]

        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, status.HTTP_200_OK, endpoint)

    def test_can_create_review_via_api_viewset(self):
        other_user = User.objects.create_user(username='reviewer', password='pass12345')
        other_movie = Movie.objects.create(
            title='Another Movie',
            description='Another Desc',
            year=2025,
            duration=90,
            genre='comedy',
        )
        self.client.force_authenticate(user=other_user)

        response = self.client.post(
            '/api/reviews/',
            {
                'movie': other_movie.pk,
                'text': 'API review',
                'rating': 9,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Review.objects.filter(user=other_user, movie=other_movie, rating=9).exists())

    def test_stats_api_returns_expected_aggregates(self):
        User.objects.create_user(username='stats_user', password='pass12345')
        Movie.objects.create(
            title='Stats Movie',
            description='Stats Desc',
            year=2021,
            duration=100,
            genre='drama',
        )

        response = self.client.get('/api/stats/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], 8.0)
        self.assertEqual(response.data['users_count'], 2)
        self.assertEqual(response.data['movies_count'], 2)

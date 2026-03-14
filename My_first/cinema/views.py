from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from cinema.forms import MovieForm, SessionForm, ReviewForm, TicketBookingForm, UserProfileForm
from cinema.models import Movie, Session, Review, TicketBooking, FavoriteMovie, UserProfile


# ================== MIXINS =================

class WorkerRequiredMixin(UserPassesTestMixin):
    """Перевіряє, чи користувач належить до групи 'Робітник'"""
    def test_func(self):
        return self.request.user.groups.filter(name='Робітник').exists() or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('movie_list')


class OwnerOrWorkerRequiredMixin(UserPassesTestMixin):
    """Перевіряє, чи користувач є автором або робітником"""
    def test_func(self):
        review = self.get_object()
        return (review.user == self.request.user or
                self.request.user.groups.filter(name='Робітник').exists() or
                self.request.user.is_superuser)


def register_view(request):
    """Реєстрація нового користувача"""
    if request.user.is_authenticated:
        return redirect('movie_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Реєстрація успішна. Тепер увійдіть у свій акаунт.')
            return redirect('login')
    else:
        form = UserCreationForm()

    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'registration/register.html', {'form': form})


# ================== MOVIE VIEWS ==================

class MovieListView(ListView):
    """Перегляд всіх фільмів з можливістю пошуку"""
    model = Movie
    template_name = 'cinema/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        """Фільтруємо фільми по пошуковим параметрам"""
        queryset = Movie.objects.all()

        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)

        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(year=year)

        title = (self.request.GET.get('title') or '').strip()
        if title:
            title_casefold = title.casefold()
            matched_ids = [
                movie.id
                for movie in queryset.only('id', 'title')
                if title_casefold in (movie.title or '').casefold()
            ]
            queryset = queryset.filter(id__in=matched_ids)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Movie.GENRE_CHOICES
        context['search_title'] = self.request.GET.get('title', '')
        context['search_genre'] = self.request.GET.get('genre', '')
        context['search_year'] = self.request.GET.get('year', '')

        if self.request.user.is_authenticated:
            favorite_ids = FavoriteMovie.objects.filter(user=self.request.user).values_list('movie_id', flat=True)
            context['favorite_movie_ids'] = set(favorite_ids)
        else:
            context['favorite_movie_ids'] = set()

        return context


class MovieDetailView(DetailView):
    """Детальна інформація про фільм"""
    model = Movie
    template_name = 'cinema/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessions'] = self.object.sessions.filter(
            date__gte=timezone.now()
        ).order_by('date')[:5]
        context['reviews'] = self.object.reviews.select_related('user', 'user__profile').all()
        context['average_rating'] = self.object.average_rating()

        context['can_edit_movie'] = (
            self.request.user.is_superuser or
            self.request.user.groups.filter(name='Робітник').exists()
        )

        if self.request.user.is_authenticated:
            user_review = self.object.reviews.filter(user=self.request.user).first()
            context['user_review'] = user_review
            context['is_favorite'] = FavoriteMovie.objects.filter(user=self.request.user, movie=self.object).exists()
            if not user_review:
                context['review_form'] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        """Обробка додавання/редагування відгуку"""
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        existing_review = self.object.reviews.filter(user=request.user).first()
        form = ReviewForm(request.POST, instance=existing_review)

        if form.is_valid():
            review = form.save(commit=False)
            review.movie = self.object
            review.user = request.user
            review.save()
            return redirect('movie_detail', pk=self.object.pk)

        context = self.get_context_data()
        context['review_form'] = form
        return render(request, self.template_name, context)


class MovieCreateView(WorkerRequiredMixin, CreateView):
    """Створення нового фільму - тільки для робітників"""
    model = Movie
    form_class = MovieForm
    template_name = 'cinema/movie_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додати фільм'
        context['button_text'] = 'Створити фільм'
        return context


class MovieUpdateView(WorkerRequiredMixin, UpdateView):
    """Редагування фільму - тільки для робітників"""
    model = Movie
    form_class = MovieForm
    template_name = 'cinema/movie_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редагувати: {self.object.title}'
        context['button_text'] = 'Зберегти зміни'
        return context


class MovieDeleteView(WorkerRequiredMixin, DeleteView):
    """Видалення фільму - тільки для робітників"""
    model = Movie
    template_name = 'cinema/movie_confirm_delete.html'
    success_url = reverse_lazy('movie_list')


# ================== SESSION VIEWS ==================

class SessionListView(ListView):
    """Перегляд всіх найближчих сеансів"""
    model = Session
    template_name = 'cinema/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        now = timezone.now()
        queryset = Session.objects.select_related('movie')

        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(date__gte=now) | Q(bookings__user=self.request.user)
            ).distinct()
        else:
            queryset = queryset.filter(date__gte=now)

        return queryset.order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Всі сеанси'
        context['now'] = timezone.now()
        context['can_manage_sessions'] = (
            self.request.user.is_superuser or
            self.request.user.groups.filter(name='Робітник').exists()
        )

        if self.request.user.is_authenticated:
            bookings = TicketBooking.objects.filter(
                user=self.request.user,
                session__in=context['sessions']
            ).select_related('session')
            bookings_map = {booking.session_id: booking for booking in bookings}
            for session in context['sessions']:
                session.current_user_booking = bookings_map.get(session.id)

        context['booking_form'] = TicketBookingForm()
        return context


class SessionCreateView(WorkerRequiredMixin, CreateView):
    """Створення нового сеансу - тільки для робітників"""
    model = Session
    form_class = SessionForm
    template_name = 'cinema/session_form.html'

    def get_initial(self):
        initial = super().get_initial()
        movie_id = self.kwargs.get('movie_id')
        if movie_id:
            initial['movie'] = movie_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додати сеанс'
        movie_id = self.kwargs.get('movie_id')
        if movie_id:
            context['movie'] = get_object_or_404(Movie, pk=movie_id)
        return context

    def get_success_url(self):
        if self.object.movie:
            return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})
        return reverse('session_list')


class SessionDeleteView(WorkerRequiredMixin, DeleteView):
    """Видалення сеансу - тільки для робітників"""
    model = Session
    template_name = 'cinema/session_confirm_delete.html'

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})


@login_required
@require_POST
def book_session(request, pk):
    """Створення або оновлення бронювання користувача для сеансу"""
    session = get_object_or_404(Session, pk=pk)
    next_url = request.POST.get('next') or reverse('session_list')

    if session.date < timezone.now():
        messages.error(request, 'Неможливо бронювати квитки на минулий сеанс.')
        return redirect(next_url)

    form = TicketBookingForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Перевірте коректність кількості квитків.')
        return redirect(next_url)

    tickets_count = form.cleaned_data['tickets_count']
    booking, created = TicketBooking.objects.get_or_create(
        session=session,
        user=request.user,
        defaults={'tickets_count': tickets_count}
    )

    if not created:
        booking.tickets_count = tickets_count

    try:
        booking.full_clean()
        booking.save()
    except ValidationError as error:
        messages.error(request, '; '.join(error.messages))
        return redirect(next_url)

    if created:
        messages.success(request, 'Квитки успішно заброньовано.')
    else:
        messages.success(request, 'Ваше бронювання оновлено.')

    return redirect(next_url)


@login_required
@require_POST
def cancel_booking(request, pk):
    """Скасування власного бронювання"""
    booking = get_object_or_404(TicketBooking, pk=pk, user=request.user)
    next_url = request.POST.get('next') or reverse('session_list')
    booking.delete()
    messages.info(request, 'Бронювання скасовано.')
    return redirect(next_url)


@login_required
@require_POST
def mark_booking_watched(request, pk):
    """Позначає бронювання користувача як переглянуте"""
    booking = get_object_or_404(TicketBooking, pk=pk, user=request.user)
    next_url = request.POST.get('next') or reverse('session_list')

    if booking.is_watched:
        messages.info(request, 'Цей сеанс вже позначено як переглянутий.')
        return redirect(next_url)


    booking.mark_watched()
    messages.success(request, 'Сеанс позначено як переглянутий.')
    return redirect(next_url)


# ================== USER PROFILE ==================

class UserProfileDetailView(DetailView):
    """Публічна сторінка профілю користувача"""
    model = User
    template_name = 'cinema/profile_detail.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_obj, _ = UserProfile.objects.get_or_create(user=self.object)
        all_reviews = self.object.reviews.select_related('movie').order_by('-created_at')
        watched_movies = Movie.objects.filter(
            sessions__bookings__user=self.object,
            sessions__bookings__is_watched=True
        ).distinct().order_by('title')
        favorite_items = FavoriteMovie.objects.filter(user=self.object).select_related('movie').order_by('-created_at')
        bookings_total = TicketBooking.objects.filter(user=self.object).count()
        watched_bookings_total = TicketBooking.objects.filter(user=self.object, is_watched=True).count()

        context['profile_obj'] = profile_obj
        context['reviews_count'] = all_reviews.count()
        context['all_reviews'] = all_reviews
        context['recent_reviews'] = all_reviews[:5]
        context['watched_movies'] = watched_movies
        context['favorite_items'] = favorite_items
        context['stats'] = {
            'reviews_count': all_reviews.count(),
            'watched_movies_count': watched_movies.count(),
            'watched_sessions_count': watched_bookings_total,
            'favorites_count': favorite_items.count(),
            'bookings_count': bookings_total,
        }

        is_owner = self.request.user.is_authenticated and self.request.user == self.object
        context['can_edit_profile'] = is_owner
        if is_owner:
            context['profile_form'] = UserProfileForm(instance=profile_obj)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated or request.user != self.object:
            return redirect('profile_detail', pk=self.object.pk)

        profile_obj, _ = UserProfile.objects.get_or_create(user=self.object)
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фото профілю оновлено.')
        else:
            messages.error(request, 'Не вдалося оновити фото профілю.')

        return redirect('profile_detail', pk=self.object.pk)


class FavoriteListView(LoginRequiredMixin, ListView):
    """Список улюблених фільмів поточного користувача"""
    model = FavoriteMovie
    template_name = 'cinema/favorite_list.html'
    context_object_name = 'favorite_items'
    login_url = 'login'

    def get_queryset(self):
        return FavoriteMovie.objects.filter(user=self.request.user).select_related('movie').order_by('-created_at')


@login_required
@require_POST
def toggle_favorite(request, pk):
    """Додає або прибирає фільм з улюблених"""
    movie = get_object_or_404(Movie, pk=pk)
    next_url = request.POST.get('next') or reverse('movie_detail', kwargs={'pk': movie.pk})
    favorite = FavoriteMovie.objects.filter(user=request.user, movie=movie)

    if favorite.exists():
        favorite.delete()
        messages.info(request, 'Фільм прибрано з улюблених.')
    else:
        FavoriteMovie.objects.create(user=request.user, movie=movie)
        messages.success(request, 'Фільм додано в улюблені.')

    return redirect(next_url)


# ================== REVIEW VIEWS ==================

class ReviewUpdateView(LoginRequiredMixin, OwnerOrWorkerRequiredMixin, UpdateView):
    """Редагування відгуку - тільки автор або робітник"""
    model = Review
    form_class = ReviewForm
    template_name = 'cinema/review_form.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редагувати відгук на {self.object.movie.title}'
        context['button_text'] = 'Зберегти зміни'
        return context

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})


class ReviewDeleteView(LoginRequiredMixin, OwnerOrWorkerRequiredMixin, DeleteView):
    """Видалення відгуку - тільки автор або робітник"""
    model = Review
    template_name = 'cinema/review_confirm_delete.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})

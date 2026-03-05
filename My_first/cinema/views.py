from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from cinema.models import Movie, Session, Review
from cinema.forms import MovieForm, SessionForm, ReviewForm


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

        # Пошук по назві
        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)

        # Фільтр по жанру
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)

        # Фільтр по року
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(year=year)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаємо жанри в шаблон для фільтра
        context['genres'] = Movie.GENRE_CHOICES
        # Передаємо поточні параметри пошуку
        context['search_title'] = self.request.GET.get('title', '')
        context['search_genre'] = self.request.GET.get('genre', '')
        context['search_year'] = self.request.GET.get('year', '')
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
        context['reviews'] = self.object.reviews.all()
        context['average_rating'] = self.object.average_rating()

        # Перевіряємо права на редагування
        context['can_edit_movie'] = (
            self.request.user.is_superuser or
            self.request.user.groups.filter(name='Робітник').exists()
        )

        # Перевіряємо, чи користувач вже залишив відгук
        if self.request.user.is_authenticated:
            user_review = self.object.reviews.filter(user=self.request.user).first()
            context['user_review'] = user_review
            if not user_review:
                context['review_form'] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        """Обробка додавання/редагування відгуку"""
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()

        # Перевіряємо, чи користувач вже залишив відгук
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
        """Показуємо тільки майбутні сеанси"""
        now = timezone.now()
        return Session.objects.filter(date__gte=now).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Всі сеанси'
        return context


class SessionCreateView(WorkerRequiredMixin, CreateView):
    """Створення нового сеансу - тільки для робітників"""
    model = Session
    form_class = SessionForm
    template_name = 'cinema/session_form.html'

    def get_initial(self):
        """Попереднє заповнення форми, якщо переданий movie_id"""
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
        """Повертаємося на сторінку фільму або сеансів"""
        if self.object.movie:
            return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})
        return reverse('session_list')


class SessionDeleteView(WorkerRequiredMixin, DeleteView):
    """Видалення сеансу - тільки для робітників"""
    model = Session
    template_name = 'cinema/session_confirm_delete.html'

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})


class UserProfileDetailView(DetailView):
    """Публічна сторінка профілю користувача"""
    model = User
    template_name = 'cinema/profile_detail.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews_count'] = self.object.reviews.count()
        context['recent_reviews'] = self.object.reviews.select_related('movie').order_by('-created_at')[:5]
        return context


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

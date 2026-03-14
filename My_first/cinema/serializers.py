from rest_framework import serializers

from cinema.models import FavoriteMovie, Movie, Review, Session, TicketBooking, UserProfile


class UserSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)


class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'description',
            'year',
            'duration',
            'genre',
            'poster',
            'average_rating',
            'created_at',
            'updated_at',
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()


class SessionSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    available_tickets = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = [
            'id',
            'movie',
            'movie_title',
            'date',
            'hall_number',
            'max_tickets',
            'available_tickets',
            'created_at',
        ]

    def get_available_tickets(self, obj):
        return obj.available_tickets()


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_info = UserSummarySerializer(source='user', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'movie',
            'movie_title',
            'user',
            'user_info',
            'text',
            'rating',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_info = UserSummarySerializer(source='user', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_info', 'avatar']


class FavoriteMovieSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_info = UserSummarySerializer(source='user', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = FavoriteMovie
        fields = ['id', 'user', 'user_info', 'movie', 'movie_title', 'created_at']
        read_only_fields = ['created_at']


class TicketBookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_info = UserSummarySerializer(source='user', read_only=True)
    session_info = serializers.SerializerMethodField()

    class Meta:
        model = TicketBooking
        fields = [
            'id',
            'user',
            'user_info',
            'session',
            'session_info',
            'tickets_count',
            'created_at',
            'is_watched',
            'watched_at',
        ]
        read_only_fields = ['created_at', 'watched_at']

    def get_session_info(self, obj):
        return str(obj.session)


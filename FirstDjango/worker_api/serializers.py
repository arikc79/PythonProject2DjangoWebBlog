from rest_framework.serializers import ModelSerializer

from workers.models import Worker, Resume


class ResumeSerializer(ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"


class WorkerSerializer(ModelSerializer):
    resume = ResumeSerializer(read_only=True)

    class Meta:
        model = Worker
        fields = "__all__"


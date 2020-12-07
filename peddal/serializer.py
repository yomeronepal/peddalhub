from rest_framework.serializers import ModelSerializer
from .models import *

class BookSerializer(ModelSerializer):
    class Meta:
        model= Cycle
        fields = "__all__"
        
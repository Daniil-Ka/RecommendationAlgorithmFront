from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
   # cover_url_200 = serializers.URLField()
   # cover_url_1000 = serializers.URLField()
   # download_url = serializers.URLField()
   class Meta:
      model = Track
      fields = "__all__"
      extra_kwargs = {
         'cover_url_200': {'required': False},
         'cover_url_1000': {'required': False},
         'download_url': {'required': False},
      }
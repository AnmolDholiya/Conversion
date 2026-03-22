from rest_framework import serializers
from .models import ImageConversion

class ImageConversionSerializer(serializers.ModelSerializer):
    original_file = serializers.FileField(required=True)
    
    class Meta:
        model = ImageConversion
        fields = ['id', 'original_file', 'converted_file', 'conversion_type', 'target_format', 'created_at']
        read_only_fields = ['id', 'converted_file', 'created_at']

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    target_format = serializers.CharField(required=False)

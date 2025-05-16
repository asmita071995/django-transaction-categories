from rest_framework import serializers
from .models import UserJsonUpload
import json

class UserJsonUploadSerializer(serializers.ModelSerializer):
    json_file_upload = serializers.FileField(write_only=True)

    class Meta:
        model = UserJsonUpload
        fields = ['name', 'place', 'date_of_birth', 'country', 'mobile_number', 'json_file_upload']

    def create(self, validated_data):
        file = validated_data.pop('json_file_upload')
        json_content = file.read().decode('utf-8')
        validated_data['json_data'] = json_content
        return UserJsonUpload.objects.create(**validated_data)

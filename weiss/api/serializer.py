from rest_framework import serializers
from weiss.api.api_response import APIResponse

class APIResponseSerializer(serializers.Serializer):
    fid = serializers.IntegerField()
    response = serializers.CharField()

    def create(self, validated_data):
        return APIResponse(**validated_data)

    def update(self, instance, validated_data):
        instance.fid = validated_data.get('fid', instance.fid)
        instance.response = validated_data.get('response', instance.response)
        return instance

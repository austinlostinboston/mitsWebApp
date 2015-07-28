"""
This file contain serializers for API requests and responses

Author: Ming Fang
"""
from rest_framework import serializers
from weiss.api.responses import *
from weiss.api.requests import *

class InitResponseSerializer(serializers.Serializer):
    fid = serializers.IntegerField()
    response = serializers.CharField()

    def create(self, validated_data):
        return InitResponse(**validated_data)

    def update(self, instance, validated_data):
        instance.response = validated_data.get('response', instance.response)
        return instance

class QueryRequestSerializer(serializers.Serializer):
    fid = serializers.IntegerField()
    query = serializers.CharField()

    def create(self, validated_data):
        return QueryRequest(**validated_data)

    def update(self, instance, validated_data):
        instance.query = validated_data.get('query', instance.response)
        return instance


class QueryResponseSerializer(serializers.Serializer):
    response = serializers.CharField()

    def create(self, validated_data):
        return QueryResponse(**validated_data)

    def update(self, instance, validated_data):
        instance.response = validated_data.get('response', instance.response)
        return instance

class CloseRequestSerializer(serializers.Serializer):
    fid = serializers.IntegerField()

    def create(self, validated_data):
        return CloseRequest(**validated_data)

    def update(self, instance, validated_data):
        instance.fid = validated_data.get('fid', instance.fid)
        return instance


class CloseResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()

    def create(self, validated_data):
        return CloseResponse(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('fid', instance.status)
        return instance

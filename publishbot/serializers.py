from rest_framework import serializers
from publishbot.models import Publication, Event, Configuration


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    publication = PublicationSerializer()
    published_data = serializers.JSONField()
    network_response = serializers.JSONField()
    reactions = serializers.JSONField()

    class Meta:
        model = Event
        fields = '__all__'


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'


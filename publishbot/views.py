import tweepy
from datetime import datetime

from django.http import JsonResponse, Http404
from django.shortcuts import render

from publishbot.connection_settings import twitter_connect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models import Publication, Event, Configuration
from serializers import PublicationSerializer, EventSerializer, ConfigurationSerializer



def home(request):
    pass


class PublicationList(APIView):
    def get(self, request, format=None):
        publications = Publication.objects.all()
        serializer = PublicationSerializer(publications, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PublicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicationDetail(APIView):
    def get_object(self, pk):
        try:
            return Publication.objects.get(pk=pk)
        except Publication.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        publication = self.get_object(pk)
        serializer = PublicationSerializer(publication)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        publication = self.get_object(pk)
        serializer = PublicationSerializer(publication, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        publication = self.get_object(pk)
        publication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventList(APIView):
    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetail(APIView):
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ConfigurationList(APIView):
    def get(self, request, format=None):
        configuration = Configuration.objects.all()
        serializer = ConfigurationSerializer(configuration, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfigurationDetail(APIView):
    def get_object(self, pk):
        try:
            return Configuration.objects.get(pk=pk)
        except Configuration.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        configuration = self.get_object(pk)
        serializer = ConfigurationSerializer(configuration)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        configuration = None


"""
API endpoints

Publication CRUD

Event CRUD

Config CRUD

send_publication

send_publications
"""

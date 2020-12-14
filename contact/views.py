from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import permissions, status


class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        if request.user.has_expired:
            self.message = "Your account has expired."
            return False
        elif request.user.has_access:
            return True
        else:
            return False

class ContactList(ListCreateAPIView):

    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)
    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)


class ContactDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

class NeedLogin(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'error': True, 'message': 'need login'}
    default_code = 'not_authenticated'
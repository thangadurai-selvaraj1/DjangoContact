from rest_framework.serializers import ModelSerializer
from .models import Contact
from rest_framework import serializers


class ContactSerializer(ModelSerializer):

    class Meta:
        model = Contact
        fields = ['country_code', 'id', 'first_name', 'last_name', 'phone_number',
                  'contact_picture', 'is_favorite'
                  ]

    def validate(self, attrs):
            first_name = attrs.get('first_name' '')
            if Contact.objects.filter(first_name=first_name).exists():
                raise serializers.ValidationError({'first_name': 'first_name alredy exits'})
            return super().validate(attrs)
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=256, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email' '')
        password = attrs.get('password' '')
        username = attrs.get('username' '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'email alredy exits'})
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'username alredy exits'})
        elif len(User.objects.filter(password=password)) < 4:
            raise serializers.ValidationError({'password': 'username alredy exits'})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

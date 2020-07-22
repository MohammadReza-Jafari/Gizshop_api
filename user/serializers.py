import re
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.shortcuts import render

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from core import helpers


class UserSerializer(serializers.ModelSerializer):
    postal_code = serializers.RegexField(
        regex=r'\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b',
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'address', 'national_code', 'postal_code', 'phone_number',
                  'bank_account', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        data = {
            'name': user.name,
            'activation_code': user.activation_code
        }
        helpers.send_email(
            'Gizshop verification',
            'verification_email.html',
            'verification_text.txt',
            data,
            user.email
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

    def validate(self, attrs):
        national_code = attrs['national_code']
        phone_number = attrs['phone_number']
        errors = {}
        national_code_error_msg = None
        phone_number_error_msg = None
        if not re.match(
                pattern="(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}",
                string=phone_number
        ):
            phone_number_error_msg = "Doesn't match with iran phone number pattern"
        if not helpers.is_valid_national_code(national_code):
            national_code_error_msg = "National code is not valid"

        if phone_number_error_msg:
            errors.update({'phone_number': phone_number_error_msg})
        if national_code_error_msg:
            errors.update({'national_code': national_code_error_msg})

        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return attrs


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False, allow_null=False)
    password = serializers.CharField(trim_whitespace=False, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        user = authenticate(
            self.context['request'], username=email, password=password)
        print(user)

        if not user:
            raise serializers.ValidationError(
                {'error': 'Can not authenticate with provided credentials'})
        if not user.is_active:
            raise serializers.ValidationError({'error': 'User is not active'})

        attrs['user'] = user
        return attrs


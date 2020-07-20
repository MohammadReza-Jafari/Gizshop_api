from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


def is_valid_national_code(national_code: str):
    if not len(national_code) == 10:
        return False
    wrong_code = [
        '0000000000', '1111111111', '2222222222', '3333333333', '4444444444', '5555555555',
        '6666666666', '7777777777', '8888888888', '9999999999'
    ]

    if national_code in wrong_code:
        return False

    if not national_code.isdigit():
        return False

    check = int(national_code[9])
    temp1 = sum([int(national_code[x]) * (10 - x) for x in range(9)])
    temp2 = temp1 % 11

    if temp2 == 0 and check == temp2:
        return True
    if temp2 == 1 and check == 1:
        return True
    if temp2 > 1 and check == abs(temp2 - 11):
        return True
    return False


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.RegexField(
        regex=r'(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}',
        required=True
    )
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
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

    def validate(self, attrs):
        national_code = attrs['national_code']
        if not is_valid_national_code(national_code):
            raise serializers.ValidationError({'national_code': 'National code is not valid'})
        return attrs


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False, allow_null=False)
    password = serializers.CharField(trim_whitespace=False, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        print(email)
        print(password)

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

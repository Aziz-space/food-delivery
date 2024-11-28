from datetime import date
from rest_framework import serializers
from account.models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'get_full_name',
            'first_name',
            'last_name',
            'email',
            'role',
        )


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'birth_date', 'gender', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Check password matching
        password = data.get('password')
        password2 = data.pop('password2')
        
        if password != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        
        return data

    def create(self, validated_data):
        # Create user method
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birth_date=validated_data['birth_date'],
            gender=validated_data['gender'],
            role=validated_data['role']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role', 'birth_date', 'gender', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance

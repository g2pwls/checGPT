from rest_framework import serializers
from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'name',
            'profile_image',
            'interests',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

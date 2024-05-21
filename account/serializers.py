from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    permission = serializers.ListField(
        source="get_user_permissions_list", read_only=True
    )
    normalized_password = serializers.CharField(
        source="initial_password_changed", read_only=True
    )
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            # "id",
            "date_joined",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "normalized_password",  # if user has change the password after login using temp password
            "date_joined",
            "full_name",
            "permission",
        ]

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%b %d %Y") if obj.date_joined else None
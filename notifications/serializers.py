from rest_framework import serializers
from .models import Notification








class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id","recipient","title","message","is_read","created_at"]
        read_only_fields = ["id","recipient","title","message","created_at"]

    def validate(self, attrs):
        is_read = attrs["is_read"]
        if self.instance:
            if self.instance.is_read == True and is_read == False:
                raise serializers.ValidationError({"is_read": "This field cannot be false"})
        return attrs

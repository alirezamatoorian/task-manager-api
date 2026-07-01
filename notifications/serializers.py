from rest_framework import serializers
from .models import Notification
from django.utils.timesince import timesince








class NotificationSerializer(serializers.ModelSerializer):
    created_at_human=serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = ["id","recipient","title","message","is_read","created_at","created_at_human"]
        read_only_fields = ["id","recipient","title","message","created_at"]

    def validate(self, attrs):
        is_read = attrs.get("is_read")
        if self.instance:
            if self.instance.is_read == True and is_read == False:
                raise serializers.ValidationError({"is_read": "This field cannot be false"})
        return attrs

    def get_created_at_human(self, obj):
        return timesince(obj.created_at)

import re

from rest_framework import serializers

from .models import Moment, Registration


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = (
            "firstName",
            "lastName",
            "email",
            "phone",
            "city",
            "churchType",
            "godhouseCentre",
            "otherChurch",
            "attendanceType",
            "accommodation",
        )
        extra_kwargs = {
            field: {"required": True, "allow_blank": False, "write_only": True}
            for field in (
                "firstName",
                "lastName",
                "email",
                "phone",
                "city",
                "churchType",
                "attendanceType",
                "accommodation",
            )
        }
        extra_kwargs.update({
            "email": {"required": True, "allow_blank": True, "allow_null": True, "write_only": True},
            "godhouseCentre": {"write_only": True},
            "otherChurch": {"write_only": True},
        })

    def validate_email(self, value):
        return value or ""

    def validate_phone(self, value):
        if not re.fullmatch(r"\+?[0-9(). -]+", value) or len(re.findall(r"[0-9]", value)) < 10:
            raise serializers.ValidationError("Enter a phone number containing at least 10 digits.")
        return value

    def validate(self, data):
        branch_field, unused_field = (
            ("godhouseCentre", "otherChurch")
            if data["churchType"] == "Godhouse"
            else ("otherChurch", "godhouseCentre")
        )
        if not data.get(branch_field):
            message = (
                "Select your Godhouse centre."
                if branch_field == "godhouseCentre"
                else "Enter your church name."
            )
            raise serializers.ValidationError({branch_field: message})
        data[unused_field] = ""
        return data


class MomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moment
        fields = "__all__"

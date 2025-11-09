from enum import verify
from os import read
from xml.dom import ValidationErr
from attr import field
from rest_framework import serializers

from base.api.v1.serializers import BaseSerializer
# from base.api. import BaseSerializer


from apps.core.models import Complaints, DropDown, User, BaseModel

from apps.core.utils import classify_civic_issue, verify_civic_issue
# Write your serializers here


class DropDownSerializer(BaseSerializer):

    sub_category = serializers.SerializerMethodField(read_only=True)
    category = serializers.CharField(source="label")

    class Meta:
        model = DropDown
        fields = "__all__"

    def get_sub_category(self, instance):
        children = DropDown.objects.filter(parent=instance)
        return DropDownSerializer(children, many=True, exclude=BaseModel.BASE_MODEL_FIELDS + ("parent", "label")).data


class LoginSerializer(BaseSerializer):

    # upvoted_posts = serializers.ManyRelatedField(required=False)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):

        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get("password"))
        user.save()
        return user


class ComplaintSerializer(BaseSerializer):

    updated_at = serializers.DateTimeField(format="%d-%b-%Y %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%d-%b-%Y %H:%M:%S", read_only=True)
    upvoted = serializers.SerializerMethodField(read_only=True)
    total_upvotes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Complaints
        fields = "__all__"

    def get_upvoted(self, instance):
        return self.context.get("request").user in instance.upvoted_complaints.all()

    def get_total_upvotes(self, instance):
        return instance.upvoted_complaints.count()

    def validate(self, data):
        if not verify_civic_issue(data["image"], description=data["description"]):
            raise serializers.ValidationError("Title or Description are not Civic Issues")
        return data

    # def create(self, validated_data):
    #     return super().create(**validated_data)

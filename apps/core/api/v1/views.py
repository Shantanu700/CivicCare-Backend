import base64

from typing import Dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from pkg_resources import require
from redis import AuthenticationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers


from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    inline_serializer,
)
from drf_spectacular.types import OpenApiTypes
from yaml import serialize

from apps.core.choices import CompalaintsChoices
from base.api.v1.views import BaseAV
from base.api.v1.decorators import extend_schema_response

from apps.core.api.v1.serializers import (
    ComplaintSerializer,
    DropDownSerializer,
    LoginSerializer,
)
from apps.core.models import BaseModel, Complaints, DropDown, User
from apps.core.tasks import send_qr_stream

# Write your views here


class DropdownAV(BaseAV):

    authentication = False

    @extend_schema(
        request=DropDownSerializer,
    )
    def post(self, request):
        data = request.data
        serializer = DropDownSerializer(
            data=data,
            exclude=BaseModel.BASE_MODEL_FIELDS + ("parent", "label"),
            many=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Dropdown Saved"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "uuid",
                OpenApiTypes.UUID,
            ),
        ]
    )
    def get(self, request):
        data = request.query_params
        dropdowns = DropDown.objects.filter(
            parent=DropDown.objects.get(uuid=data.get("uuid"))
        )
        serializer = DropDownSerializer(
            dropdowns,
            many=True,
            exclude=BaseModel.BASE_MODEL_FIELDS + ("parent", "label"),
        )
        return Response(serializer.data)


class RegisterAV(BaseAV):

    authentication = False

    @extend_schema(
        request=inline_serializer(
            name="LoginSerializer",
            fields={
                **{
                    k: v
                    for k, v in LoginSerializer().get_fields().items()
                    if k
                    not in User.USER_MODEL_FIELDS
                    + (
                        "role",
                        "uuid",
                        "user_permissions",
                        "location",
                        "upvoted_posts",
                    )
                },
                "latitude": serializers.FloatField(required=True),
                "longitude": serializers.FloatField(required=True),
            },
        ),
    )
    def post(self, request):
        data = request.data
        print(request.data)
        data = data.copy()
        longitude = float(data.pop("longitude", []))
        latitude = float(data.pop("latitude", []))
        data["location"] = Point(longitude, latitude)
        serializer = LoginSerializer(data=data, exclude=(User.USER_MODEL_FIELDS))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class LoginAV(BaseAV):
    "Login/Logout API View"

    authentication = {
        "post": False,
    }

    def decrypt_auth(self, meta_info) -> None | Dict:
        print(meta_info)
        header, data = meta_info.split(" ")
        if header != "Basic":
            return None
        decrypted_auth = base64.b64decode(data).decode("utf-8")
        credentials = decrypted_auth.split(":")
        print(credentials)
        return {
            "phone_number": credentials[0],
            "password": credentials[1],
        }

    @extend_schema_response(type=LoginSerializer(exclude=User.USER_MODEL_FIELDS))
    def get(self, request):
        serializer = LoginSerializer(
            instance=request.user,
            exclude=User.USER_MODEL_FIELDS,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema_response(type=LoginSerializer(exclude=User.USER_MODEL_FIELDS))
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="Authorization",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                required=True,
                examples=[
                    OpenApiExample(
                        name="User Authentication",
                        value="Basic ZXJwQGtpZXQuZWR1OkBlcnA=",
                        summary="base64 encoded credentials are required",
                        description="",
                    )
                ],
            )
        ]
    )
    def post(self, request):
        auth_data = request.META.get("HTTP_AUTHORIZATION")
        credentials = self.decrypt_auth(auth_data)
        user = authenticate(request, **credentials)
        if user is not None:
            login(request, user)
            response = {
                "msg": "Login Successfull.",
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "msg": "Invalid Credentials.",
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        logout(request)
        response = {
            "msg": "Logout successfull.",
        }
        return Response(response, status=status.HTTP_200_OK)


class ComplaintAV(BaseAV):

    authentication = True

    @extend_schema(
        request=inline_serializer(
            name="ComplaintSerializer",
            fields={
                **{
                    k: v
                    for k, v in ComplaintSerializer().get_fields().items()
                    if k not in ("location", "user", "status")
                },
                "latitude": serializers.FloatField(),
                "longitude": serializers.FloatField(),
            },
        ),
        responses={
            201: inline_serializer(
                name="ComplaintPostResponse",
                fields={"msg": serializers.CharField(default="Complaint Registered")},
            )
        },
    )
    def post(self, request):
        data = request.data
        data = data.copy()
        longitude = float(data.pop("longitude", [1])[0])
        latitude = float(data.pop("latitude", [1])[0])
        data["location"] = Point(longitude, latitude)
        data["user"] = request.user.id
        serializer = ComplaintSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema_response(
        type=ComplaintSerializer,
    )
    def get(self, request):
        user_location = request.user.location
        nearest_complaints = (
            Complaints.objects.filter(location__distance_lte=(user_location, D(km=10)))
            .exclude(status=CompalaintsChoices.DELETED)
            .annotate(distance=Distance("location", user_location))
            .order_by("distance")
        )
        serializer = ComplaintSerializer(
            nearest_complaints,
            many=True,
            exclude=["uuid"],
            context={"request": request},
        )
        return Response(serializer.data)

    @extend_schema(
        request=inline_serializer(
            name="ComplaintPutRequest",
            fields={"id": serializers.IntegerField(default=0)},
        )
    )
    def put(self, request):
        data = request.data
        issue_id = data.get("id")
        if int(issue_id) in request.user.upvoted_posts.all().values_list(
            "id", flat=True
        ):
            request.user.upvoted_posts.remove(Complaints.objects.get(id=issue_id))
            return Response({"msg": "Post Downvoted"})
        else:
            request.user.upvoted_posts.add(Complaints.objects.get(id=issue_id))
            return Response({"msg": "Post Upvoted"})


class IssuesAV(BaseAV):

    authentication = False

    def get(self, request):
        nearest_complaints = Complaints.objects.filter().exclude(
            status=CompalaintsChoices.DELETED
        )
        serializer = ComplaintSerializer(
            nearest_complaints,
            many=True,
            exclude=["uuid"],
            context={"request": request},
        )
        return Response(serializer.data)

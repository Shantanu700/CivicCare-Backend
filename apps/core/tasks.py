from celery import shared_task
import uuid6
import time

from django_eventstream import send_event

from apps.core.utils import generate_svg_qr
from apps.core.api.v1.serializers import UserTokenSerializer


@shared_task
def send_qr_stream(uuid):
    # qr_uuid = uuid6.uuid6()
    # serializer = UserTokenSerializer(
    #     data={
    #         "token": uuid,
    #         "qr_uuid": qr_uuid,
    #     }
    # )
    # if serializer.is_valid():
    #     serializer.save()
    send_event(
        # f"{uuid}",
        "test",
        "message",
        {"data": f"Testing channel {uuid}", "uuid": uuid},
    )
    # qr1 = generate_svg_qr(qr_uuid, token=None)
    # return qr1

from base64 import b64decode

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import JSONParser, ParseError
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ModelViewSet

from common.request_utils import get_query_param_int, get_query_param_str
from devices.models import Device, Measurement

from .serializers import DeviceCreateSerializer, DeviceSerializer, MeasurementCreateSerializer, MeasurementSerializer


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["uuid", "name", "time_created"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == "create":
            return DeviceCreateSerializer
        return DeviceSerializer


class MeasurementViewSet(ModelViewSet):
    queryset = Measurement.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return MeasurementCreateSerializer
        return MeasurementSerializer

    def get_queryset(self):
        queryset = Measurement.objects.all()
        if self.action != "list":
            return queryset

        # Filter by query params
        queryset = self.get_queryset_direct(self.request, queryset)

        # Limit max returned count
        hard_max_count = settings.API_MEASUREMENTS_MAX_COUNT
        queryset = queryset[:hard_max_count]

        return queryset

    def get_queryset_direct(self, request, queryset):

        # Filter by query params
        device = get_query_param_str(request, "device")
        if device is not None:
            try:
                queryset = queryset.filter(device=device)
            except ValidationError as err:  # noqa: F841
                pass  # Ignore

        time_start = get_query_param_str(request, "time_start")
        if time_start is not None:
            try:
                queryset = queryset.filter(time__gte=time_start)
            except ValidationError as err:  # noqa: F841
                pass  # Ignore

        time_end = get_query_param_str(request, "time_end")
        if time_end is not None:
            try:
                queryset = queryset.filter(time__lt=time_end)
            except ValidationError as err:  # noqa: F841
                pass  # Ignore

        id_start = get_query_param_int(request, "id_start")
        if id_start is not None:
            queryset = queryset.filter(id__gte=id_start)

        id_end = get_query_param_int(request, "id_end")
        if id_end is not None:
            queryset = queryset.filter(id__lt=id_end)

        max_count = get_query_param_int(request, "max_count")
        if max_count is not None:
            queryset = queryset[:max_count]

        order_by = get_query_param_str(request, "order_by")
        if order_by == "uuid":
            queryset = queryset.order_by("uuid")
        if order_by == "-uuid":
            queryset = queryset.order_by("-uuid")
        if order_by == "name":
            queryset = queryset.order_by("name")
        if order_by == "-name":
            queryset = queryset.order_by("-name")
        if order_by == "time_created":
            queryset = queryset.order_by("time_created")
        if order_by == "-time_created":
            queryset = queryset.order_by("-time_created")

        return queryset

    @action(url_path="nbiot_engineering", name="NB-IoT Engineering Webhook Endpoint", detail=False, methods=["post"])
    def nbiot_engineering(self, request):
        data = JSONParser().parse(request)
        if "messages" not in data or len(data["messages"]) == 0 or "payload" not in data["messages"][0]:
            return JsonResponse(status=400, data={"error": "Missing payload."})
        payload_encoded = data["messages"][0]["payload"]
        payload_string = b64decode(payload_encoded).decode("utf-8")
        try:
            payload_data = json.loads(payload_string)
        except ValueError as ex:
            raise ParseError("JSON parse error - {ex}".format(ex=ex))
        serializer = MeasurementCreateSerializer(data=payload_data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @action(url_path="count", name="Measurements Count", detail=False, methods=["get"])
    def measurements_count(self, request):
        queryset = self.get_queryset_direct(self.request, self.queryset)
        data = {
            "count": queryset.count(),
        }
        return Response(data)

from rest_framework import serializers

from .models import Device, Measurement


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ["uuid", "time_created"]

    url = serializers.HyperlinkedIdentityField(view_name="device-detail")
    measurements_count = serializers.SerializerMethodField()

    def get_measurements_count(self, obj):
        return Measurement.objects.filter(device=obj).count()


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = "__all__"
        read_only_fields = ["device", "time", "ph"]

    url = serializers.HyperlinkedIdentityField(view_name="measurement-detail")

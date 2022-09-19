from . import models
from users.models import CustomUser
from rest_framework import serializers


class ViewCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = ("id", "name")


class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "role",
            "first_name",
            "last_name",
            "signedUpAt",
        )


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AirlineCompany
        fields = ("id", "name", "country", "slug", "user")


class ViewAirlineSerializer(serializers.ModelSerializer):
    country = ViewCountrySerializer()
    user = ViewUserSerializer()

    class Meta:
        model = models.AirlineCompany
        fields = ("id", "name", "country", "slug", "user")


class FlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flight
        fields = (
            "id",
            "airline_company",
            "origin_contry",
            "destination_contry",
            "departure_time",
            "landing_time",
            "remaining_tickets",
            "price",
        )


class ViewFlightsSerializer(serializers.ModelSerializer):
    airline_company = ViewAirlineSerializer()
    origin_contry = ViewCountrySerializer()
    destination_contry = ViewCountrySerializer()

    class Meta:
        model = models.Flight
        fields = (
            "id",
            "airline_company",
            "origin_contry",
            "destination_contry",
            "departure_time",
            "landing_time",
            "remaining_tickets",
            "price",
        )


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = ("id", "flight_id", "customer_id", "quantity")


class ViewTicketsSerializer(serializers.ModelSerializer):
    flight_id = ViewFlightsSerializer()
    customer_id = ViewUserSerializer()

    class Meta:
        model = models.Ticket
        fields = ("id", "flight_id", "customer_id", "quantity")

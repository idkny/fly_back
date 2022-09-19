from rest_framework.decorators import api_view
from . import serializers
from . import models
from django.http.response import JsonResponse
from rest_framework import status, permissions
from django.db.models import F
from rest_framework.parsers import JSONParser
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)



@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def Countries(request):
    if request.method == "GET":
        all_data = models.Country.objects.all().order_by("-id")
        object_serializer = serializers.ViewCountrySerializer(all_data, many=True)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(["POST", "GET"])
def Airlines(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        count = (
            models.AirlineCompany.objects.all()
            .filter(user=data["user"], name=data["name"])
            .count()
        )
        if count > 0:
            return JsonResponse(
                {"message": "Airline with the same name already exists!"},
                status=status.HTTP_200_OK,
            )
        data["slug"] = data["name"]
        object_serializer = serializers.AirlineSerializer(data=data)
        if object_serializer.is_valid():
            object_serializer.save()
            return JsonResponse(object_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(
            {"message": object_serializer.errors}, status=status.HTTP_200_OK
        )
    elif request.method == "GET":
        all_data = models.AirlineCompany.objects.all().order_by("-id")
        object_serializer = serializers.ViewAirlineSerializer(all_data, many=True)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(["GET"])
def MyAirlines(request, pk):
    if request.method == "GET":
        all_data = models.AirlineCompany.objects.all().filter(user=pk).order_by("-id")
        object_serializer = serializers.ViewAirlineSerializer(all_data, many=True)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(["POST", "GET"])
@authentication_classes([])
@permission_classes([])
def Flights(request):
    if request.method == "GET":
        all_data = models.Flight.objects.all().order_by("-id")
        object_serializer = serializers.ViewFlightsSerializer(all_data, many=True)
        return JsonResponse(object_serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        object_serializer = serializers.FlightsSerializer(data=data)
        if object_serializer.is_valid():
            object_serializer.save()
            return JsonResponse(object_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(
            {"message": object_serializer.errors}, status=status.HTTP_200_OK
        )


@api_view(["GET"])
def MyFlights(request, pk):
    if request.method == "GET":
        all_data = (
            models.Flight.objects.all().filter(airline_company=pk).order_by("-id")
        )
        object_serializer = serializers.ViewFlightsSerializer(all_data, many=True)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(["GET", "POST"])
@authentication_classes([])
@permission_classes([])
def FlightByID(request, pk):
    if request.method == "GET":
        all_data = models.Flight.objects.all().filter(id=pk).order_by("-id").first()
        object_serializer = serializers.ViewFlightsSerializer(all_data, many=False)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def FilterFlights(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        origin_contry = data["origin_contry"]
        destination_contry = data["destination_contry"]
        departure_time = data["departure_time"]
        landing_time = data["landing_time"]
        all_data = models.Flight.objects.all()
        if origin_contry != "":
            all_data = all_data.filter(origin_contry=origin_contry)
        if destination_contry != "":
            all_data = all_data.filter(destination_contry=destination_contry)
        if departure_time != "":
            print(all_data.count())
            all_data = all_data.filter(departure_time__gte=departure_time)
            print(all_data.count())
        if landing_time != "":
            all_data = all_data.filter(landing_time__lte=landing_time)
        all_data = all_data.order_by("-id")
        object_serializer = serializers.ViewFlightsSerializer(all_data, many=True)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(["POST"])
def Tickets(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            models.Flight.objects.filter(pk=int(data["flight_id"])).update(
                remaining_tickets=F("remaining_tickets") - int(data["quantity"])
            )

        except Exception as e:
            print(e)
        object_serializer = serializers.TicketsSerializer(data=data)
        if object_serializer.is_valid():
            object_serializer.save()
            return JsonResponse(object_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(
            {"message": object_serializer.errors}, status=status.HTTP_200_OK
        )


@api_view(["GET"])
def TicketsByID(request, pk):
    if request.method == "GET":
        all_data = models.Ticket.objects.all().filter(customer_id=pk).order_by("-id")
        object_serializer = serializers.ViewTicketsSerializer(all_data, many=True)
        return JsonResponse(object_serializer.data, safe=False)

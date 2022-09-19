from django.db import models
from django.conf import settings


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True) 
   
    class Meta:
        db_table = "countries"

    def __str__(self):
        return f"Country id: {self.id}, name: {self.name}"


class AirlineCompany(models.Model):
    name = models.CharField(max_length=50, unique=True)  
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        db_table = "airline_companies"

    def __str__(self):
        return (
            f"AirlineCompany: {self.name}, country: {self.country}, user: {self.user}"
        )


class Flight(models.Model):
    airline_company = models.ForeignKey(AirlineCompany, on_delete=models.CASCADE)
    origin_contry = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name="origin_flights"
    )
    destination_contry = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="destination_flights",
    )
    departure_time = models.DateTimeField()  
    landing_time = models.DateTimeField()  
    remaining_tickets = models.IntegerField()  
    price = models.IntegerField()  

    def __str__(self):
        return f"Flight from {self.origin_contry} to {self.destination_contry}, departure time: {self.departure_time}, remaining tickets: {self.remaining_tickets}"

    class Meta:
        db_table = "flights"


class Ticket(models.Model):
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE) 
    customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self):
        return f"flight id: {self.flight_id}, customer id: {self.customer_id}"

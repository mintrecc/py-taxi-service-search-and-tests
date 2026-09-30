from urllib import response

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, DriverSearchForm, CarSearchForm
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class ManufacturersListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        response_custom = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response_custom.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response_custom.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response_custom,
            "taxi/manufacturer_list.html"
        )

    def test_manufacturer_context_messages(self):
        query = "Audi"
        custom_response = self.client.get(MANUFACTURER_URL, {"name": query})
        search_form_context = custom_response.context["search_form"]
        self.assertIsInstance(search_form_context, ManufacturerSearchForm)
        self.assertEqual(search_form_context.initial.get("name"), query)


class DriversListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        driver1 = get_user_model().objects.create(
            username="test1",
            license_number="ABC12345"
        )
        driver1.set_password("test1234")
        driver2 = get_user_model().objects.create(
            username="test2",
            license_number="DFE12345"
        )
        driver2.set_password("test1234")
        response_custom = self.client.get(DRIVER_URL)
        self.assertEqual(response_custom.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response_custom.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response_custom, "taxi/driver_list.html")

    def test_driver_context_message(self):
        query = "test1"
        custom_response = self.client.get(DRIVER_URL, {"username": query})
        search_form_context = custom_response.context["search_form"]
        self.assertIsInstance(search_form_context, DriverSearchForm)
        self.assertEqual(search_form_context.initial.get("username"), query)


class CarListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        driver1 = get_user_model().objects.create(
            username="test1",
            password="test1234",
            license_number="ABC12345"
        )
        driver2 = get_user_model().objects.create(
            username="test2",
            password="test1234",
            license_number="DFE12345"
        )
        audi = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car1 = Car.objects.create(
            model="Q8",
            manufacturer=audi

        )
        car1.drivers.set([driver1, driver2])
        car2 = Car.objects.create(
            model="Corolla",
            manufacturer=toyota
        )
        car2.drivers.set([driver1, driver2])

        response_custom = self.client.get(CAR_URL)
        self.assertEqual(response_custom.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response_custom.context["car_list"]), list(cars))
        self.assertTemplateUsed(response_custom, "taxi/car_list.html")

    def test_cars_context_message(self):
        query = "Q8"
        custom_response = self.client.get(CAR_URL, {"model": query})
        search_form_context = custom_response.context["search_form"]
        self.assertIsInstance(search_form_context, CarSearchForm)
        self.assertEqual(search_form_context.initial.get("model"), query)

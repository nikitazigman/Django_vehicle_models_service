import json
import logging
import os
from pathlib import Path
from typing import Type, Union

import requests
from app.models import VehicleBody, VehicleManufacture, VehicleModel, VehicleModelYear
from django.core.management.base import BaseCommand
from django.db import transaction
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

# Load .dev-env file
load_dotenv(BASE_DIR.joinpath("conf/env/.dev-env"))

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Command(BaseCommand):
    help = "add dataset of vehicles models into db, max rows is 10000"
    MODEL_T = Union[
        Type[VehicleModel],
        Type[VehicleBody],
        Type[VehicleManufacture],
        Type[VehicleModelYear],
    ]

    years: set[str] = set()
    manufactures: set[str] = set()
    bodies: set[str] = set()

    url = "https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?order=Year"

    headers = {
        "X-Parse-Application-Id": os.environ.get("APPLICATION_ID"),
        "X-Parse-REST-API-Key": os.environ.get("REST_API_KEY"),
    }

    DEFAULT_LIMIT = 10000

    def add_arguments(self, parser):
        parser.add_argument("limit", type=int)

    def _clean_the_table(self, model: MODEL_T):
        model.objects.all().delete()

    def _store_set_in_the_model(self, data: dict[str, set], model: MODEL_T):
        field_name = list(data.keys())[0]
        items = list(data.values())[0]
        for item in items:
            created_object = model(**{field_name: item})
            created_object.full_clean()
            created_object.save()

    def _create_and_store_vehicle_model(self, model_dict: dict):
        if not VehicleModel.objects.filter(name=model_dict["Model"]).exists():
            vehicle_model = VehicleModel(name=model_dict["Model"])
            vehicle_model.manufacture = VehicleManufacture.objects.get(
                name=model_dict["Make"]
            )
            vehicle_model.full_clean()
            vehicle_model.save()
        else:
            vehicle_model = VehicleModel.objects.get(name=model_dict["Model"])

        bodies = [body.strip() for body in model_dict["Category"].split(",")]
        model_bodies = VehicleBody.objects.filter(name__in=bodies)
        vehicle_model.body.add(*model_bodies)

        model_year = VehicleModelYear.objects.get(year=model_dict["Year"])
        vehicle_model.year.add(model_year)

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.url += f'&limit={kwargs["limit"]}'

            logger.debug(f"got limit={kwargs['limit']}")
            logger.debug("retrieving data from the server")
            data = json.loads(
                requests.get(self.url, headers=self.headers).content.decode("utf-8")
            )

            logger.debug(f"got {len(data['results'])} rows")

            for result in data["results"]:
                self.years.add(result["Year"])
                self.manufactures.add(result["Make"].strip())
                self.bodies.update([s.strip() for s in result["Category"].split(",")])

            logger.debug(
                "created sets of the vehicle model's years, manufactures, bodies"
            )

            sets_list = [self.years, self.manufactures, self.bodies]
            models_list = [VehicleModelYear, VehicleManufacture, VehicleBody]
            field_names_list = ["year", "name", "name"]

            logger.debug(
                "storing the sets of the vehicle model's years, manufactures, bodies into the DB"
            )

            for item, field_name, model in zip(
                sets_list, field_names_list, models_list
            ):
                self._clean_the_table(model)
                self._store_set_in_the_model({field_name: item}, model)

            logger.debug("Creating and storing vehicles' models into the DB")

            self._clean_the_table(VehicleModel)
            for vehicle_model in data["results"]:
                self._create_and_store_vehicle_model(vehicle_model)

            logger.debug("the command is done")

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Dict, List

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR.joinpath("conf/env/.dev-env"))

REMOTE_DB_URL = "https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?order=Year"
HEADERS = {
    "X-Parse-Application-Id": os.environ.get("APPLICATION_ID"),
    "X-Parse-REST-API-Key": os.environ.get("REST_API_KEY"),
}
DEFAULT_MODELS_NUMBER = 10000
DEFAULT_FILE_PATH = BASE_DIR.joinpath("/tools")


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def pull_vehicle_models(models_number: int) -> List[Dict]:
    global HEADERS

    pulled_data = []

    url = f"{REMOTE_DB_URL}&limit={models_number}"
    data = json.loads(
        requests.get(url, headers=HEADERS).content.decode("utf-8")
    )

    result_data = data["results"]

    result_length = len(result_data)

    for idx, result in enumerate(result_data):
        logger.debug(f"parsed {idx+1}/{result_length} models")

        for category in result["Category"].split(","):
            pulled_data.append(
                {
                    "year": result["Year"],
                    "manufacture": result["Make"],
                    "model": result["Model"],
                    "body": category.strip(),
                }
            )

    return pulled_data


def store_data(file_path: Path, data: List[Dict]):
    with open(
        file_path.joinpath("vehicle-model-dataset.json"), "w+"
    ) as f:
        json.dump(data, f)


def parse_arguments() -> dict:
    global DEFAULT_FILE_PATH
    global DEFAULT_MODELS_NUMBER

    parser = argparse.ArgumentParser(
        description="pull the vehicle models from remote server and store it as JSON file"
    )
    parser.add_argument("--path", type=str, default=DEFAULT_FILE_PATH)
    parser.add_argument(
        "--number", type=int, default=DEFAULT_MODELS_NUMBER
    )

    return parser.parse_args()


def main():
    logger.info("script was started")
    logger.debug(f"{HEADERS=}")
    logger.debug(f"{REMOTE_DB_URL=}")
    logger.debug(f"{BASE_DIR=}")

    args = parse_arguments()
    logger.debug(f"got following arguments: {args}")
    file_path = Path(args.path)

    data = pull_vehicle_models(models_number=args.number)
    store_data(file_path=file_path, data=data)

    logger.debug(
        f"data was stored to {file_path} folder as JSON file"
    )


if __name__ == "__main__":
    main()

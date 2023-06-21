# Note: This file will be used to hold a script
# that will be inserted into a Docker container with openIMIS.
# The script will take seed data and convert it into records in openIMIS.

import os
import django
import json

# w main zrobić setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openimis-be.openIMIS.openIMIS.settings")
django.setup()
from core.models import Officer, InteractiveUser, User, TechnicalUser
from core.services import create_or_update_user_roles

# from core.test_helpers import create_test_interactive_user


def load_django_settings():
    pass

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def create_interactive_user_from_data(
        user_id,
        user_uuid,
        username=None,
        other_names=None,
        last_name=None,
        birth_certificate_id=None,
        password="Test1234",
        roles=None,
        custom_props=None
):
    if roles is None:
        roles = [3]
    if username is None:
        username = other_names


    # id musi być przechowywane w jsonExt, bo typ danych się różni
    # ew. zmienić typ testowych danych na integer
    i_user = InteractiveUser.objects.create(
        **{
            "language_id": "en",
            "uuid": user_uuid,
            "last_name": last_name,
            "other_names": other_names,
            "login_name": username,
            "audit_user_id": -1,
            "role_id": roles[0]
        }
    )
    i_user.set_password(password)
    i_user.save()
    create_or_update_user_roles(i_user, roles, None)
    return User.objects.create(
        username=username,
        i_user=i_user,
        )


if __name__ == "__main__":
    print("It does work")
    # load_django_settings
    # test_data = load_json_data("../../test-data.json")
    
    print("-------------")
    # for record in test_data["registries"]["records"]:
        # print(record)
        # create_interactive_user_from_data(
        #     user_id=record["id"],
        #     user_uuid=record["uuid"],
        #     username=record["FirstName"],
        #     other_names=record["FirstName"],
        #     last_name=record["LastName"],
        #     birth_certificate_id=None,
        #     password="Test1234",
        #     roles=None,
        #     custom_props=None
        # )
        # print(record["id"], record["uuid"], record["FirstName"], record["FirstName"], record["LastName"])
        # print("------------- end")

    # create_test_interactive_user("Lucas2")
    # print("report_definitions")
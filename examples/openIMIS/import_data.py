import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openimis-be.openIMIS.openIMIS.settings")
django.setup()

from insuree.gql_mutations import update_or_create_gender
from govstack_api.models import Registry
from insuree.models import Insuree, Family, Gender
from django.db import IntegrityError


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def load_parameter_from_custom_parameters(file_path, parameter: str = ""):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return {k: v for k, v in data.items() if k.startswith(f'{parameter}_')}


def create_test_insuree(
        with_family=True, is_head=False, custom_props=None, family_custom_props=None,
        last_name=None, other_names=None, insuree_id=None, insuree_uuid=None, json_ext=None):
    # insuree has a mandatory reference to family and family has a mandatory reference to insuree
    # So we first insert the family with a dummy id and then update it
    print(insuree_uuid)
    if with_family:
        family = Family.objects.create(
            validity_from="2019-01-01",
            head_insuree_id=1,  # dummy
            audit_user_id=-1,
            **(family_custom_props if family_custom_props else {})
        )
    else:
        family = None

    insuree = Insuree.objects.create(
        **{
            "last_name": last_name,
            "id": insuree_id,
            "uuid": insuree_uuid,
            "other_names": other_names,
            "chf_id": str(insuree_id),
            "family": Family.objects.get(id=1),
            "gender": Gender.objects.get(code='M'),
            "dob": "1920-04-02",
            "head": is_head,
            "card_issued": False,
            "validity_from": "2019-01-01",
            "audit_user_id": -1,
            "json_ext": json_ext,
            **(custom_props if custom_props else {})
        }
    )
    if with_family:
        family.head_insuree_id = insuree.id
        if family_custom_props:
            for k, v in family_custom_props.items():
                setattr(family, k, v)
        family.save()

    insuree.save()
    return insuree


def create_gender(user, data):
    update_or_create_gender(data, user)


def create_default_registry(registry_name=None, version=None, class_name=None, model=None,
                            fields_mapping=None, special_fields=None, default_values=None,
                            mutations=None, queries=None, id_field=None):
    default_args = {
        "registry_name": 'registryname',
        "version": '111',
        "class_name": 'InsureeRegistry',
        "model": 'Insuree',
        "fields_mapping": {"ID": "id", "uuid": "uuid", "LastName": "lastName", "FirstName": "otherNames"},
        "special_fields": ["BirthCertificateID", "PersonalData"],
        "default_values": {
            "dob": 'dob: "1920-04-02"',
            "head": "head: false",
            "family_id": "familyId: 1",
            "gender_id": "genderId: \"M\"",
            "card_issued": "cardIssued: false"
        },
        "mutations": {"create": "createInsuree", "delete": "deleteInsurees", "update": "updateInsuree"},
        "queries": {"get": "insurees"},
        "id_field": "chfId",
    }

    registry = Registry.objects.create(
        registry_name=registry_name if registry_name is not None else default_args["registry_name"],
        version=version if version is not None else default_args["version"],
        class_name=class_name if class_name is not None else default_args["class_name"],
        model=model if model is not None else default_args["model"],
        fields_mapping=fields_mapping if fields_mapping is not None else default_args["fields_mapping"],
        special_fields=special_fields if special_fields is not None else default_args["special_fields"],
        default_values=default_values if default_values is not None else default_args["default_values"],
        mutations=mutations if mutations is not None else default_args["mutations"],
        queries=queries if queries is not None else default_args["queries"],
        id_field=id_field if id_field is not None else default_args["id_field"]
    )
    registry.save()
    print("Registry has been successfully saved to the database")


if __name__ == "__main__":
    test_data = load_json_data("../../test-data.json")
    create_default_registry()
    id_data = load_parameter_from_custom_parameters(file_path="testCustomParameters.json", parameter="ID")
    for index, record in enumerate(test_data["registries"]["records"]):
        insuree_id = id_data.get(f"ID_{index + 1}", record.pop("id"))
        try:
            insuree = create_test_insuree(
                insuree_id=insuree_id,
                last_name=record.pop('LastName'),
                other_names=record.pop('FirstName'),
                insuree_uuid=record.pop('uuid'),
                json_ext=record
            )
        except IntegrityError as e:
            print(f"Error while creating insuree for ID {insuree_id}. Error: {str(e)}")

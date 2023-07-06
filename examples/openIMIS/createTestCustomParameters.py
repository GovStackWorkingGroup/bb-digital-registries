import requests
import json

data_dict = {}

def get_tokens():
    global data_dict
    response = requests.post("http://localhost:8000/login/")
    response_data = response.json()

    data_dict["csrf_token"] = response_data["csrf_token"]
    data_dict["jwt_token"] = response_data["jwt_token"]

def add_to_dict(dict_default_values):
    global data_dict
    data_dict.update(dict_default_values)

def save_to_file():
    with open("testCustomParameters.json", "w") as json_file:
        json.dump(data_dict, json_file)


if __name__ == "__main__":
    print("Creating custom paramerers for test suite")
    get_tokens()
    add_to_dict({"ID_1": '"0000012345"'})
    add_to_dict({"ID_2": '"0000012346"'})
    save_to_file()
    print("data dict:", data_dict)


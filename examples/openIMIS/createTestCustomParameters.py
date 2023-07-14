import requests
import json

class CustomParamManager:
    def __init__(self):
        self.params = {}

    def fetch_tokens(self):
        response = requests.post("http://localhost:8000/login/")
        response_data = response.json()
        self.params["csrf_token"] = response_data["csrf_token"]
        self.params["jwt_token"] = response_data["jwt_token"]

    def add_params(self, new_params):
        self.params.update(new_params)

    def save_to_file(self):
        with open("testCustomParameters.json", "w") as json_file:
            json.dump(self.params, json_file)

    def show_params(self):
        print("Params:", self.params)


if __name__ == "__main__":
    print("Creating custom parameters for test suite")
    param_manager = CustomParamManager()
    param_manager.fetch_tokens()
    default_values = [
        {"ID_1": "12345"},
        {"ID_2": "12346"},
        {"ID_3": "12346"},
        {"ID_4": "12346"},
    ]
    for default_value in default_values:
        param_manager.add_params(default_value)
    param_manager.save_to_file()



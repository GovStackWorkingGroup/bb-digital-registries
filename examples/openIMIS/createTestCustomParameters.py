import requests
import json
import os 
class CustomParamManager:
    def __init__(self):
        self.params = {}

    def fetch_tokens(self):
        response = requests.post("http://localhost:3333/api/login/")
        print(response)
        response_data = response.json()
        self.params["csrf_token"] = response_data["csrf_token"]
        self.params["jwt_token"] = response_data["jwt_token"]

    def add_params(self, new_params_list):
        for new_params in new_params_list:
            self.params.update(new_params)

    def save_to_file(self):
        with open("testCustomParameters.json", "w") as json_file:
            json.dump(self.params, json_file)

    def show_params(self):
        print("Params:", self.params)


if __name__ == "__main__":
    try:
        print("Creating custom parameters for test suite")
        param_manager = CustomParamManager()
        # param_manager.fetch_tokens()

        id_parameters = [{"ID_" + str(i): str(1999 + i - 1)} for i in range(0, 35)]

        first_name_parameters = [
            {"FirstName_0": "Anna"},
            {"FirstName_1": "Zofia"},
            {"FirstName_2": "Elsa"},
            {"FirstName_3": "Nick"},
            {"FirstName_4": "Thomas"},
        ]

        last_name_parameters = [
            {"LastName_0": "Stock"},
            {"LastName_1": "Don"},
            {"LastName_2": "Smith"},
            {"LastName_3": "Evans"},
            {"LastName_4": "Johnson"},
        ]

        birth_certificate_id = [
            {"BirthCertificateID_0": "RR-1234567999"},
            {"BirthCertificateID_1": "RR-5465679229"},
            {"BirthCertificateID_2": "RR-1234537999"},
            {"BirthCertificateID_3": "RR-7898797999"},
            {"BirthCertificateID_4": "RR-8534567781"},
        ]

        param_manager.add_params(id_parameters)
        param_manager.add_params(first_name_parameters)
        param_manager.add_params(last_name_parameters)
        param_manager.add_params(birth_certificate_id)
        param_manager.save_to_file()
        print("Custom parameters created.")
    except Exception as e: 
        import traceback
        print("Failed to create custom parameters. Error:")
        traceback.print_exc()
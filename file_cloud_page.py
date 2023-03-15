import requests


class FileCloudPage:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session_id = self.get_session_id()

    def get_session_id(self):
        url = f"{self.base_url}/admin/adminlogin"
        credentials = {
            "username": self.username,
            "password": self.password,
        }
        response = requests.post(url, data=credentials)
        return response.text.strip()

    def create_folder(self, folder_name):
        create_folder_url = f"{self.base_url}/admin/setteamfolderuser"
        data = {
            "sessionid": self.session_id,
            "path": f"/My Files/{folder_name}",
        }
        response = requests.post(create_folder_url, data=data)
        return response

    def create_group(self, group_name):
        create_group_url = f"{self.base_url}/admin/addgroup"
        data = {
            "sessionid": self.session_id,
            "name": group_name,
        }
        response = requests.post(create_group_url, data=data)
        return response

    def create_user(self, user_data):
        create_user_url = f"{self.base_url}/admin/adduser"
        response = requests.post(create_user_url, data=user_data)
        return response

    def create_role(self, role_name, privileges):
        create_role_url = f"{self.base_url}/admin/addroleuser"
        data = {
            "sessionid": self.session_id,
            "name": role_name,
            "privileges": privileges,
        }
        response = requests.post(create_role_url, data=data)
        return response

    def update_user_role(self, user_name, role_name):
        update_user_role_url = f"{self.base_url}/core/updateroleifany"
        data = {
            "sessionid": self.session_id,
            "username": user_name,
            "role": role_name,
        }
        response = requests.post(update_user_role_url, data=data)
        return response

    def add_user_to_group(self, user_name, group_name):
        add_user_to_group_url = f"{self.base_url}/admin/addmembertogroup"
        data = {
            "sessionid": self.session_id,
            "username": user_name,
            "groupname": group_name,
        }
        response = requests.post(add_user_to_group_url, data=data)
        return response

    def upload_file(self, filepath, filename):
        url = f"{self.base_url}/core/upload"
        with open(filepath, "rb") as file:
            files = {"file": (filename, file)}
            data = {"sessionid": self.session_id}
            response = requests.post(url, files=files, data=data)
        return response

    def get_file_versions(self, filename):
        url = f"{self.base_url}/core/getversions"
        data = {
            "sessionid": self.session_id,
            "path": f"/My Files/{filename}",
        }
        response = requests.post(url, data=data)
        return response.json()

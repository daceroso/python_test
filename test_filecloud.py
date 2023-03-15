import pytest
from file_cloud_page import FileCloudPage

filecloud_base_url = "https://daceros.filecloudonline.com"
username = "daceros19"
password = "jMEW6GVN"
test_filepath = "./test.odt"

filecloud_page = FileCloudPage(filecloud_base_url, username, password)

groups_users = {
    "Accounting": ["Henderson Nakashima", "Biserka Wilkie", "Giltbert Thatcher", "Octavia Blanchard", "Dawid Morel"],
    "Operations": ["Zülfikar Aafjes", "Vlasi Szilágyi", "Madelyn Donne", "Şule Zima", "Rehema Barr"],
    "Engineering": ["Awee Murdoch", "Tsholofelo Boer", "Mari Winthrop"],
    "Consultants": ["Dragoslav Echevarría", "Kaley Petrov"],
}


@pytest.mark.parametrize("group, users", groups_users.items())
def test_import_users(group, users):
    response = filecloud_page.create_group(group)
    assert response.status_code in (200, 409), f"Failed to create group '{group}'."

    response = filecloud_page.create_folder(group)
    assert response.status_code in (200, 409), f"Failed to create folder for group '{group}'."

    if group == "Consultants":
        limited_privileges = "R"
        response = filecloud_page.create_role("ConsultantLimited", limited_privileges)
        assert response.status_code in (200, 409), "Failed to create limited role for consultants."

    for user in users:
        user_data = {
            "sessionid": filecloud_page.session_id,
            "username": user,

        }
        response = filecloud_page.create_user(user_data)
        assert response.status_code == 200, f"Failed to create user '{user}'."

        response = filecloud_page.add_user_to_group(user, group)
        assert response.status_code == 200, f"Failed to add user '{user}' to the '{group}' group."

        if group == "Consultants":
            response = filecloud_page.update_user_role(user, "ConsultantLimited")
            assert response.status_code == 200, f"Failed to assign limited role to consultant user '{user}'."


def test_docx_storage_and_versioning():
    response = filecloud_page.upload_file(test_filepath, "test.odt")
    assert response.status_code == 200, "Failed to upload the file for the first time."

    response = filecloud_page.upload_file(test_filepath, "test.odt")
    assert response.status_code == 200, "Failed to upload the file for the second time."

    versions = filecloud_page.get_file_versions("test.odt")
    assert len(versions) >= 2, "The file should have at least 2 versions after uploading twice."


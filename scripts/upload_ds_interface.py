import requests
import hashlib


def dasai_upload(fr, file_path):
    login_url = "http://122.190.50.75:64053/predpower/userlogin"

    login_data = {
        'username': "yccs-085",
        'password': hashlib.md5("NMDR_zyfg001".encode('utf-8')).hexdigest()
    }

    login_response = requests.post(login_url, data=login_data)

    cookie_token = login_response.json().get('data').get('CookieToken')

    upload_url = "http://122.190.50.75:64053/predpower/uploaddata"

    headers = {
        'token': cookie_token
    }

    data = {
        'siteid': f'{fr}'
    }

    # file_path = 'data/output/dasai/D_DQ_20240815.csv'

    files = {
        'file': open(file_path, 'rb')
    }

    upload_response = requests.post(upload_url, headers=headers, data=data, files=files)

    return upload_response.json()


if __name__ == "__main__":
    file_path = 'data/output/dasai/D_DQ_20240815.csv'
    dasai_upload('D', file_path)

import os
import requests
import json
import sys


def get_config(app_name, apps_conf):
    with open(apps_conf, 'r') as f:
        apps = json.load(f)["Apps"]
        for app in apps:
            if app["Name"] == app_name:
                return app["Config"]
    return None

def get_name():
    for arg in sys.argv:
        if arg.startswith('--s_name='):
            return arg.split('=')[1]
    return None


def send_post_request():
    addr = os.environ.get("FANLIGHT_BACKEND")
    port = os.environ.get("FANLIGHT_BACKEND_PORT")
    desktop_id = os.environ.get("DESKTOP_ID")
    url = 'http://{}:{}/desktops/{}/apps'.format(addr, port, desktop_id)
    headers = {'Content-Type': 'application/json'}

    app_name = get_name()
    config = get_config(app_name, os.getenv('APPS_CONF'))
    payload = {
        "AppName": app_name,
        "Config": config
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print('POST request sent successfully!')
    else:
        print('Failed to send POST request:', response.status_code)


if __name__ == '__main__':
    send_post_request()

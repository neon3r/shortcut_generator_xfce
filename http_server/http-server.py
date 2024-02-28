import sys
from flask import Flask, request

app = Flask(__name__)


@app.route('/desktops/<desktop_id>/apps', methods=['POST'])
def handle_post_request(desktop_id):
    app_name = request.json.get('AppName')
    config = request.json.get('Config')

    print(f'Received POST request from desktop {desktop_id} with AppName: {app_name} and Config: {config}', flush=True)

    return 'POST request received successfully!', 200


if __name__ == '__main__':
    app.run(host='172.17.0.2', port=5000)

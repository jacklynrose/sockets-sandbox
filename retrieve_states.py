import requests

server_url = 'http://192.168.0.139:5050'

def get_state():
    try:
        response = requests.get('http://192.168.0.139:5050/get')  # Replace <your_server_address> with the actual address of your server
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching state: {e}")
        return None

app_state = get_state()

if app_state is not None:
    print("Current state:")
    print(app_state)
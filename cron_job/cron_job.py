import requests

def trigger_update():
    try:
        url = "http://127.0.0.1:5000/update_data"  
        response = requests.get(url)
        if response.status_code == 200:
            return "Data updated successfully."
        else:
            return f"Failed to update data. Status code: {response.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"

trigger_update()
import requests

# DELIGHT_COOK_TOKEN_URL = "http://127.0.0.1:8080/token"

DELIGHT_COOK_BASE_URL = "http://127.0.0.1:8080"  

def get_token():
    token_response = requests.post(f"{DELIGHT_COOK_BASE_URL}/token", data={
        'username': 'marvel', 
        'password': '12345678'
    })
    if token_response.status_code == 200:
        token = token_response.json().get('access_token')
        return token
    else:
        print("Failed to fetch token:", token_response.status_code, token_response.text)
        return None

#get composition
def get_compositions_from_delight_cook():
    token = get_token()
    if not token:
        print("No token available")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{DELIGHT_COOK_BASE_URL}/composition", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch compositions:", response.status_code, response.text)
        return None

#Get menu
def get_menu_from_delight_cook():
    token = get_token()
    if not token:
        print("No token available")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{DELIGHT_COOK_BASE_URL}/menu_items", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch menu_items:", response.status_code, response.text)
        return None
    
#Get Ingredients
def get_ingredients_from_delight_cook():
    token = get_token()
    if not token:
        print("No token available")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{DELIGHT_COOK_BASE_URL}/ingredients", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch ingredients:", response.status_code, response.text)
        return None
    
#Get Customization
def get_customization_from_delight_cook():
    token = get_token()
    if not token:
        print("No token available")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{DELIGHT_COOK_BASE_URL}/customization", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch customization:", response.status_code, response.text)
        return None
    
#get Order 
def get_order_from_delight_cook():
    token = get_token()
    if not token:
        print("No token available")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{DELIGHT_COOK_BASE_URL}/order", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch order:", response.status_code, response.text)
        return None

#Post Order 
def post_order_to_delight_cook(order_details):
    token = get_token()
    if not token:
        print("No token available")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{DELIGHT_COOK_BASE_URL}/order",
        headers=headers,
        json=order_details  # Assuming 'order_details' is a dictionary
    )
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to post order:", response.status_code, response.text)
        return None
    


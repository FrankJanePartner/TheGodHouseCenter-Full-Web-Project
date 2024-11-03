import json
import requests
from requests import Session
from pprint import pprint as pp

API_KEY = "sb_prod_2a8af1e94ad5f1e5e721552aa1ba34f2e4ac03b88a9a2916e86d022a835163e9"
BASE_URL = "https://api.shipbubble.com/v1/shipping/"

class ShipBubble:
    def __init__(self, API_KEY):
        self.base_url = BASE_URL
        self.headers = {
            "Accepts": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        self.session = Session()
        self.session.headers.update(self.headers)

    def getBalance(self):
        url = f"{self.base_url}/wallet/balance"
        response = self.session.get(url, timeout=(5, 30))
        return response.json()

    def validateAddress(self, name, email, phone, address):
        url = f"{self.base_url}/address/validate"
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
        }
        response = self.session.post(url, json=payload, timeout=(5, 30))
        return response.json()

    def getValidatedAddress(self):
        url = f"{self.base_url}/address"
        response = self.session.get(url, timeout=(5, 30))
        return response.json()

    def editAddress(self, address_code, name, email, phone, address):
        url = f"{self.base_url}/address/{address_code}"
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
        }
        response = self.session.patch(url, json=payload, timeout=(5, 30))
        return response.json()


    def getAddressDetails(self, address_code):
        url = f"{self.base_url}/address/{address_code}"
        response = self.session.get(url, timeout=(5, 30))
        return response.json()
    

    def getCategories(self):
        url = f"{self.base_url}/labels/categories"
        response = self.session.get(url, timeout=(5, 30))
        return response.json()
    
    def getDimensions(self):
        url = f"{self.base_url}/labels/boxes"
        response = self.session.get(url, timeout=(5, 30))
        return response.json()
    
    def getCouriers(self):
        url = f"{self.base_url}/couriers"
        response = self.session.get(url, timeout=(5, 30))
        return response.json()
    
    def getShippingRate(self, sender_address_code, recipient_address_code, pickup_date, category_id, package_items, delivery_instructions, package_dimension, service_type):
        url = f"{self.base_url}/fetch_rates"
        data = {
            "sender_address_code": sender_address_code,
            "reciever_address_code": recipient_address_code,
            "pickup_date": pickup_date,
            "category_id": category_id,
            "package_items": package_items,
            "package_dimension": package_dimension,
            "delivery_instructions": delivery_instructions,
            'service_type': service_type,
        }

        response = self.session.post(url, json=data, timeout=(5, 30))
        return response.json()
    

    def getRateDetails(self, service_codes):
        url = f"{self.base_url}/fetch_rates?{service_codes}"
        response = self.session.get(url, timeout=(5, 30))
        return response.json()

    def editrates(self, request_token, sender_name, sender_phone, reciever_name, reciever_phone):
            url = f"{self.base_url}/fetch_rates/request_token"
            data = {
                "request_token": request_token,
                "sender_name": sender_name,
                "sender_phone": sender_phone,
                "reciever_name": reciever_name,
                "reciever_phone": reciever_phone,
            }


            response = self.session.patch(url, json=data, timeout=(5, 30))
            return response.json()

    def getInsuranceRates(self, request_token):
        url = f"{self.base_url}/fetch_rates?{request_token}"
        response = self.session.get(url, timeout=(5, 30))
        return response.json()

    def createShipment(self, request_token, service_code, courier_id, insurance_code):
        url = f"{self.base_url}/shipping/labels"
        data = {
            "request_token": request_token,
            "service_code": service_code,
            "courier_id": courier_id,
            "insurance_code": insurance_code,
        }

        response = self.session.post(url, json=data, timeout=(5, 30))
        return response.json()
# delhivery_config.py
import requests
import json
import base64

class DelhiveryAPI:
    def __init__(self):
        self.base_url = "https://track.delhivery.com"  # Production URL
        self.api_key = "YOUR_DELHIVERY_API_KEY"  # Get from Delhivery dashboard
        self.pickup_address = {
            "name": "Ecomonks",
            "address": "Yathisha Bliss No 9/329, Moorkanikkara Kozhukully PO",
            "city": "Thrissur",
            "state": "Kerala",
            "pincode": "680752",
            "phone": "9845736584"
        }
        
    def create_shipment(self, order_data):
        """Create a shipment in Delhivery"""
        
        # Prepare shipment data
        shipment_data = {
            "shipment": {
                "pickup_location": {
                    "name": self.pickup_address["name"],
                    "address": self.pickup_address["address"],
                    "city": self.pickup_address["city"],
                    "state": self.pickup_address["state"],
                    "pincode": self.pickup_address["pincode"],
                    "phone": self.pickup_address["phone"]
                },
                "waybill": order_data.get('waybill', ''),
                "customer_details": {
                    "name": order_data["customer_name"],
                    "phone": order_data["phone"],
                    "address": order_data["address"],
                    "city": order_data.get("city", ""),
                    "state": order_data.get("state", ""),
                    "pincode": order_data.get("pincode", ""),
                    "country": "India"
                },
                "shipment_products": [
                    {
                        "name": "Divya Bhimseni Karpooram",
                        "sku": order_data.get("sku", "KARP-01"),
                        "quantity": 1,
                        "price": str(order_data.get("amount", 0))
                    }
                ],
                "cod_amount": "0",  # Set to amount if COD
                "order_id": order_data["order_id"],
                "length": "10",
                "breadth": "10",
                "height": "10",
                "weight": order_data.get("weight", "0.5"),
                "invoice_number": order_data.get("invoice_no", ""),
                "client_id": "ECOMONKS"
            }
        }
        
        # API call
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/cmu/create.json",
                json=shipment_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Delhivery API Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error creating shipment: {str(e)}")
            return None
    
    def get_shipping_rates(self, pincode, weight=0.5):
        """Get shipping rates from Delhivery"""
        
        payload = {
            "pickup_pincode": self.pickup_address["pincode"],
            "delivery_pincode": pincode,
            "weight": weight,
            "cod": "0"
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/packing/charges",
                params=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error getting rates: {str(e)}")
            return None
    
    def generate_waybill(self):
        """Generate a waybill number"""
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/waybill/generate",
                params={"count": "1"},
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('waybill', [])
            return None
            
        except Exception as e:
            print(f"Error generating waybill: {str(e)}")
            return None
    
    def print_label(self, waybill):
        """Generate shipping label"""
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/print",
                params={"waybill": waybill, "format": "pdf"},
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.content  # Returns PDF data
            return None
            
        except Exception as e:
            print(f"Error generating label: {str(e)}")
            return None
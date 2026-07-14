import requests
import json


class DelhiveryAPI:

    def __init__(self):

        print("=" * 80)
        print("Initializing Delhivery API")

        # Change to staging if testing
        # self.base_url = "https://staging-express.delhivery.com"

        # Production
        self.base_url = "https://track.delhivery.com"

        self.api_key = "f04f6bba55ca9b7346a7959b01da41182c786083"

        self.pickup_address = {
            "name": "yathisha",
            "address": "Global Avenue Opp SIB Aranattukara Branch Thoppinmoola Poothole",
            "city": "Thrissur",
            "state": "Kerala",
            "pincode": "680004",
            "phone": "7204610007"
        }

        print("Base URL :", self.base_url)
        print("Token    :", self.api_key[:8] + "********")
        print("=" * 80)

    # -------------------------------------------------------
    # COMMON HEADERS
    # -------------------------------------------------------

    def headers(self):

        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    # -------------------------------------------------------
    # WAYBILL
    # -------------------------------------------------------

    def generate_waybill(self):

        url = f"{self.base_url}/waybill/api/fetch/json/"

        response = requests.get(
            url,
            params={"count": 1},
            headers=self.headers()
        )

        print(response.status_code)
        print(response.text)

        if response.status_code == 200:

            waybill = response.json()

            print("Waybill:", waybill)

            return waybill

        return None

    # -------------------------------------------------------
    # CREATE SHIPMENT
    # -------------------------------------------------------

    def create_shipment(self, order_data):

        print("\n" + "=" * 80)
        print("CREATE SHIPMENT")

        url = f"{self.base_url}/api/cmu/create.json"

        shipment = {
            "shipment": {

                "pickup_location": self.pickup_address,

                "waybill": order_data.get("waybill", ""),

                "customer_details": {

                    "name": order_data["customer_name"],
                    "phone": order_data["phone"],

                    "address": order_data["address"],
                    "city": order_data["city"],
                    "state": order_data["state"],
                    "pincode": order_data["pincode"],
                    "country": "India"
                },

                "shipment_products": [

                    {
                        "name": "Divya Bhimseni Karpooram",
                        "sku": "KARP-01",
                        "quantity": 1,
                        "price": str(order_data.get("amount", 0))
                    }

                ],

                "cod_amount": "0",

                "order_id": order_data["order_id"],

                "length": "10",
                "breadth": "10",
                "height": "10",
                "weight": order_data.get("weight", "0.5"),

                "invoice_number": order_data.get("invoice_no", ""),

                "client_id": "ECOMONKS"
            }
        }

        print("URL")
        print(url)

        print("\nHeaders")
        print(self.headers())

        print("\nShipment JSON")
        print(json.dumps(shipment, indent=4))

        try:

            payload = {
                "format": "json",
                "data": json.dumps(shipment)
            }

            headers = {
                "Authorization": f"Token {self.api_key}"
            }

            response = requests.post(
                url,
                data=payload,
                headers=headers,
                timeout=60
            )

            print("\nHTTP STATUS :", response.status_code)

            print("\nRESPONSE")
            print(response.text)

            result = response.json()

            print(json.dumps(result, indent=4))

            if result.get("success"):
                print("Shipment Created Successfully")
            else:
                print("Shipment Creation Failed")
                print(result)

            return result
        except Exception as e:

            print("CREATE SHIPMENT ERROR")
            print(e)

            return None

    # -------------------------------------------------------
    # PINCODE CHECK
    # -------------------------------------------------------

    def check_pincode(self, pincode):

        print("\nChecking Pincode")

        url = f"{self.base_url}/c/api/pin-codes/json/"

        params = {
            "filter_codes": pincode
        }

        print(url)

        try:

            response = requests.get(
                url,
                params=params,
                headers=self.headers(),
                timeout=30
            )

            print(response.status_code)
            print(response.text)

            return response.json()

        except Exception as e:

            print(e)

            return None

    # -------------------------------------------------------
    # SHIPPING CHARGES
    # -------------------------------------------------------

    def get_shipping_rates(self, pincode, weight=0.5):

        url = f"{self.base_url}/api/packing/charges"

        params = {
            "pickup_pincode": self.pickup_address["pincode"],
            "delivery_pincode": pincode,
            "weight": weight,
            "cod": 0
        }

        print("\nShipping Charges")

        print(url)

        try:

            response = requests.get(
                url,
                params=params,
                headers=self.headers(),
                timeout=30
            )

            print(response.status_code)
            print(response.text)

            return response.json()

        except Exception as e:

            print(e)

            return None

    # -------------------------------------------------------
    # LABEL
    # -------------------------------------------------------

    def print_label(self, waybill):

        url = f"{self.base_url}/api/p/packing/slip"

        params = {
            "wbns": waybill
        }

        print("\nGenerating Label")

        print(url)

        try:

            response = requests.get(
                url,
                params=params,
                headers=self.headers(),
                timeout=30
            )

            print(response.status_code)

            if response.status_code == 200:

                return response.content

            print(response.text)

            return None

        except Exception as e:

            print(e)

            return None
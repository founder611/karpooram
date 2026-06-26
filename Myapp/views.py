# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from django.shortcuts import render
# from django.shortcuts import redirect
# from django.http import HttpResponse
# from django.core.mail import send_mail
# from django.shortcuts import render
# from django.http import HttpResponse
# import smtplib
# from openpyxl import Workbook, load_workbook
# from datetime import datetime

# import requests


# def homepage(request):
#     return render(request,'updatehome.html')


# def order_post(request):

#     name = request.POST['name']
#     email = request.POST['email']
#     phone = request.POST['phone']
#     address = request.POST['address']
#     quantity = request.POST['quantity']

#     print(name,email,phone,address,quantity,"fffffffffffffffffff")

#     if quantity == "50g":
#         amount = 1 * 100   # Razorpay uses paise

#     elif quantity == "200g":
#         amount = 1 * 100

#     else:
#         amount = 0

#     return render(request, 'pp.html', {

#         'name': name,
#         'email': email,
#         'phone': phone,
#         'address': address,
#         'quantity': quantity,
#         'amount': amount,
#         'razorpay_api_key': 'rzp_live_Su35EVyNYFeKCF',
#         'currency': 'INR'

#     })


# def raz_pay(request, amount):

#     import razorpay

#     razorpay_api_key = "rzp_live_Su35EVyNYFeKCF"
#     razorpay_secret_key = "NQE3JfS6rdlmp8YtHrxF120H"

#     razorpay_client = razorpay.Client(
#         auth=(razorpay_api_key, razorpay_secret_key)
#     )

#     amount = float(amount)

#     order_data = {
#         'amount': amount,
#         'currency': 'INR',
#         'receipt': 'order_rcptid_11',
#         'payment_capture': '1',
#     }

#     order = razorpay_client.order.create(data=order_data)

#     return render(request, 'pp.html', {

#         'razorpay_api_key': razorpay_api_key,
#         'amount': order_data['amount'],
#         'currency': order_data['currency'],
#         'order_id': order['id']

#     })


# def userpayment_post(request):

#     if request.method == "POST":

#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         quantity = request.POST.get('quantity')
#         payment_id = request.POST.get('payment_id')

#         if not email:
#             return HttpResponse("Email not found")

#         try:

#             # ==========================================
#             # CUSTOMER HTML EMAIL
#             # ==========================================

#             customer_html = f"""
#             <html>

#             <body style="font-family: Arial; background:#f4f4f4; padding:30px;">

#             <div style="
#             max-width:600px;
#             margin:auto;
#             background:white;
#             border-radius:15px;
#             padding:30px;
#             box-shadow:0 0 10px rgba(0,0,0,0.1);
#             ">

#             <h1 style="color:#0b7d45; text-align:center;">
#             🌿 ECOMONKS
#             </h1>

#             <h2 style="color:#222;">
#             Thank You For Your Order
#             </h2>

#             <p style="font-size:16px; color:#555;">
#             Dear <b>{name}</b>,
#             </p>

#             <p style="font-size:16px; color:#555;">
#             Your payment has been received successfully and your order is confirmed.
#             </p>

#             <div style="
#             background:#f7fff9;
#             border:1px solid #d4f5dd;
#             padding:20px;
#             border-radius:10px;
#             margin-top:20px;
#             ">

#             <h3 style="color:#0b7d45;">
#             🧾 Order Details
#             </h3>

#             <p><b>👤 Name:</b> {name}</p>

#             <p><b>📧 Email:</b> {email}</p>

#             <p><b>📞 Phone:</b> {phone}</p>

#             <p><b>📍 Address:</b> {address}</p>

#             <p><b>📦 Quantity:</b> {quantity}</p>

#             <p><b>💳 Payment ID:</b> {payment_id}</p>

#             </div>

#             <p style="
#             margin-top:25px;
#             font-size:16px;
#             color:#444;
#             ">
#             We truly appreciate your support and trust in ECOMONKS.
#             </p>

#             <div style="
#             margin-top:30px;
#             background:#0b7d45;
#             color:white;
#             padding:15px;
#             border-radius:10px;
#             text-align:center;
#             ">

#             Thank you for shopping with us ❤️

#             </div>

#             </div>

#             </body>

#             </html>
#             """

#             # ==========================================
#             # SMTP SERVER
#             # ==========================================

#             server = smtplib.SMTP('smtp.gmail.com', 587)

#             server.starttls()

#             server.ehlo()

#             server.login(
#                 "founder@ecomonks.in",
#                 "crmwddzdzoqatofz"
#             )

#             # ==========================================
#             # CUSTOMER EMAIL
#             # ==========================================

#             customer_msg = MIMEMultipart()

#             customer_msg['From'] = "founder@ecomonks.in"

#             customer_msg['To'] = email

#             customer_msg['Subject'] = "ECOMONKS Order Confirmation"

#             customer_msg.attach(
#                 MIMEText(customer_html, 'html', 'utf-8')
#             )

#             server.sendmail(
#                 "founder@ecomonks.in",
#                 email,
#                 customer_msg.as_string()
#             )

#             # ==========================================
#             # ADMIN EMAIL
#             # ==========================================

#             admin_html = f"""
#             <html>

#             <body style="font-family: Arial; background:#f4f4f4; padding:30px;">

#             <div style="
#             max-width:600px;
#             margin:auto;
#             background:white;
#             border-radius:15px;
#             padding:30px;
#             box-shadow:0 0 10px rgba(0,0,0,0.1);
#             ">

#             <h1 style="color:#d62828; text-align:center;">
#             🚨 NEW ORDER RECEIVED
#             </h1>

#             <div style="
#             background:#fff5f5;
#             border:1px solid #ffd6d6;
#             padding:20px;
#             border-radius:10px;
#             margin-top:20px;
#             ">

#             <p><b>👤 Customer Name:</b> {name}</p>

#             <p><b>📧 Email:</b> {email}</p>

#             <p><b>📞 Phone:</b> {phone}</p>

#             <p><b>📍 Address:</b> {address}</p>

#             <p><b>📦 Quantity:</b> {quantity}</p>

#             <p><b>💳 Payment ID:</b> {payment_id}</p>

#             </div>

#             <div style="
#             margin-top:30px;
#             background:#0b7d45;
#             color:white;
#             padding:15px;
#             border-radius:10px;
#             text-align:center;
#             ">

#             ✅ PAYMENT SUCCESSFUL

#             </div>

#             </div>

#             </body>

#             </html>
#             """

#             admin_msg = MIMEMultipart()

#             admin_msg['From'] = "founder@ecomonks.in"

#             admin_msg['To'] = "founder@ecomonks.in"

#             admin_msg['Subject'] = "New ECOMONKS Order Received"

#             admin_msg.attach(
#                 MIMEText(admin_html, 'html', 'utf-8')
#             )

#             server.sendmail(
#                 "founder@ecomonks.in",
#                 "founder@ecomonks.in",
#                 admin_msg.as_string()
#             )

#             server.quit()


#             # SAVE TO EXCEL
#             save_order_to_excel(
#                 name,
#                 email,
#                 phone,
#                 address,
#                 quantity,
#                 payment_id
#             )

#             # SEND WHATSAPP MESSAGE
#             send_whatsapp_message(
#                 name,
#                 phone,
#                 quantity
#             )

#             return HttpResponse("""
#             <script>
#             alert('Payment Successful & Email Sent');
#             window.location='/';
#             </script>
#             """)

#         except Exception as e:

#             return HttpResponse(f"ERROR: {e}")

#     return HttpResponse("Invalid Request")


# # ==========================================
# # SAVE ORDER TO SUPABASE
# # ==========================================
# from supabase import create_client
# from datetime import datetime

# def save_order_to_excel(name, email, phone, address, quantity, payment_id):
#     try:
#         # Your Supabase credentials - DIRECTLY (not from environment)
#         supabase_url = "https://fgikrpxjaskyduewekiu.supabase.co"
#         supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZnaWtycHhqYXNreWR1ZXdla2l1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAzNTg3MDUsImV4cCI6MjA5NTkzNDcwNX0.kyIphJzU-gNIEvA2rXAWAKy6lC4Vur362U2lFWm6BtI"
        
#         # Create client
#         supabase = create_client(supabase_url, supabase_key)
        
#         # Get next order number
#         try:
#             result = supabase.table('orders').select('order_no', count='exact').execute()
#             order_no = result.count + 1 if result.count else 1
#         except:
#             order_no = 1
        
#         # Insert order
#         supabase.table('orders').insert({
#             "order_no": order_no,
#             "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "customer_name": name,
#             "email": email,
#             "phone": phone,
#             "address": address,
#             "quantity": quantity,
#             "payment_id": payment_id
#         }).execute()
        
#         print(f"✅ Order #{order_no} saved to Supabase")
#         return True
        
#     except Exception as e:
#         print(f"❌ Supabase error: {e}")
#         return False


# # ==========================================
# # SEND WHATSAPP MESSAGE USING WATI
# # ==========================================

# def send_whatsapp_message(name, phone, quantity):

#     # REMOVE SPACES / +91
#     phone = phone.replace(" ", "").replace("+91", "")

#     url = f"https://live-mt-server.wati.io/12345/api/v1/sendTemplateMessage?whatsappNumber=91{phone}"

#     payload = {
#         "template_name": "order_confirmation",
#         "broadcast_name": "order_confirmation",
#         "parameters": [
#             {
#                 "name": "name",
#                 "value": name
#             },
#             {
#                 "name": "quantity",
#                 "value": quantity
#             }
#         ]
#     }

#     headers = {
#         "Authorization": "wati_f8ed980e-5142-424a-9096-7cb7b2a40bd3.pUd4YizkgaTv3b1hRdnRjpIMRcObEZ9udOuJ6hN2L0_FptY3fKsysDz8Skt30_ziCCNiYbn4FsD0YbmN4OP8jpVDCwpN2scUSqq28QMUwtWjWmMjdxIJNPL8EQIRE3bt",
#         "Content-Type": "application/json"
#     }

#     try:

#         response = requests.post(
#             url,
#             json=payload,
#             headers=headers
#         )

#         print("WATI RESPONSE:")
#         print(response.status_code)
#         print(response.text)

#     except Exception as e:

#         print("WhatsApp Error:", e)





# # ==========================================
# # SUBSCRIPTION EMAIL FUNCTION
# # ==========================================

# def emailenquiry(request):

#     if request.method == "POST":

#         email = request.POST.get('email')

#         try:

#             subscription_html = f"""
#             <html>

#             <body style="font-family: Arial; background:#f4f4f4; padding:30px;">

#             <div style="
#             max-width:600px;
#             margin:auto;
#             background:white;
#             border-radius:15px;
#             padding:30px;
#             box-shadow:0 0 10px rgba(0,0,0,0.1);
#             ">

#             <h1 style="color:#0b7d45; text-align:center;">
#             🌿 Welcome to ECOMONKS
#             </h1>

#             <p style="font-size:16px; color:#555;">
#             Thank you for subscribing to ECOMONKS.
#             </p>

#             <p style="font-size:16px; color:#555;">
#             We are excited to have you as part of our growing family ❤️
#             </p>

#             <div style="
#             background:#f7fff9;
#             border:1px solid #d4f5dd;
#             padding:20px;
#             border-radius:10px;
#             margin-top:20px;
#             ">

#             <h3 style="color:#0b7d45;">
#             ✨ What You Will Receive
#             </h3>

#             <p>🛍️ Exclusive Product Updates</p>

#             <p>🎉 Special Offers & Discounts</p>

#             <p>📢 Latest Announcements</p>

#             <p>🌱 Natural & Traditional Product Information</p>

#             </div>

#             <div style="
#             margin-top:30px;
#             background:#0b7d45;
#             color:white;
#             padding:15px;
#             border-radius:10px;
#             text-align:center;
#             ">

#             Thank You For Staying Connected With Us ❤️

#             </div>

#             </div>

#             </body>

#             </html>
#             """

#             server = smtplib.SMTP('smtp.gmail.com', 587)

#             server.starttls()

#             server.ehlo()

#             server.login(
#                 "founder@ecomonks.in",
#                 "crmwddzdzoqatofz"
#             )

#             # Subscriber Email
#             subscriber_msg = MIMEMultipart()

#             subscriber_msg['From'] = "founder@ecomonks.in"

#             subscriber_msg['To'] = email

#             subscriber_msg['Subject'] = "ECOMONKS Subscription"

#             subscriber_msg.attach(
#                 MIMEText(subscription_html, 'html', 'utf-8')
#             )

#             server.sendmail(
#                 "founder@ecomonks.in",
#                 email,
#                 subscriber_msg.as_string()
#             )

#             # Admin Email
#             admin_html = f"""
#             <html>

#             <body style="font-family: Arial;">

#             <h2>📩 New Subscription Received</h2>

#             <p><b>Subscriber Email:</b> {email}</p>

#             </body>

#             </html>
#             """

#             admin_msg = MIMEMultipart()

#             admin_msg['From'] = "founder@ecomonks.in"

#             admin_msg['To'] = "founder@ecomonks.in"

#             admin_msg['Subject'] = "New ECOMONKS Subscription"

#             admin_msg.attach(
#                 MIMEText(admin_html, 'html', 'utf-8')
#             )

#             server.sendmail(
#                 "founder@ecomonks.in",
#                 "founder@ecomonks.in",
#                 admin_msg.as_string()
#             )

#             server.quit()

#             return HttpResponse("""
#             <script>
#             alert('Subscribed Successfully');
#             window.location='/';
#             </script>
#             """)

#         except Exception as e:

#             return HttpResponse(f"ERROR: {e}")

#     return HttpResponse("Invalid Request")




import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests

# Import Supabase
from supabase import create_client

def homepage(request):
    return render(request, 'newhome.html')


def blog_page(request):
    return render(request,'blog.html')

def order_post(request):

    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    quantity = request.POST['quantity']

    

    if quantity == "50g":
        amount = 1 * 100
    elif quantity == "175g":
        amount = 1 * 100
    else:
        amount = 0

    return render(request, 'pp.html', {
        'name': name,
        'email': email,
        'phone': phone,
        'address': address,
        'quantity': quantity,
        'amount': amount,
        'razorpay_api_key': 'rzp_live_Su35EVyNYFeKCF',
        'currency': 'INR'
    })

def raz_pay(request, amount):
    import razorpay
    razorpay_api_key = "rzp_live_Su35EVyNYFeKCF"
    razorpay_secret_key = "NQE3JfS6rdlmp8YtHrxF120H"
    
    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))
    amount = float(amount)
    
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',
    }
    
    order = razorpay_client.order.create(data=order_data)
    
    return render(request, 'pp.html', {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id']
    })

# ==========================================
# SAVE ORDER TO SUPABASE - FIXED VERSION
# ==========================================
def save_order_to_supabase(name, email, phone, address, quantity, payment_id,amount):
    """Save order to Supabase database"""
    try:
        # Your Supabase credentials - DIRECT values
        supabase_url = "https://fgikrpxjaskyduewekiu.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZnaWtycHhqYXNreWR1ZXdla2l1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAzNTg3MDUsImV4cCI6MjA5NTkzNDcwNX0.kyIphJzU-gNIEvA2rXAWAKy6lC4Vur362U2lFWm6BtI"
        
        # Create client
        supabase = create_client(supabase_url, supabase_key)
        
        # Get next order number by counting existing orders
        try:
            response = supabase.table('orders').select('id', count='exact').execute()
            order_no = response.count + 1 if response.count else 1
        except Exception as e:
            print(f"Could not get count: {e}")
            order_no = 1
        
        # Insert order
        order_data = {
            "order_no": order_no,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "quantity": quantity,
            "amount": amount,
            "payment_id": payment_id
        }
        
        result = supabase.table('orders').insert(order_data).execute()
        print(f"✅ Order #{order_no} saved to Supabase")
        return True
        
    except Exception as e:
        print(f"❌ Supabase error: {str(e)}")
        return False



import requests
from datetime import datetime
import json

def send_whatsapp_message(name, phone, quantity, payment_id, amount, order_date=""):
    """
    FINAL FIXED VERSION - Testing all authentication methods
    """
    try:
        # Clean phone
        phone = str(phone).replace(" ", "").replace("+", "").strip()
        if not phone.startswith("91"):
            phone = "91" + phone

        if not order_date:
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "templateName": "karpooram_orderconfirmation",
            "senderId": phone,
            "variables": {
                "header": [],
                "body": [
                    str(name),
                    str(quantity),
                    str(amount),
                    str(payment_id),
                    str(order_date)
                ]
            }
        }

        print("📤 Sending WhatsApp Template...")
        print(f"📱 To: {phone}")
        print(f"📝 Template: karpooram_orderconfirmation")
        print(f"📦 Variables: {payload['variables']['body']}")

        # TRY MULTIPLE AUTHENTICATION METHODS
        auth_configs = [
            # Method 1: x-api-key header (as per documentation)
            {
                "name": "x-api-key header",
                "headers": {
                    "Content-Type": "application/json",
                    "x-api-key": "ded0fe99217e8a35606cb6d39e0246f1",
                    "Accept": "application/json"
                }
            },
            # Method 2: Authorization Bearer
            {
                "name": "Bearer token",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer ded0fe99217e8a35606cb6d39e0246f1",
                    "Accept": "application/json"
                }
            },
            # Method 3: API key as query parameter
            {
                "name": "Query param",
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                "params": {
                    "api_key": "ded0fe99217e8a35606cb6d39e0246f1"
                }
            },
            # Method 4: API key as query parameter with different name
            {
                "name": "Query param (apikey)",
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                "params": {
                    "apikey": "ded0fe99217e8a35606cb6d39e0246f1"
                }
            },
            # Method 5: x-api-key header with different key
            {
                "name": "x-api-key (alternative key)",
                "headers": {
                    "Content-Type": "application/json",
                    "x-api-key": "ded0fe99217e8a35606cb6d39e0246f1",
                    "Accept": "application/json"
                }
            },
        ]

        for config in auth_configs:
            print(f"\n🔑 Trying: {config['name']}")
            
            # Prepare request parameters
            kwargs = {
                "url": "https://chatbot.digitalmbg.com/v1/whatsapp/send_templet",
                "headers": config["headers"],
                "json": payload,
                "timeout": 30,
                "allow_redirects": False  # Don't follow redirects
            }
            
            # Add query parameters if present
            if "params" in config:
                kwargs["params"] = config["params"]

            response = requests.post(**kwargs)

            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")

            # Check if we got a redirect
            if response.status_code in [301, 302, 303, 307, 308]:
                location = response.headers.get('Location', '')
                print(f"   ❌ Redirected to: {location}")
                if 'login' in location:
                    print(f"   ❌ Authentication failed for this method")
                continue

            # Success!
            if response.status_code == 200:
                print(f"   ✅ SUCCESS! Message sent!")
                try:
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=2)}")
                except:
                    print(f"   Response: {response.text[:200]}")
                return True
            
            # Other status codes
            elif response.status_code == 400:
                print(f"   ❌ Bad Request: {response.text}")
                return False
            elif response.status_code == 401:
                print(f"   ❌ Unauthorized: {response.text}")
                continue
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                print(f"   Response: {response.text[:200]}")

        print("\n❌ All authentication methods failed!")
        print("\n💡 RECOMMENDED ACTIONS:")
        print("   1. Generate a NEW API key from the dashboard")
        print("   2. Make sure you're using the correct WhatsApp Business number")
        print("   3. Check if your IP needs to be whitelisted")
        print("   4. Verify the template name is exactly: karpooram_orderconfirmation")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False



# import requests

# def send_whatsapp_message(name, phone, quantity, payment_id, amount, order_date=""):
#     try:
#         print("========== MBG WHATSAPP STARTED ==========")

#         # Clean phone number
#         phone = str(phone).replace(" ", "").replace("+", "").strip()

#         if not phone.startswith("91"):
#             phone = "91" + phone

#         print("PHONE :", phone)

#         response = requests.post(
#             "https://chatbot.digitalmbg.com/v1/whatsapp/send_templet",
#             headers={
#                 "Content-Type": "application/json",
#                 "x-api-key": "e0b1a703d4d3bfc0adcdec2681a0b219"
#             },
#             json={
#                 "templateName": "karpooram_orderconfirmation",
#                 "senderId": phone,
#                 "variables": {
#                     "header": [],
#                     "body": [
#                         str(name),
#                         str(quantity),
#                         str(amount),
#                         str(payment_id),
#                         str(order_date)
#                     ]
#                 }
#             },
#             timeout=30,
#             allow_redirects=True
#         )

#         print("=" * 60)
#         print("STATUS :", response.status_code)
#         print("URL    :", response.url)
#         print("HEADERS:", response.headers)
#         print("Location :", response.headers.get("Location"))
#         print("BODY   :", response.text)
#         print("=" * 60)

#         if response.status_code == 200:
#             print("✅ WhatsApp Message Sent Successfully")
#             return True
#         else:
#             print("❌ WhatsApp Message Failed")
#             return False

#     except Exception as e:
#         print("MBG WhatsApp Error:", e)
#         return False


# def send_whatsapp_message(name, phone, quantity):
#     try:

#         print("========== WHATSAPP FUNCTION STARTED ==========")

#         # Clean phone number
#         phone = str(phone).replace(" ", "").replace("+", "").strip()

#         # Add country code if missing
#         if not phone.startswith("91"):
#             phone = f"91{phone}"

#         print("FINAL PHONE:", phone)

#         # WATI API URL
#         # url = f"https://live-mt-server.wati.io/1043453/api/v1/sendTemplateMessage?whatsappNumber={phone}"
        
#         url = f"https://live-mt-server.wati.io/1043453/api/v1/sendTemplateMessage?whatsappNumber={phone}"


#         # Payload
#         payload = {
#             "template_name": "order_confirmation",
#             "broadcast_name": "order_confirmation",
#             "parameters": [
#                 {
#                     "name": "1",
#                     "value": str(name)
#                 },
#                 {
#                     "name": "2",
#                     "value": str(quantity)
#                 }
#             ]
#         }

#         print("PAYLOAD:", payload)

#         # Headers
#         headers = {
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InByZW1zZWtoYXJAeWF0aGlzaGEuY29tIiwibmFtZWlkIjoicHJlbXNla2hhckB5YXRoaXNoYS5jb20iLCJlbWFpbCI6InByZW1zZWtoYXJAeWF0aGlzaGEuY29tIiwiYXV0aF90aW1lIjoiMDYvMDYvMjAyNiAxNzoxOToxNCIsInRlbmFudF9pZCI6IjEwNDM0NTMiLCJkYl9uYW1lIjoibXQtcHJvZC1UZW5hbnRzIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQURNSU5JU1RSQVRPUiIsImV4cCI6MjUzNDAyMzAwODAwLCJpc3MiOiJDbGFyZV9BSSIsImF1ZCI6IkNsYXJlX0FJIn0.i7aQp3cYOtk2wraWyMjHLP7L0T8znm-xf7SthfOPvZ4",
#             "Content-Type": "application/json"
#         }

#         # Send request
#         response = requests.post(
#             url,
#             json=payload,
#             headers=headers,
#             timeout=30
#         )

#         print("========== WATI RESPONSE ==========")
#         print("STATUS CODE:", response.status_code)
#         print("RESPONSE:", response.text)
#         print("===================================")

#         return response.status_code == 200

#     except Exception as e:

#         print("WhatsApp Error:", str(e))
#         return False


# ==========================================
# USER PAYMENT POST - MAIN FUNCTION
# ==========================================
def userpayment_post(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')
        payment_id = request.POST.get('payment_id')
        amount = request.POST.get('amount')


        try:
            amount = float(amount) / 100   # Paisa → Rupees
        except:
            amount = 0
        
        if not email:
            return HttpResponse("Email not found")
        
        # Success HTML template
        success_html = """
        <script>
        alert('Payment Successful!');
        window.location='/';
        </script>
        """
        
        # 1. Send emails (critical - if this fails, alert the user)
        email_sent = False
        try:
            # Customer HTML Email
            customer_html = f"""
            <html>
            <body style="font-family: Arial; background:#f4f4f4; padding:30px;">
            <div style="max-width:600px; margin:auto; background:white; border-radius:15px; padding:30px;">
            <h1 style="color:#0b7d45; text-align:center;">🌿 ECOMONKS</h1>
            <h2>Thank You For Your Order</h2>
            <p>Dear <b>{name}</b>,</p>
            <p>Your payment has been received successfully and your order is confirmed.</p>
            <div style="background:#f7fff9; border:1px solid #d4f5dd; padding:20px; border-radius:10px;">
            <h3>🧾 Order Details</h3>
            <p><b>👤 Name:</b> {name}</p>
            <p><b>📧 Email:</b> {email}</p>
            <p><b>📞 Phone:</b> {phone}</p>
            <p><b>📍 Address:</b> {address}</p>
            <p><b>💰 Amount:</b> {amount}</p>
            <p><b>📦 Quantity:</b> {quantity}</p>
            <p><b>💳 Payment ID:</b> {payment_id}</p>
            </div>
            </div>
            </body>
            </html>
            """
            
            admin_html = f"""
            <html>
            <body>
            <h2>🚨 NEW ORDER RECEIVED</h2>
            <p><b>Customer:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Phone:</b> {phone}</p>
            <p><b>Address:</b> {address}</p>
            <p><b>Quantity:</b> {quantity}</p>
            <p><b>Amount:</b> {amount}</p>
            <p><b>Payment ID:</b> {payment_id}</p>
            </body>
            </html>
            """
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("founder@ecomonks.in", "crmwddzdzoqatofz")
            
            # Customer email
            customer_msg = MIMEMultipart()
            customer_msg['From'] = "founder@ecomonks.in"
            customer_msg['To'] = email
            customer_msg['Subject'] = "ECOMONKS Order Confirmation"
            customer_msg.attach(MIMEText(customer_html, 'html', 'utf-8'))
            server.sendmail("founder@ecomonks.in", email, customer_msg.as_string())
            
            # Admin email
            admin_msg = MIMEMultipart()
            admin_msg['From'] = "founder@ecomonks.in"
            admin_msg['To'] = "founder@ecomonks.in"
            admin_msg['Subject'] = "New ECOMONKS Order Received"
            admin_msg.attach(MIMEText(admin_html, 'html', 'utf-8'))
            server.sendmail("founder@ecomonks.in", "founder@ecomonks.in", admin_msg.as_string())
            
            server.quit()
            email_sent = True
            print("✅ Emails sent successfully")
            
        except Exception as e:
            print(f"❌ Email error: {str(e)}")
            # If email fails, still continue but log it
        
        # 2. Save to Supabase (non-critical)
        try:
            save_order_to_supabase(name, email, phone, address, quantity, payment_id, amount)
        except Exception as e:
            print(f"❌ Supabase save error: {str(e)}")
        
        # 3. Send WhatsApp (non-critical)
        try:
            send_whatsapp_message(name, phone, quantity, payment_id, amount,order_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            print(f"❌ WhatsApp error: {str(e)}")
        
        # Always return success to user
        return HttpResponse(success_html)
    
    return HttpResponse("Invalid Request")

# ==========================================
# SUBSCRIPTION EMAIL FUNCTION
# ==========================================
def emailenquiry(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        try:
            subscription_html = f"""
            <html>
            <body style="font-family: Arial; background:#f4f4f4; padding:30px;">
            <div style="max-width:600px; margin:auto; background:white; border-radius:15px; padding:30px;">
            <h1 style="color:#0b7d45; text-align:center;">🌿 Welcome to ECOMONKS</h1>
            <p>Thank you for subscribing to ECOMONKS.</p>
            <p>We are excited to have you as part of our growing family ❤️</p>
            </div>
            </body>
            </html>
            """
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("founder@ecomonks.in", "crmwddzdzoqatofz")
            
            subscriber_msg = MIMEMultipart()
            subscriber_msg['From'] = "founder@ecomonks.in"
            subscriber_msg['To'] = email
            subscriber_msg['Subject'] = "ECOMONKS Subscription"
            subscriber_msg.attach(MIMEText(subscription_html, 'html', 'utf-8'))
            server.sendmail("founder@ecomonks.in", email, subscriber_msg.as_string())
            
            server.quit()
            
            return HttpResponse("""
            <script>
            alert('Subscribed Successfully');
            window.location='/';
            </script>
            """)
            
        except Exception as e:
            return HttpResponse(f"ERROR: {str(e)}")
    
    return HttpResponse("Invalid Request")




from django.http import HttpResponse

def robots_txt(request):
    return HttpResponse(
        "User-agent: *\n"
        "Allow: /\n"
        "Sitemap: https://shop.ecomonks.in/sitemap.xml",
        content_type="text/plain"
    ) 


# import random

# from django.http import JsonResponse

# def send_otp(request):

#     phone = request.POST.get("phone")

#     otp = random.randint(100000,999999)

#     request.session["otp"] = str(otp)

#     request.session["otp_phone"] = phone

#     send_whatsapp_otp(phone, otp)

#     return JsonResponse({
#         "status":"success"
#     })


# from django.http import JsonResponse

# def verify_otp(request):

#     otp = request.POST.get("otp")

#     if otp == request.session.get("otp"):

#         request.session["verified"] = True

#         return JsonResponse({
#             "verified":True
#         })

#     return JsonResponse({
#         "verified":False
#     })
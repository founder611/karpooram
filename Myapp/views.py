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
    # return render(request, 'newhome.html')
    return render(request, 'homeindex.html')



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

def send_whatsapp_message(name, phone, quantity, payment_id, amount, order_date=""):
    try:
        API_KEY = "901ff03aa80b2d5793fb6368f4e0ea22"
        
        # Clean phone number (remove spaces, + sign)
        phone = str(phone).replace(" ", "").replace("+", "").strip()
        if not phone.startswith("91"):
            phone = "91" + phone

        # Set order date if not provided
        if not order_date:
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare payload with all 5 variables
        payload = {
            "templateName": "karpooram_orderconfirmation",
            "senderId": phone,
            "variables": {
                "header": ["Thank You for Your Order"],  # No header variables in this template
                "body": [
                    str(name),        # {{1}} - Customer Name
                    str(quantity),    # {{2}} - Quantity
                    str(amount),      # {{3}} - Amount Paid
                    str(payment_id),  # {{4}} - Payment ID
                    str(order_date)   # {{5}} - Order Date
                ]
            }
        }

        print(f"📤 Sending to: {phone}")
        print(f"📝 Template: karpooram_orderconfirmation")
        print(f"📋 Variables: Name={name}, Qty={quantity}, Amount=₹{amount}, Payment={payment_id}")

        response = requests.post(
            "https://chatbot.digitalmbg.com/v1/whatsapp/send_templet",
            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY,
                "Accept": "application/json"
            },
            json=payload,
            timeout=30
        )

        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ WhatsApp message sent successfully!")
            try:
                result = response.json()
                print(f"📨 Response: {result}")
            except:
                print(f"📨 Response: {response.text}")
            return True
        elif response.status_code == 307:
            print("❌ Redirecting to login - Invalid API key")
            print("💡 Please get the correct API key from your dashboard")
            return False
        elif response.status_code == 401:
            print("❌ Unauthorized - Invalid or expired API key")
            return False
        elif response.status_code == 400:
            print("❌ Bad Request - Check template name or variables")
            print(f"Response: {response.text}")
            return False
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Request timed out - Please try again")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Check your internet")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
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



import random
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_email_otp(email, otp):
    """Send OTP via email"""
    try:
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:30px;">
            <div style="max-width:450px; margin:auto; background:white; border-radius:12px; padding:30px; text-align:center;">
                <h1 style="color:#0b7d45; margin-bottom:8px;">🌿 ECOMONKS</h1>
                <h2 style="color:#333; font-weight:300;">Your Verification Code</h2>
                <div style="background:#f7fff9; padding:20px; border-radius:10px; margin:20px 0;">
                    <div style="font-size:2.2rem; font-weight:700; letter-spacing:8px; color:#0b7d45; font-family:monospace;">
                        {otp}
                    </div>
                </div>
                <p style="color:#666; font-size:0.9rem;">
                    Enter this code to verify your email and complete your order.<br>
                    This code expires in 5 minutes.
                </p>
                <hr style="border:none; border-top:1px solid #eee; margin:20px 0;">
                <p style="color:#999; font-size:0.75rem;">
                    If you didn't request this, please ignore this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        msg = MIMEMultipart()
        msg['From'] = "founder@ecomonks.in"
        msg['To'] = email
        msg['Subject'] = "🔐 ECOMONKS - Email Verification Code"
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("founder@ecomonks.in", "crmwddzdzoqatofz")
        server.sendmail("founder@ecomonks.in", email, msg.as_string())
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email OTP error: {e}")
        return False

@csrf_exempt
def send_otp(request):
    """Send OTP to user's email"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email required'}, status=400)
        
        # Generate OTP
        otp = generate_otp()
        
        # Store in cache (expires in 5 minutes)
        cache_key = f"otp_{email}"
        cache.set(cache_key, otp, timeout=300)
        
        # Send email
        if send_email_otp(email, otp):
            return JsonResponse({'status': 'success', 'message': 'OTP sent to email'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to send email'}, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def verify_otp(request):
    """Verify the OTP submitted by user"""
    if request.method != 'POST':
        return JsonResponse({'verified': False, 'message': 'Invalid method'}, status=405)
    
    try:
        data = json.loads(request.body)
        otp_input = data.get('otp', '').strip()
        email = data.get('email', '').strip()
        
        if not email or not otp_input:
            return JsonResponse({'verified': False, 'message': 'Missing data'}, status=400)
        
        # Get stored OTP from cache
        cache_key = f"otp_{email}"
        stored_otp = cache.get(cache_key)
        
        if not stored_otp:
            return JsonResponse({'verified': False, 'message': 'OTP expired or not found'}, status=400)
        
        if str(stored_otp) == str(otp_input):
            # Mark email as verified in session
            request.session['email_verified'] = email
            request.session['verified_at'] = str(datetime.now())
            
            # Delete OTP from cache after successful verification
            cache.delete(cache_key)
            
            return JsonResponse({'verified': True, 'message': 'OTP verified successfully'})
        else:
            return JsonResponse({'verified': False, 'message': 'Invalid OTP'}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'verified': False, 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'verified': False, 'message': str(e)}, status=500)
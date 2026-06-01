import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
import smtplib
from openpyxl import Workbook, load_workbook
from datetime import datetime

import requests


def homepage(request):
    return render(request,'updatehome.html')


def order_post(request):

    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    quantity = request.POST['quantity']

    print(name,email,phone,address,quantity,"fffffffffffffffffff")

    if quantity == "50g":
        amount = 1 * 100   # Razorpay uses paise

    elif quantity == "200g":
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

    razorpay_client = razorpay.Client(
        auth=(razorpay_api_key, razorpay_secret_key)
    )

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


def userpayment_post(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')
        payment_id = request.POST.get('payment_id')

        if not email:
            return HttpResponse("Email not found")

        try:

            # ==========================================
            # CUSTOMER HTML EMAIL
            # ==========================================

            customer_html = f"""
            <html>

            <body style="font-family: Arial; background:#f4f4f4; padding:30px;">

            <div style="
            max-width:600px;
            margin:auto;
            background:white;
            border-radius:15px;
            padding:30px;
            box-shadow:0 0 10px rgba(0,0,0,0.1);
            ">

            <h1 style="color:#0b7d45; text-align:center;">
            🌿 ECOMONKS
            </h1>

            <h2 style="color:#222;">
            Thank You For Your Order
            </h2>

            <p style="font-size:16px; color:#555;">
            Dear <b>{name}</b>,
            </p>

            <p style="font-size:16px; color:#555;">
            Your payment has been received successfully and your order is confirmed.
            </p>

            <div style="
            background:#f7fff9;
            border:1px solid #d4f5dd;
            padding:20px;
            border-radius:10px;
            margin-top:20px;
            ">

            <h3 style="color:#0b7d45;">
            🧾 Order Details
            </h3>

            <p><b>👤 Name:</b> {name}</p>

            <p><b>📧 Email:</b> {email}</p>

            <p><b>📞 Phone:</b> {phone}</p>

            <p><b>📍 Address:</b> {address}</p>

            <p><b>📦 Quantity:</b> {quantity}</p>

            <p><b>💳 Payment ID:</b> {payment_id}</p>

            </div>

            <p style="
            margin-top:25px;
            font-size:16px;
            color:#444;
            ">
            We truly appreciate your support and trust in ECOMONKS.
            </p>

            <div style="
            margin-top:30px;
            background:#0b7d45;
            color:white;
            padding:15px;
            border-radius:10px;
            text-align:center;
            ">

            Thank you for shopping with us ❤️

            </div>

            </div>

            </body>

            </html>
            """

            # ==========================================
            # SMTP SERVER
            # ==========================================

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.ehlo()

            server.login(
                "founder@ecomonks.in",
                "crmwddzdzoqatofz"
            )

            # ==========================================
            # CUSTOMER EMAIL
            # ==========================================

            customer_msg = MIMEMultipart()

            customer_msg['From'] = "founder@ecomonks.in"

            customer_msg['To'] = email

            customer_msg['Subject'] = "ECOMONKS Order Confirmation"

            customer_msg.attach(
                MIMEText(customer_html, 'html', 'utf-8')
            )

            server.sendmail(
                "founder@ecomonks.in",
                email,
                customer_msg.as_string()
            )

            # ==========================================
            # ADMIN EMAIL
            # ==========================================

            admin_html = f"""
            <html>

            <body style="font-family: Arial; background:#f4f4f4; padding:30px;">

            <div style="
            max-width:600px;
            margin:auto;
            background:white;
            border-radius:15px;
            padding:30px;
            box-shadow:0 0 10px rgba(0,0,0,0.1);
            ">

            <h1 style="color:#d62828; text-align:center;">
            🚨 NEW ORDER RECEIVED
            </h1>

            <div style="
            background:#fff5f5;
            border:1px solid #ffd6d6;
            padding:20px;
            border-radius:10px;
            margin-top:20px;
            ">

            <p><b>👤 Customer Name:</b> {name}</p>

            <p><b>📧 Email:</b> {email}</p>

            <p><b>📞 Phone:</b> {phone}</p>

            <p><b>📍 Address:</b> {address}</p>

            <p><b>📦 Quantity:</b> {quantity}</p>

            <p><b>💳 Payment ID:</b> {payment_id}</p>

            </div>

            <div style="
            margin-top:30px;
            background:#0b7d45;
            color:white;
            padding:15px;
            border-radius:10px;
            text-align:center;
            ">

            ✅ PAYMENT SUCCESSFUL

            </div>

            </div>

            </body>

            </html>
            """

            admin_msg = MIMEMultipart()

            admin_msg['From'] = "founder@ecomonks.in"

            admin_msg['To'] = "founder@ecomonks.in"

            admin_msg['Subject'] = "New ECOMONKS Order Received"

            admin_msg.attach(
                MIMEText(admin_html, 'html', 'utf-8')
            )

            server.sendmail(
                "founder@ecomonks.in",
                "founder@ecomonks.in",
                admin_msg.as_string()
            )

            server.quit()


            # SAVE TO EXCEL
            save_order_to_excel(
                name,
                email,
                phone,
                address,
                quantity,
                payment_id
            )

            # SEND WHATSAPP MESSAGE
            send_whatsapp_message(
                name,
                phone,
                quantity
            )

            return HttpResponse("""
            <script>
            alert('Payment Successful & Email Sent');
            window.location='/';
            </script>
            """)

        except Exception as e:

            return HttpResponse(f"ERROR: {e}")

    return HttpResponse("Invalid Request")


# ==========================================
# SAVE ORDER TO EXCEL
# ==========================================

def save_order_to_excel(name, email, phone, address, quantity, payment_id):

    file_path = "orders.xlsx"

    # File illa engil create cheyyum
    if not os.path.exists(file_path):

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Orders"

        # Heading Row
        sheet.append([
            "Order No",
            "Date",
            "Customer Name",
            "Email",
            "Phone",
            "Address",
            "Quantity",
            "Payment ID"
        ])

        workbook.save(file_path)

    # Existing workbook open cheyyuka
    workbook = load_workbook(file_path)
    sheet = workbook.active

    # Next Order Number
    order_no = sheet.max_row

    # Current Date Time
    current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Add Row
    sheet.append([
        order_no,
        current_date,
        name,
        email,
        phone,
        address,
        quantity,
        payment_id
    ])

    workbook.save(file_path)





# ==========================================
# SEND WHATSAPP MESSAGE USING WATI
# ==========================================

def send_whatsapp_message(name, phone, quantity):

    # REMOVE SPACES / +91
    phone = phone.replace(" ", "").replace("+91", "")

    url = f"https://live-mt-server.wati.io/12345/api/v1/sendTemplateMessage?whatsappNumber=91{phone}"

    payload = {
        "template_name": "order_confirmation",
        "broadcast_name": "order_confirmation",
        "parameters": [
            {
                "name": "name",
                "value": name
            },
            {
                "name": "quantity",
                "value": quantity
            }
        ]
    }

    headers = {
        "Authorization": "wati_f8ed980e-5142-424a-9096-7cb7b2a40bd3.pUd4YizkgaTv3b1hRdnRjpIMRcObEZ9udOuJ6hN2L0_FptY3fKsysDz8Skt30_ziCCNiYbn4FsD0YbmN4OP8jpVDCwpN2scUSqq28QMUwtWjWmMjdxIJNPL8EQIRE3bt",
        "Content-Type": "application/json"
    }

    try:

        response = requests.post(
            url,
            json=payload,
            headers=headers
        )

        print("WATI RESPONSE:")
        print(response.status_code)
        print(response.text)

    except Exception as e:

        print("WhatsApp Error:", e)





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

            <div style="
            max-width:600px;
            margin:auto;
            background:white;
            border-radius:15px;
            padding:30px;
            box-shadow:0 0 10px rgba(0,0,0,0.1);
            ">

            <h1 style="color:#0b7d45; text-align:center;">
            🌿 Welcome to ECOMONKS
            </h1>

            <p style="font-size:16px; color:#555;">
            Thank you for subscribing to ECOMONKS.
            </p>

            <p style="font-size:16px; color:#555;">
            We are excited to have you as part of our growing family ❤️
            </p>

            <div style="
            background:#f7fff9;
            border:1px solid #d4f5dd;
            padding:20px;
            border-radius:10px;
            margin-top:20px;
            ">

            <h3 style="color:#0b7d45;">
            ✨ What You Will Receive
            </h3>

            <p>🛍️ Exclusive Product Updates</p>

            <p>🎉 Special Offers & Discounts</p>

            <p>📢 Latest Announcements</p>

            <p>🌱 Natural & Traditional Product Information</p>

            </div>

            <div style="
            margin-top:30px;
            background:#0b7d45;
            color:white;
            padding:15px;
            border-radius:10px;
            text-align:center;
            ">

            Thank You For Staying Connected With Us ❤️

            </div>

            </div>

            </body>

            </html>
            """

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.ehlo()

            server.login(
                "founder@ecomonks.in",
                "crmwddzdzoqatofz"
            )

            # Subscriber Email
            subscriber_msg = MIMEMultipart()

            subscriber_msg['From'] = "founder@ecomonks.in"

            subscriber_msg['To'] = email

            subscriber_msg['Subject'] = "ECOMONKS Subscription"

            subscriber_msg.attach(
                MIMEText(subscription_html, 'html', 'utf-8')
            )

            server.sendmail(
                "founder@ecomonks.in",
                email,
                subscriber_msg.as_string()
            )

            # Admin Email
            admin_html = f"""
            <html>

            <body style="font-family: Arial;">

            <h2>📩 New Subscription Received</h2>

            <p><b>Subscriber Email:</b> {email}</p>

            </body>

            </html>
            """

            admin_msg = MIMEMultipart()

            admin_msg['From'] = "founder@ecomonks.in"

            admin_msg['To'] = "founder@ecomonks.in"

            admin_msg['Subject'] = "New ECOMONKS Subscription"

            admin_msg.attach(
                MIMEText(admin_html, 'html', 'utf-8')
            )

            server.sendmail(
                "founder@ecomonks.in",
                "founder@ecomonks.in",
                admin_msg.as_string()
            )

            server.quit()

            return HttpResponse("""
            <script>
            alert('Subscribed Successfully');
            window.location='/';
            </script>
            """)

        except Exception as e:

            return HttpResponse(f"ERROR: {e}")

    return HttpResponse("Invalid Request")
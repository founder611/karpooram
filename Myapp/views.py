import smtplib
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
import smtplib


def homepage(request):
    return render(request,'updatehome.html')



# def order_post(request):

#     name = request.POST['name']
#     email = request.POST['email']
#     phone = request.POST['phone']
#     address = request.POST['address']
#     quantity = request.POST['quantity']

#     amount = 500 * 100

#     request.session.flush()

#     return redirect('/raz_pay/' + str(amount))

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



# def userpayment_post(request):

#     name = request.session.get('name')
#     email = request.session.get('email')
#     phone = request.session.get('phone')
#     address = request.session.get('address')
#     quantity = request.session.get('quantity')  

#     subject = "ECOMONKS Order Confirmation"

#     message = f"""
# Hello {name},

# Your payment was successful.

# Order Details:

# Name: {name}
# Phone: {phone}
# Address: {address}
# Quantity: {quantity}

# Thank you for ordering Edible Karpooram from ECOMONKS.
# """
    
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login("leagaladvisorteam@gmail.com", "eugnxtyylwtqwlav") 
#     to = email
#     subject = "Test Email"
#     body = message
#     msg = f"Subject: {subject}\n\n{body}"
#     server.sendmail("leagaladvisorteam@gmail.com", to, msg)  
#     server.quit()


#     return HttpResponse(
#         "<script>alert('Payment Successful & Email Sent');window.location='/'</script>"
#     )

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

        message = f"""
        Dear {name},

        🌿 Thank you for shopping with ECOMONKS.

        Your payment has been received successfully and your order is now confirmed.

        ━━━━━━━━━━━━━━━━━━
        🧾 ORDER DETAILS
        ━━━━━━━━━━━━━━━━━━

        👤 Name       : {name}
        📧 Email      : {email}
        📞 Phone      : {phone}
        📍 Address    : {address}
        📦 Quantity   : {quantity}
        💳 Payment ID : {payment_id}

        ━━━━━━━━━━━━━━━━━━

        We truly appreciate your support and trust in ECOMONKS.

        You will receive further updates regarding your order soon.

        Thank you,
        🌿 Team ECOMONKS
        """

        print("FUNCTION CALLED")
        print(name)
        print(email)
        print(phone)
        print(address)
        print(quantity)
        print(payment_id)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()

        server.login(
            # "leagaladvisorteam@gmail.com",
            "founder@ecomonks.in",
            "crmwddzdzoqatofz"
            # "eugnxtyylwtqwlav"
        )

        subject = "ECOMONKS Order Confirmation"

        msg = f"Subject: {subject}\n\n{message}"

        server.sendmail(
            "founder@ecomonks.in",
            email,
            msg
        )

        # Admin / Owner Mail
        admin_message = f"""
        🚨 NEW ORDER RECEIVED - ECOMONKS

        ━━━━━━━━━━━━━━━━━━
        🛒 CUSTOMER DETAILS
        ━━━━━━━━━━━━━━━━━━

        👤 Customer Name : {name}
        📧 Email         : {email}
        📞 Phone         : {phone}

        📍 Delivery Address:
        {address}

        📦 Ordered Quantity : {quantity}

        💳 Payment ID : {payment_id}

        ━━━━━━━━━━━━━━━━━━
        ✅ Payment Status : SUCCESSFUL
        ━━━━━━━━━━━━━━━━━━
        """

        admin_msg = f"Subject: New ECOMONKS Order Received\n\n{admin_message}"

        server.sendmail(
            "founder@ecomonks.in",
            "founder@ecomonks.in",
            admin_msg
        )

        server.quit()

        return HttpResponse("""
            <script>
                alert('Payment Successful');
                window.location='/';
            </script>
        """)

    return HttpResponse("Invalid Request")



def emailenquiry(request):

    if request.method == "POST":

        email = request.POST.get('email')

        subject = "ECOMONKS Subscription"

        message = f"""
Hello,

Thank you for subscribing to ECOMONKS.

You will now receive:
- Product updates
- Offers
- Latest notifications

Thank you for staying connected with us.
"""

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            # Gmail App Password
            server.login(
                 "founder@ecomonks.in",
                 "crmwddzdzoqatofz"
                # "leagaladvisorteam@gmail.com",
                # "eugnxtyylwtqwlav"
            )

            msg = f"Subject: {subject}\n\n{message}"

            # server.sendmail(
            #     "yourgmail@gmail.com",
            #     email,
            #     msg
            # )

            # Subscriber confirmation mail
            server.sendmail(
                "founder@ecomonks.in",
                email,
                msg
            )

            # Admin notification mail
            admin_message = f"""
            New Subscription Received

            Subscriber Email:
            {email}
            """

            admin_msg = f"Subject: New ECOMONKS Subscription\n\n{admin_message}"

            server.sendmail(
                "founder@ecomonks.in",
                "founder@ecomonks.in",
                admin_msg
            )

            server.quit()

            return HttpResponse(
                "<script>alert('Subscribed Successfully');window.location='/'</script>"
            )

        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return HttpResponse("Invalid Request")
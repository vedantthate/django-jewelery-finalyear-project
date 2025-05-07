from django.conf import settings
import pyotp
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from store.models import Address, Order
from datetime import timedelta,datetime

def send_otp(request):
    otp_secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(otp_secret_key, interval=120)
    otp = totp.now()
    
    otp_valid_date = (datetime.now() + timedelta(minutes=2)).isoformat()
    request.session['otp_secret_key'] = otp_secret_key
    request.session['otp_valid_date'] = otp_valid_date

    return otp




    
def user_full_message(email,name):
    fullmessage=f"""
                Hi {email},
                
                Welcome to the {name} family! We're thrilled to have you here. 💖

                As a valued subscriber, you'll be the first to know about:
                Exclusive New Arrivals -- Discover our latest collections 
                    before anyone else.
                Special Offers & Discounts -- Enjoy members-only savings 
                    on your favorite pieces.
                Jewelry Care Tips & Trends -- Get expert advice to keep 
                    your jewelry shining bright.

                Your journey to timeless elegance starts here. Stay tuned for our 
                next email -- something sparkly is coming your way!

                With love,
                Vedant
                
                Founder, {name}

                P.S. Follow us on [Social Media Links] for daily 
                inspiration and behind-the-scenes sneak peeks!
                ----------------------------
                This is an automated message. Please do not reply to this email..
                """
    return fullmessage
    
    
# def verification_full_messgae(user,otp):
#     otpfullmessage = f"""
#                     Hey {user},
#                     Welcome! To ensure the safety and security of your account, we need to verify
#                     your email address.
#                     Here's your One Time Password (OTP): {otp}
#                     Please enter this OTP within 5 minutes of receiving this email to complete your
#                     verification process.
#                     Do not share this code with anyone.
#                     Thank you for your cooperation,
#                     Golden Glamour
#                         """
#     return otpfullmessage



def send_order(order, razorpay_order_id):
    subject = f"Your Receipt for Order #{order.id}"
    
    order = Order.objects.filter(razorpay_order_id=razorpay_order_id).first()
    if not order:
        print("Error: Order not found for email confirmation.")
        return

    user_email = order.user.email
    order_items = order.items.all()  # Using related_name="items"
    subtotal = order.subtotal
    context = {
        "user": order.user.username,
        "order_id": order.id,
        "items": order_items,
        "total_amount": order.amount,
        "shiping_amount":order.shipping_charge,
        "shipping_details": {
            "name": order.user.username,
            "address": order.address,
            "phone": order.address.user_phone_number
        },
        "tracking_uid":order.tracking_uid,
        "subtotal":subtotal,
        "status":order.payment_status,
    }

    html_content = render_to_string("receipt_order.html", context)
    plain_message = strip_tags(html_content)

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [user_email],
        html_message=html_content,
        fail_silently=False,
    )


def send_delivery_email(user_email, product_name, order_id):
    subject = f"Your Golden Glamour Order #{order_id} has been Delivered!"
    message = f"""
        Hi there,

        Good news! Your order #{order_id} containing **{product_name}** has been successfully delivered.

        We hope you love your purchase! 😊  
        If you have any questions or need help, feel free to reach out to us anytime.

        Thank you for shopping with Golden Glamour.  
        We look forward to serving you again soon.

        Warm regards,  
        Team Golden Glamour ✨
        
        ----------------------------
        This is an automated message. Please do not reply to this email.
        """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )



#send email as html format
def verification_full_messgae(user,otp):
    # Send as HTML
    otpfullmessage = f"""
            <div style="max-width: 600px; margin: auto; font-family: Arial, sans-serif; text-align: center;">
                <div style="background: linear-gradient(to right, #0f6, #03a9f4); padding: 15px; border-radius: 10px 10px 0 0;">
                    <h2 style="color: white; margin: 0;">Golden Glamour</h2>
                </div>
                <div style="background: #fff; padding: 20px; border-radius: 0 0 10px 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <p style="color: white; margin: 5px 0;"><h2>Your OTP Code</h2></p>
                    <p style="color: #333; font-size: 16px;">Hey {user},</p>
                    <p style="color: #666; font-size: 14px;">
                        Thank you for choosing Golden Glamour. Use the following OTP to complete your registration. 
                        OTP is valid for <strong style="font-weight: bold; color: #C0392B;">2 minutes</strong>.
                        Do not share this code with anyone, including our helpdesk.
                    </p>
                    <h2 style="color: #C0392B; letter-spacing: 5px;">{otp}</h2>
                </div>
            </div>
            """
    
    return otpfullmessage
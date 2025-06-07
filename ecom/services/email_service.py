import secrets
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
 


def generate_otp(length:int = 6)->str:
    return ''.join(secrets.choice("0123456789") for _ in range(length))



def send_otp_email(to_email: str,name:str, otp: str = generate_otp()) -> None:
    subject = "🔐 Your OTP Code - Secure Login"
    from_email = settings.EMAIL_HOST_USER
    text_content = f"Hello {name}, your OTP code is: {otp}"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h2 style="color: #333;">👋 Hello, {name}</h2>
            <p style="font-size: 16px; color: #555;">
                We received a request to login or reset your password. Please use the following One-Time Password (OTP) to proceed:
            </p>
            <div style="text-align: center; margin: 20px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #1a73e8;">{otp}</span>
            </div>
            <p style="font-size: 14px; color: #888;">This code will expire in 10 minutes.</p>
            <p style="font-size: 14px; color: #888;">
                If you didn't request this, you can safely ignore this email.
            </p>
            <br/>
            <p style="font-size: 14px; color: #999;">– The E-Com Team</p>
        </div>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


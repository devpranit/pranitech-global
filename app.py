from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        service = request.form.get('service')
        message = request.form.get('message')
        
        # --- EMAIL AUTOMATION CONFIGURATION ---
        sender_email = "pranit.singh222@gmail.com"
        receiver_email = "pranit.singh222@gmail.com"
        # CRITICAL: Replace the text below with your copied 16-character App Password (no spaces)
        app_password = "ocoy telt yoyk okrp" 

        # Constructing the email structure
        subject = f"🚨 New Lead Capture: {name} - Pranitech Global"
        body = f"""
        Pranitech Global Systems,
        
        A new enterprise inquiry has been submitted through your website contact engine.
        
        [Client Metrics]
        Full Name:       {name}
        Business Email:  {email}
        Service Domain:  {service}
        
        [Project Context]
        {message}
        
        --
        Automated Dispatch System | Pranitech Cloud Engine
        """

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connect to Gmail SMTP over standard secure port 587
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Upgrade connection to secure Transport Layer Security (TLS)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print(f"✅ Lead Notification successfully routed to {receiver_email}")
        except Exception as e:
            print(f"❌ Automation Failure. Error Logs: {e}")

        return "<h1>Thank you!</h1><p>Pranitech Global Solution has received your inquiry. We will contact you shortly.</p><a href='/'>Return Home</a>"
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
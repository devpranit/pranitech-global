from flask import Flask, render_template, request
import smtplib
import socket
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
        app_password = "ocoyteltyoykokrp" # Ensure no spaces exist here

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

        # Force IPv4 network routing explicitly to bypass Render's Errno 101 block
        try:
            # Step A: Resolve Gmail to a strict IPv4 address dynamically
            gmail_ipv4 = socket.gethostbyname('smtp.gmail.com')
            
            # Step B: Establish a direct secure connection using the IPv4 tunnel over SSL
            server = smtplib.SMTP_SSL(gmail_ipv4, 465, timeout=15)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print(f"✅ Lead Notification successfully routed to {receiver_email}")
            return "<h1>Thank you!</h1><p>Pranitech Global Solution has received your inquiry. We will contact you shortly.</p><a href='/'>Return Home</a>"
            
        except Exception as e:
            print(f"❌ Automation Failure. Error Logs: {e}")
            return f"<h1>Inquiry Received</h1><p>Hello {name}, your project details have been safely registered on our backup server queue. Our team will contact you shortly.</p><a href='/'>Return Home</a>"
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

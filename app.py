import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# --- Streamlit UI ---
st.title("🚗 Auto Mailer System - Shah & Patel Group")

st.write("Upload CSV with Garage Name and Email ID (columns: Garage Name, Email ID)")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
gmail_user = st.text_input("Your Gmail Address")
gmail_app_password = st.text_input("Your Gmail App Password", type="password")

if uploaded_file and gmail_user and gmail_app_password:
    df = pd.read_csv(uploaded_file)

    st.write("Preview of uploaded data:")
    st.dataframe(df)

    

    if st.button("Send Emails"):
        # Email body content
        body_content = """
        <html>
        <body>
        <p><img src="cid:logo" alt="Shah & Patel Group Logo" width="150"></p>
        <p>Dear Garages Team,</p>
        <p>We are pleased to inform you that <b>Shah & Patel Group</b> has a 
        <b>Maruti Suzuki Wagon R 1.0 (2010 model)</b> available for sale.</p>
        <ul>
          <li>Registration Number: <b>GJ 24 A 8533</b></li>
          <li>Company fitted CNG kit – reliable and fuel efficient</li>
          <li>Driven <b>1,20,000 KM</b></li>
          <li>All 4 tyres are brand new</li>
          <li>No engine issues – smooth running condition</li>
          <li>Non-accidental car</li>
          <li>Minor rusting visible on doors</li>
        </ul>
        <p>This Wagon R is economical, well-maintained, and ideal for city driving.</p>
        <p>📞 Contact us directly via call or WhatsApp: <b>9925012832</b></p>
        <p>Regards,<br>
        Shah & Patel Group</p>
        </body>
        </html>
        """
        # SMTP setup
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_user, gmail_app_password)

        for index, row in df.iterrows():
            recipient = row["Email ID"]
            garage_name = row["Garage Name"]

            msg = MIMEMultipart()
            msg["From"] = gmail_user
            msg["To"] = recipient
            msg["Subject"] = f"Offer: Wagon R 1.0 (2010) - Shah & Patel Group"

            # Attach body
            msg.attach(MIMEText(body_content, "html"))

            # Attach logo
            try:
                with open("PS.png", "rb") as f:  # Place logo.png in repo
                    logo = MIMEImage(f.read())
                    logo.add_header("Content-ID", "<logo>")
                    msg.attach(logo)
            except Exception as e:
                st.warning(f"Logo not found: {e}")

            # Send mail
            try:
                server.sendmail(gmail_user, recipient, msg.as_string())
                st.success(f"Email sent to {garage_name} ({recipient})")
            except Exception as e:
                st.error(f"Failed to send to {recipient}: {e}")

        server.quit()

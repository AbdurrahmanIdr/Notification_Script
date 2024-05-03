import os
import configparser
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# database connection details
# for sqlite connection
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f'sqlite:///{os.path.join(basedir, "users.db")}'

# Define database models
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String(8), primary_key=True)
    staff_id = Column(Integer, nullable=False, unique=True)
    email = Column(String, nullable=False)


# Connect to the database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Create tables if they don't exist
Session = sessionmaker(bind=engine)
session = Session()


# Function to read configuration from config file
def read_config(filename='config.ini'):
    configure = configparser.ConfigParser()
    configure.read(filename)
    return configure


# Email configuration
config = read_config()

smtp_server = config['Email']['smtp_server']
smtp_port = config['Email'].getint('smtp_port')
sender_email = config['Email']['sender_email']
sender_password = config['Email']['sender_password']

# Maximum retry attempts for email sending
MAX_RETRY_ATTEMPTS = 3
RETRY_INTERVAL = 5  # Seconds between retries

print(f"SMTP Server: {smtp_server}")
print(f"SMTP Port: {smtp_port}")


def get_user_id():
    """
    Prompts the user for an ID.

    Returns:
        str: Valid user ID if entered, None otherwise
    """
    user_input = int(input("Enter a user ID: "))
    if not user_input:
        return None

    return user_input


def get_folder_path():
    """
    Prompts the user for a folder path and validates its existence.

    Returns:
        str: Valid folder path if entered, None otherwise
    """
    folder_path = input("Enter the path to the folder to process: ")
    if os.path.exists(folder_path):
        return folder_path
    else:
        print("Invalid folder path. Please enter a valid existing directory.")
        return None


def send_email_with_attachment(recipient_email, user_id, filename, matched_file_path):
    """
    Sends an email notification to the user with details about the matched file
    and optionally attaches the PDF if it exists and is accessible. Implements
    a basic retry mechanism with a configurable retry count and interval.

    Args:
        recipient_email (str): User's email address
        user_id (str): User ID
        filename (str): Matched filename containing the user ID
        matched_file_path (str): Full path to the matched file (optional)
    """
    attempts = 0
    while attempts < MAX_RETRY_ATTEMPTS:
        try:
            # Validate input for clarity and security
            if not all([recipient_email, user_id, filename]):
                print("Error: Missing information for email notification.")
                return

            # Configure email details
            subject = f"User ID: {user_id} in File: {filename}"
            body = f"Hi {recipient_email},\n\n" \
                   f"Please find the attached file for your reference.\n\n" \
                   f"Regards,\n" \
                   f"Yours Thankfully."

            # Create the message with multipart structure
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject

            # Add the plain text body
            message.attach(MIMEText(body, "plain"))

            # Attach the PDF if provided and accessible
            if matched_file_path and filename.lower().endswith(".pdf") and os.path.isfile(matched_file_path):
                with open(matched_file_path, "rb") as attachment_file:
                    pdf_part = MIMEBase("application", "octet-stream")
                    pdf_part.set_payload(attachment_file.read())
                    encoders.encode_base64(pdf_part)
                    pdf_part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                    message.attach(pdf_part)
            elif matched_file_path:
                print(f"Warning: {matched_file_path} is not a PDF file or does not exist.")

            # Create a secure connection with SMTP server
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)

                # Send the email
                server.sendmail(sender_email, recipient_email, message.as_string())
                print(f"Email notification sent to {recipient_email} for user ID {user_id}.")
                return  # Success, exit retry loop

        except (smtplib.SMTPException, FileNotFoundError) as e:
            print(f"Error sending email notification: {e}")
            attempts += 1
            if attempts < MAX_RETRY_ATTEMPTS:
                print(f"Retrying email sending in {RETRY_INTERVAL} seconds...")
                time.sleep(RETRY_INTERVAL)  # Wait before retrying
            else:
                print(f"Maximum retries ({MAX_RETRY_ATTEMPTS}) reached. Email sending failed.")

    # End of retry loop


def process_folder(folder_path):
    """
    Processes a folder, extracts IDs from filenames, retrieves user data,
    and sends email notifications with matched information (if applicable).

    Args:
        folder_path (str): Path to the folder to process
    """
    if folder_path:
        user_id = get_user_id()
        if user_id:
            user = session.query(User).filter_by(staff_id=user_id).first()
            if user:
                for filename in os.listdir(folder_path):
                    print(f"Processing file {filename}")
                    if str(user_id) in filename:
                        matched_file_path = os.path.join(folder_path, filename)  # Full path to matched file
                        send_email_with_attachment(str(user.email), user_id, filename, matched_file_path)

                        break
            else:
                print(f"ID: {user_id} - User information/file not found")
        else:
            print(f"ID: No User inputed")


folder_pathi = get_folder_path()
process_folder(folder_pathi)

# Close the session
session.close()

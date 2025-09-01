import os
import win32com.client
from datetime import datetime

# 📁 Path where attachments will be saved ("attachments" folder)
ATTACHMENTS_PATH = os.path.join(os.getcwd(), "attachments")
os.makedirs(ATTACHMENTS_PATH, exist_ok=True)

try:
    # 📨 Connect to Outlook
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")

    # Access Inbox
    inbox = namespace.GetDefaultFolder(6)  # 6 = Inbox
    if not inbox:
        raise ValueError("Could not access the Inbox")

    emails = inbox.Items
    emails.Sort("[ReceivedTime]", True)  # Sort: newest first

    # 📅 Today's date
    today = datetime.now().date()

    print(f"Found {len(emails)} emails in the inbox.")

    # 🔍 Iterate through today's emails with attachments
    for email in emails:
        if email.Class == 43:  # 43 = MailItem
            received_date = email.ReceivedTime.date()

            # Check if the email is from today and has attachments
            if received_date == today and email.Attachments.Count > 0:
                print(f"Checking email: {email.Subject}")  

                # Validate subject
                if "CONSUMPTION TRACKING" in email.Subject.upper():
                    print(f"\n📩 Subject: {email.Subject}")
                    for attachment in email.Attachments:
                        filename = attachment.FileName
                        file_path = os.path.join(ATTACHMENTS_PATH, filename)
                        attachment.SaveAsFile(file_path)
                        print(f"✅ Saved: {file_path}")
                else:
                    print(f"✋ Not a relevant email: {email.Subject}")

except Exception as e:
    print(f"Error accessing Outlook: {e}")

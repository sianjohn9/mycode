# Import necessary libraries
import imaplib
import email
from email.header import decode_header
import matplotlib.pyplot as plt
from collections import Counter

# Email account credentials
EMAIL_USER = "Gmail address"
EMAIL_PASS = "Passcode"

# Initialize the category counter
category_counts = Counter()

# Connect to the email server
def connect_to_email():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")  # Change to your email provider's IMAP server
        mail.login(EMAIL_USER, EMAIL_PASS)
        return mail
    except imaplib.IMAP4.error as e:
        print("Failed to connect to email:", e)
        return None

# Search and retrieve unread emails
def fetch_unread_emails(mail):
    mail.select("inbox")
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    return email_ids
# Function to mark an email as read
def mark_as_read(mail, email_id):
    mail.store(email_id, '+FLAGS', '\\Seen')
    print("Marked email as read with ID:", email_id)

# Process and categorize emails with additional actions
def process_email(mail, email_id):

    status, msg_data = mail.fetch(email_id, "(RFC822)")
    body = ""  # Initialize body as an empty string
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            # Check if the subject is None
            subject = msg["Subject"]
            if subject is None:
                subject = "No Subject"  # Set a default value if no subject
                encoding = None
            else:
                subject, encoding = decode_header(subject)[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

            from_ = msg.get("From")
            print(f"From: {from_}")
            print(f"Subject: {subject}")

            # Get email body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
            else:
                body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

            print(f"Body:\n{body}\n")

            # Categorize based on keywords in both subject and body
            categories = categorize_email(subject, body)
            for category in categories:
                category_counts[category] += 1  # Increment the count for each category

            save_email_summary(subject, from_, categories)

            # Perform actions based on categories
            if "general" in categories:
                mark_as_read(mail, email_id)  # Mark as read
                move_to_trash(mail, email_id)  # Move to trash (delete)
            elif "urgent" in categories:
                mark_as_unread(mail, email_id)  # Keep as unread for urgent emails


            # Categorize based on keywords in both subject and body
            categories = categorize_email(subject, body)
            for category in categories:
                category_counts[category] += 1  # Increment the count for each category

            save_email_summary(subject, from_, categories)

            # Perform actions based on categories
            if "general" in categories:
                mark_as_read(mail, email_id)  # Mark as read
                move_to_trash(mail, email_id)  # Move to trash (delete)
            elif "urgent" in categories:
                mark_as_unread(mail, email_id)  # Keep as unread for urgent emails
# Function to move an email to the Trash folder
def move_to_trash(mail, email_id):
    # 'INBOX' is selected by default, so we copy the email to Trash
    mail.copy(email_id, "[Gmail]/Trash")
    print("Moved email to Trash with ID:", email_id)

# Function to mark an email as unread
def mark_as_unread(mail, email_id):
    mail.store(email_id, '-FLAGS', '\\Seen')
    print("Marked email as unread with ID:", email_id)

# Define keyword categories
def categorize_email(subject, body):
    categories = []
    keywords = {
        "urgent": ["urgent", "asap", "important"],
        "finance": ["invoice", "payment", "bill"],
        "meeting": ["meeting", "schedule", "appointment"]
    }
    content = subject.lower() + " " + body.lower()  # Combine subject and body for keyword search
    for category, words in keywords.items():
        if any(word in content for word in words):
            categories.append(category)
    return categories or ["general"]

# Save email summaries to a file
def save_email_summary(subject, from_, categories):
    with open("email_summaries.txt", "a", encoding="utf-8") as f:
        f.write(f"From: {from_}\nSubject: {subject}\nCategories: {', '.join(categories)}\n\n")

# Plotting function for email categories
# Plotting function for email categories with color customization
def plot_category_distribution(category_counts):
    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    colors = ['red' if category == 'urgent' else 'skyblue' for category in categories]

    plt.figure(figsize=(10, 6))
    plt.bar(categories, counts, color=colors)
    plt.xlabel("Email Categories")
    plt.ylabel("Number of Emails")
    plt.title("Email Category Distribution")
    plt.show()

# Main program
def main():
    print("Connecting to email server...")
    mail = connect_to_email()
    if mail:
        print("Connected.")
        print("Fetching unread emails...")
        email_ids = fetch_unread_emails(mail)
        if email_ids:
            print(f"Found {len(email_ids)} unread emails.")
            for email_id in email_ids:
                process_email(mail, email_id)
            # Plot the distribution after processing all emails
            plot_category_distribution(category_counts)
            plt.show()  # Ensures the plot is shown before the script exits
        else:
            print("No unread emails found.")
        mail.logout()
    else:
        print("Could not connect to email server.")


if __name__ == "__main__":
    main()


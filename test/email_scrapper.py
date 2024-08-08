import requests
import re

domain = "www.bpindustrial.com.ph"
def scrape_emails(domain):
    # Send a GET request to the domain's homepage
    response = requests.get(f"http://{domain}")

    # Extract all email addresses using regular expressions
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails = re.findall(email_pattern, response.text)

    # Print the scraped email addresses
    for email in emails:
        print(email)

# Example usage
domain = "example.com"
scrape_emails(domain)
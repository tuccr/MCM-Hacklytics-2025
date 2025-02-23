import string
import openai
import os
import random
import datetime
from fpdf import FPDF
from openpyxl import Workbook
import json

# Set your OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Directory to save honeypot files
OUTPUT_DIR = "honeypot_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sample company profile
# company_profile = {
#     "name": "Acme Finance",
#     "sector": "Finance",
#     "domain": "acme-corp.com",
#     "industry_keywords": ["Financial Statements", "Accounts", "Internal Report"]
# }

openai.api_key = OPENAI_API_KEY

# Function to call OpenAI API for content generation
def generate_text(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Use the correct model name, e.g., "gpt-4" or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}]
    )
    yield response.choices[0].message.content


def get_company_profile(user_input):
    prompt = f'Parse the user input for information about their company including company "name", "sector", "domain", and all relevant "industry_keywords". If you are not able to parse out all of this information from the user input, ask the user to provide the missing information. If you have all of the information, return it as a json file and provide no other information. If you do need to ask the user to clarify something, begin your response with "I\'m Sorry" \n The user input is: "{user_input}"'
    response = "".join(generate_text(prompt))
    if response.startswith("I'm Sorry"):
        print(response)
    company_profile = {}
    try:
        company_profile = json.loads(response)
    except json.JSONDecodeError:
        print("Failed to parse company profile from response.")
    
    return company_profile

# Function to generate a honeypot PDF
def generate_pdf(company_profile, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, title, ln=True, align='C')
    pdf.ln(10)

    prompt = f"Write a fake confidential report for {company_profile['name']} named {title}."
    fake_content = "".join(generate_text(prompt))

    for _ in range(3):
        fake_content = grade_response(fake_content, prompt)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, fake_content.encode('latin-1', 'replace').decode('latin-1'))

    filename = f"{OUTPUT_DIR}/{title}_{company_profile['name']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf".strip()
    pdf.output(filename, 'F')
    print(f"Generated PDF: {filename}")

# Function to generate a honeypot Excel file
def generate_excel(company_profile, title):
    wb = Workbook()
    ws = wb.active
    ws.title = title

    headers = ["Date", "Transaction ID", "Amount", "Account", "Description"]
    ws.append(headers)

    prompt = f"Generate 10 fake financial transactions for {company_profile['name']}. Include Date, Transaction ID, Amount, Account, and Description."
    transactions = "".join(generate_text(prompt))

    for _ in range(3):
        transactions = grade_response(transactions, prompt)

    for row in transactions.split("\n"):
        ws.append(row.split(", "))

    filename = f"{OUTPUT_DIR}/{title}_{company_profile['name']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx".strip()
    wb.save(filename)
    print(f"Generated Excel: {filename}")

# Function to generate a honeypot text file
def generate_text_file(company_profile, title):
    prompt = f"Generate a fake internal memo about {random.choice(company_profile['industry_keywords'])} for {company_profile['name']} named {title}."
    fake_content = generate_text(prompt)

    for _ in range(3):
        fake_content = grade_response(fake_content, prompt)

    filename = f"{OUTPUT_DIR}/{title}_{company_profile['name']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt".strip()
    with open(filename, "w", encoding="utf-8") as file:
        file.write(fake_content)
    
    print(f"Generated Text File: {filename}")

# Function to generate titles for honeypot files
def generate_title(company_profile, num):
    prompt = f"Generate a list of {num} titles for honeypot files related to {company_profile['name']} in the {company_profile['sector']} sector. Return no other information other than the titles separated by newline characters (do not number or label outputs in any way shape or form, do not include the company name or file extensions in the returned titles). Maximum length of a title is 25 characters. Ensure titles contain no characters which cannot be included in file names such as quotation marks, slashes, spaces, etc."
    return "".join(generate_text(prompt)).strip().split('\n')

# Function to grade and revise the response
def grade_response(response, original_prompt):
    prompt = f'Analyze the following response which was generated using the prompt "{original_prompt}" and revise it for any errors or "strange" syntax: \n {response}. Make sure there are no illegal or otherwise "program breaking" characters in the response text and only return a revised version of the original text. Do not respond with any commentary or notes, simply respond with the revised text in a similar fashion to the original I\'ve given you.'
    return "".join(generate_text(prompt))

# titles = generate_title(company_profile, 5)

# # Generate multiple honeypot files
# for title in titles:
#     generate_pdf(company_profile, title)
#     generate_excel(company_profile, title)
#     generate_text_file(company_profile, title)

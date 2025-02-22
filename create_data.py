import openai
import os
import random
import datetime
import csv
from fpdf import FPDF
from openpyxl import Workbook

# Set your OpenAI API key
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Directory to save honeypot files
OUTPUT_DIR = "honeypot_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sample company profile
company_profile = {
    "name": "Acme Finance",
    "sector": "Finance",
    "domain": "acme-corp.com",
    "industry_keywords": ["Financial Statements", "Accounts", "Internal Report"]
}

# Function to call OpenAI API for content generation
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )
    return response["choices"][0]["message"]["content"]

# Function to generate a honeypot PDF
def generate_pdf(company_profile, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    pdf.cell(200, 10, title, ln=True, align='C')
    pdf.ln(10)

    # Generate fake content using ChatGPT
    prompt = f"Write a fake confidential report for {company_profile['name']} named {title}."
    fake_content = generate_text(prompt)

    revisions = 3
    for _ in range(revisions):
        fake_content = grade_response(fake_content, prompt)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, fake_content)

    # Save the PDF
    filename = f"{OUTPUT_DIR}/{title}_{company_profile['name']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    print(f"Generated PDF: {filename}")


# Function to generate a honeypot Excel file
def generate_excel(company_profile, title):
    wb = Workbook()
    ws = wb.active
    ws.title = title

    # Header row
    headers = ["Date", "Transaction ID", "Amount", "Account", "Description"]
    ws.append(headers)

    # Generate fake transactions using ChatGPT
    prompt = f"Generate 10 fake financial transactions for {company_profile['name']}. Include Date, Transaction ID, Amount, Account, and Description."
    transactions = generate_text(prompt)

    revisions = 3
    for _ in range(revisions):
        transactions = grade_response(transactions, prompt)
    
    transactions = transactions.split("\n")

    # Fill the Excel sheet
    for row in transactions:
        ws.append(row.split(", "))

    # Save the Excel file
    filename = f"{OUTPUT_DIR}/{company_profile['name']}_Financial_Records_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    wb.save(filename)
    print(f"Generated Excel: {filename}")

# Function to generate a honeypot text file
def generate_text_file(company_profile, title):
    # Generate fake content using ChatGPT
    prompt = f"Generate a fake internal memo about {random.choice(company_profile['industry_keywords'])} for {company_profile['name']} named {title}."
    fake_content = generate_text(prompt)

    revisions = 3
    for _ in range(revisions):
        fake_content = grade_response(fake_content, prompt)

    # Save the text file
    filename = f"{OUTPUT_DIR}/{company_profile['name']}_{title}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(fake_content)
    
    print(f"Generated Text File: {filename}")
    
# Generate good titles for company profile honeypot files with chatgpt
def generate_title(company_profile, num):
    prompt = f"Generate a list of {num} titles for honeypot files related to {company_profile['name']} in the {company_profile['sector']} sector. Return no other information other than the titles separated by newline characters (do not number or label outputs in any way shape or form, do not include the company name or file extensions in the returned titles)"
    return generate_text(prompt).split('\n')

# have chatgpt grade the reeponse to a prompt and revise the output
def grade_response(response, original_prompt):
    prompt = f'Analyze the following response which was generated using the prompt "{original_prompt}" and revise it for any errors or "strange" syntax: \n {response}'
    return generate_text(prompt)

titles = generate_title(company_profile, 5)

# Generate multiple honeypot files
for title in titles:  # Generates 5 of each type
    generate_pdf(company_profile, title)
    generate_excel(company_profile, title)
    generate_text_file(company_profile, title)

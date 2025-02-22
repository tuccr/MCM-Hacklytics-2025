import openai

# Enter your OpenAI API key here
# openai.api_key = None

def ask_openai(messages):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages = messages,
    )
    yield response.choices[0].message.content
# messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt},
#         ]

# print(ask_openai("What is the capital of Monaco?"))
import openai

def chat_with_openai(api_key, messages):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # oder "gpt-4" falls du Zugriff auf GPT-4 hast
        messages=messages
    )
    return response.choices[0].message['content']

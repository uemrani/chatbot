import openai

def chat_with_openai(api_key, messages):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

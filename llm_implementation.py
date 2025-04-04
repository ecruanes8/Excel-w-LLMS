import openai

openai.api_key = 'open_ai_key_goes_here'

def build_llm_prompt(user_request, schema): 
    return f"""You are an AI assistant that writes SQLite queries.
    Database schema:
    {schema}

    User question:
    {user_request}

    Write a valid SQL query for SQLite:
    """

def ask_llm(prompt):
   response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ])
   return response.choices[0].message['content']

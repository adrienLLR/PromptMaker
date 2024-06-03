from openai import OpenAI
import time

def embedding(api_key: str, input: str) -> list:
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=input)
    return response.data[0].embedding

def completion(input: str, 
                api_key: str, 
                model = "gpt-3.5-turbo", 
                temperature: float = 0.0, 
                top_p: float = 1.0, 
                frequency_penalty: float = 0.0, 
                presence_penalty: float = 0.0) -> str:
    # client = OpenAI(api_key=api_key)
    # response = client.chat.completions.create(
    # model=model,
    # messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": input}
    # ],
    # temperature=temperature,
    # top_p=top_p,
    # frequency_penalty=frequency_penalty,
    # presence_penalty=presence_penalty
    # )
    # return response.choices[0].message.content
    return input + str(time.time())

def include_context_in_prompt(past_messages: list, prompt: str, model: str):
    """
    Assume that the prompt in itself is below the token limit
    """
    if len(past_messages) == 0:
        return prompt
    character_limit = 8000 * 6 # Need to change that to use the model selected
    header = "Past conversation:"
    current_prompt = f"\nCurrent prompt:\n user: {prompt}"
    for message in reversed(past_messages):
        new_prompt = f"{message['role']}: {message['content']}\n" + current_prompt 
        if len(new_prompt) + len(header) < character_limit:
            current_prompt = new_prompt
        else:
            break
    # Only add the header if at least one past message was concatenated   
    if len(current_prompt) == len(prompt):
        return prompt
    current_prompt = f"{header}\n {current_prompt}"
    return current_prompt
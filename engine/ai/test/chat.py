import os
from llama_index.llms import Gemini

GOOGLE_API_KEY = "AIzaSyAZzGyJ9DlHZYjmTJHR33FkmN09LU0W8-Q"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

resp = Gemini().complete("Write a poem about a magic backpack")
print(resp)

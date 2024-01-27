import time
from selenium import webdriver
import pytesseract
from PIL import Image
import textwrap
import google.generativeai as genai
#from IPython.display import Markdown

def phish_check(link):
    driver = webdriver.Chrome()
    driver.set_window_size(1500, 2000)
    driver.get(link)
    time.sleep(3)
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()
    image = Image.open('screenshot.png')
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd
    text = pytesseract.image_to_string(image)
    print(text)
    return(text)

l="http://telstra-101474.weeblysite.com/"

tt=phish_check(l)

def to_markdown(text):
    text = text.replace('•', '  *')
    return(textwrap.indent(text, '> ', predicate=lambda _: True))
    #return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key="AIzaSyAZzGyJ9DlHZYjmTJHR33FkmN09LU0W8-Q")

# List Models
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

# Generate text from text inputs
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Please say if the following site is phishing: "+tt+" and the website is "+l)

print(to_markdown(response.text))

print(response.candidates)

response = model.generate_content("Please say if the following site is phishing: "+tt+" and the website is "+l, stream=True)
for chunk in response:
    print(chunk.text)
    print("_"*80)

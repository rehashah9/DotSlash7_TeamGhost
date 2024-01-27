import time
import streamlit as sl
from selenium import webdriver
import pytesseract
from PIL import Image
import textwrap
import google.generativeai as genai
#from IPython.display import Markdown

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

def phish_check(link):
    driver = webdriver.Chrome()
    driver.set_window_size(1500, 2000)
    driver.get(link)
    time.sleep(1)
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()
    image = Image.open('screenshot.png')
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd
    tt = pytesseract.image_to_string(image)
    print(tt)
    global model
    response = model.generate_content("Please say if the following site is phishing: "+tt+" and the website is "+link)
    output=to_markdown(response.text)
    print(output)
    print(response.candidates)
    output+="\n"+str(response.candidates)+"\n"
    response = model.generate_content("Please say if the following site is phishing: "+tt+" and the website is "+link, stream=True)
    for chunk in response:
        print(chunk.text)
        output+=chunk.text+"\n"
        print("_"*80)
        output+="_"*80
    sl.session_state["out"]=output    

sl.set_page_config(page_title="PhishingCheck", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

if sl.session_state.get("check"):
    phish_check(sl.session_state["link"])

sl.title("Detecting Phishing Links")
sl.text_input("Link to check: ",key="link")
sl.button("Check",key="check")
sl.text_area(label="Results: ",value="",height=350,key="out")

import time
from selenium import webdriver
import pytesseract
from PIL import Image

def phish_check(link):
    driver=webdriver.Chrome()
    driver.set_window_size(1500,2000)
    driver.get(link)
    time.sleep(3)
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()
    image = Image.open('screenshot.png')
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd
    text = pytesseract.image_to_string(image)
    print(text)

phish_check("https://goodreads.com/")

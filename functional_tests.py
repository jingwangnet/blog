from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://127.0.0.1:8000')

assert 'successful' in browser.title

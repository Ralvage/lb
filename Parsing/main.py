import time
from selenium import webdriver
from openpyxl import Workbook
from selenium.webdriver.common.by import By

driver = webdriver.Edge()
driver.get('https://iotvega.com/product')
time.sleep(2)
wb = Workbook()
ws = wb.active
ws.title = 'Products'

driver.find_element(By.CLASS_NAME, 'spoiler-button').click()
time.sleep(2)
driver.find_element(By.XPATH, '//div[@data-filter=".tag-terminal-device"]').click()

time.sleep(2)
product_elements = driver.find_elements(By.CLASS_NAME, 'product-name')
price_elements = driver.find_elements(By.CLASS_NAME, 'price_item')

for product, price in zip(product_elements, price_elements):
    product_name = product.text
    product_price = price.text
    if product_name and product_price != '':
        ws.append([product_name, product_price])

wb.save('products.xlsx')
driver.quit()

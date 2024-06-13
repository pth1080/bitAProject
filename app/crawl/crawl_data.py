import asyncio
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from sqlmodel.ext.asyncio.session import AsyncSession

from app import Product, ProductImage
from app.models.base_class import engine

driver = webdriver.Chrome()
products = []


async def create_product(product_name, current_price, original_price, location='', sold=0, rate=0, rate_counts=0,
                         discount_percent=0):
    async with AsyncSession(engine) as async_session:
        product = Product(
            name=product_name,
            location=location,
            sold=sold,
            rate=rate,
            rate_counts=rate_counts,
            current_price=current_price,
            original_price=original_price,
            discount_percent=discount_percent,
        )
        async_session.add(product)
        await async_session.commit()
        await async_session.refresh(product)
    print('created product', dict(name=product_name,
                                  location=location,
                                  sold=sold,
                                  rate=rate,
                                  rate_counts=rate_counts,
                                  current_price=current_price,
                                  original_price=original_price,
                                  discount_percent=discount_percent, ))
    return product


async def create_product_image(list_product_images):
    async with AsyncSession(engine) as async_session:
        async_session.add_all(list_product_images)
        await async_session.commit()
        return


def convert_to_int(s):
    return int(re.sub(r'\D', '', s))


async def scrape_page():
    # Find all product items on the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Iterate through each product item and extract data
    for item in soup.findAll('div', class_='Bm3ON'):
        # Extract product name
        product_name = item.find('div', class_='RfADt').text
        location = item.find('span', class_='oa6ri')
        if location:
            location = location.text
        sold = item.find('span', class_='_1cEkb')
        if sold:
            sold = convert_to_int(sold.text)
        rate = item.find('div', class_='mdmmT _32vUv')
        if rate:
            rate = len(rate.findAll('i', class_='_9-ogB Dy1nx'))
        rate_counts = item.find('span', class_='qzqFw')
        if rate_counts:
            rate_counts = convert_to_int(rate_counts.text)
        # Extract new price
        current_price, original_price, discount_percent = 0, 0, 0
        current_price_element = item.find('div', class_='aBrP0').find('span', class_='ooOxS')
        if current_price_element:
            current_price = convert_to_int(current_price_element.text)

        # Extract old price and discount percentage
        discount_element = item.find('div', class_='WNoq3')
        if discount_element:
            original_price_element = discount_element.find('del', class_='ooOxS')
            if original_price_element:
                original_price = convert_to_int(original_price_element.text)
            discount_percent_element = discount_element.find('span', class_='IcOsH')
            if discount_percent_element:
                discount_percent = convert_to_int(discount_percent_element.text)
        # create product
        product = await create_product(product_name, current_price, original_price, location, sold, rate, rate_counts,
                                       discount_percent)
        # Extract product image
        list_product_images = []
        main_image_div = item.find('div', class_='_95X4G')
        main_image_tag = main_image_div.find('img')
        if main_image_tag and 'src' in main_image_tag.attrs:
            main_image_url = main_image_tag['src']
            list_product_images.append(ProductImage(
                url=main_image_url,
                is_main=True,
                product_id=product.id,
            ))
        list_images_div = item.find('div', class_='eZKPe')
        if list_images_div:
            list_image_tags = list_images_div.find_all('img')
            for img in list_image_tags:
                if img and 'src' in img.attrs:
                    list_product_images.append(ProductImage(
                        url=img['src'],
                        is_main=False,
                        product_id=product.id,
                    ))
        if list_product_images:
            await create_product_image(list_product_images)


async def main():
    driver.get(f"https://www.lazada.vn/locklock-flagship-store/?q=All-Products&from=wangpu&langFlag=vi&pageTypeId=2")
    # Wait for the product items to load
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root")))

    current_page = 1

    # Variable to indicate whether there are more pages to crawl
    has_next_page = True

    # Loop until there are no more pages to crawl
    while has_next_page:
        print("Scraping page", current_page)

        # Scrape product information from the current page
        await scrape_page()
        print("Scraping done - page", current_page)
        # Increment the current page number
        current_page += 1

        # Find the "Next Page" button and click it
        try:
            next_page_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@title='Next Page']")))
            driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
            next_page_button.click()

            # Wait for the new content to load
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root")))            # Wait for the page to load
            time.sleep(1)  # Adjust the wait time as needed

        except Exception as e:
            # If the "Next Page" button is not found, exit the loop
            print("No more pages to scrape.", e.__str__())
            has_next_page = False


if __name__ == "__main__":
    asyncio.run(main())
    driver.quit()

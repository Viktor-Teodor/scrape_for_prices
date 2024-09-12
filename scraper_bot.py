from time import sleep
import requests
import config
import google.generativeai as genai
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper():

    def __init__(self, model_type):
        genai.configure(api_key = config.api_key)
        self.model = genai.GenerativeModel(model_type)


    def extract_property_data(html_content):
        """Extracts property data from the given HTML content.

        Args:
            html_content (str): The HTML content of the webpage.

        Returns:
            list: A list of dictionaries, each representing a property.
        """

        soup = BeautifulSoup(html_content, 'html.parser')
        properties = []

        # Assuming a specific structure for the property listings, adjust selectors as needed
        for property in soup.find_all('div', class_='offer'):
            title = property.find('h2').text.strip()
            price_element = property.find('span', class_='price no-mobile')
            price, currency = price_element.text.strip().split()
            address_elements = property.find_all('li', class_='pinZona')[0].text.strip().split(',')
            address = ', '.join(address_elements)
            rooms, surface = [item.text.strip() for item in property.find_all('li', class_='labelTags')]
            # Extract offer code, assuming it's within the 'sku' span
            offer_code = property.find('span', class_='sku').text.strip().split(': ')[1]

            properties.append({
                'name': title,
                'price': price,
                'currency': currency,
                'address': address,
                'surface': surface,
                'rooms': rooms,
                'offer_code': offer_code
            })

        return json.dumps(properties, indent=4)

    def get_information(self, url : str):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx and 5xx)

            # Access the content of the webpage
            webpage_content = response.text

            response = self.model.generate_content("Write a story about a magic backpack.")
            return webpage_content

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def scrape_website(url):
        driver = webdriver.Safari()  # Or webdriver.Firefox(), etc.

        try:
            # Load the website
            driver.get(url)

            sleep(5)
            
            # Find all elements with the "post-card" prefix in their ID
            elements = driver.find_elements(By.CSS_SELECTOR, '[id^="post-card"]')
            print(title for title in elements.)

        finally:
            # Close the browser
            driver.quit()

if __name__ == "__main__":
    scraper = Scraper("gemini-1.5-flash")
    url = "https://interimobiliare.ro/apartamente-de-inchiriat-iasi?gad_source=1&gclid=CjwKCAjwufq2BhAmEiwAnZqw8jIu4PceEkfe2pM-1yMy9d1hHDS6KO54YECjaYX79grQ-myQPjr2ARoC3qUQAvD_BwE"

    info = scraper.get_information(url)
    print(info)

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

header = {
    "User-Agent": "https://myhttpheader.com/ = {User-Agent:'Mozilla420'}}",
    "Accept-Language": "da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(
    "https://www.zillow.com/manhattan-new-york-ny/rentals/?searchQueryState=%7B%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22north%22%3A40.96198983009294%2C%22east%22%3A-73.71721056152342%2C%22south%22%3A40.59907344570779%2C%22west%22%3A-74.24043443847654%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A387908%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A2000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12530%2C%22regionType%22%3A17%7D%5D%2C%22pagination%22%3A%7B%7D%7D",
    headers=header)

data = response.text
soup = BeautifulSoup(data, "html.parser")
all_link_elements = soup.select(".result-list-container ul li a")
all_link_elements = all_link_elements[1::2]
all_links = []
for link in all_link_elements:
    href = link["href"]
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

all_address_elements = soup.select(".result-list-container ul li a address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]

all_price_elements = soup.select(".property-card-data span")
all_prices = []
for element in all_price_elements:
    try:
        price = element.contents[0]
    except IndexError:
        raise Exception("TODO:")
    finally:
        all_prices.append(price)

chrome_driver_path = r'/Users/frodoswaggins/chromedriver_mac_arm64'
ser = Service(chrome_driver_path)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)
for n in range(len(all_addresses)):
    driver.get('https://forms.gle/5Mwpik9s7dSgzgND8')

    time.sleep(3)
    # driver.implicitly_wait(10)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()

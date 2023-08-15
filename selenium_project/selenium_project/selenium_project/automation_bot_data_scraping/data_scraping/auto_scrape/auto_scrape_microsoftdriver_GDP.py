import time
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
import pandas as pd
import os
import random
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import csv


world_gdp = 'https://tradingeconomics.com/matrix'
eu_gdp = 'https://tradingeconomics.com/matrix?g=europe'
asia_gdp = 'https://tradingeconomics.com/matrix?g=asia'
america_gdp = 'https://tradingeconomics.com/matrix?g=america'

list_gdp_contries = [
    world_gdp, america_gdp, eu_gdp, asia_gdp
]
app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")
path = "D:\microsoftdriver_autotest_114\msedgedriver.exe"
service = Service(executable_path=path)
options = webdriver.EdgeOptions()


def get_proxy_ip_and_port():
    url = "https://free-proxy-list.net/#list"
    response = requests.get(url)
    html = response.text
    proxy_table = html.split("<tbody>")[1].split("</tbody>")[0]
    proxies = proxy_table.split("<tr><td>")[1:]
    proxy_list = []
    for proxy in proxies:
        ip = proxy.split("</td><td>")[0]
        port = proxy.split("</td><td>")[1].split("</td><td>")[0]
        proxy_list.append({"http": f"http://{ip}:{port}"})
    return proxy_list


def is_proxy_alive(proxy):
    try:
        response = requests.get("https://free-proxy-list.net/#list", proxies={"http": proxy, "https": proxy})
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        return False


def get_proxy_list():
    url = "https://free-proxy-list.net/#list"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.104 Safari/537.3'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    proxy_list = []
    for row in soup.find_all("table")[0].tbody.find_all("tr"):
        https_value = row.find_all("td")[6].text
        if https_value == "yes":
            proxy = row.find_all("td")[0].text + ":" + row.find_all("td")[1].text
            proxy_list.append(proxy)
    return proxy_list


def extract_proxy(proxy_string):
    proxy = proxy_string.split(":")
    ip = proxy[0]
    port = proxy[1]
    return ip, port


proxy_list = get_proxy_list()
print(proxy_list)
proxy_sever = random.choice(proxy_list)
print(proxy_sever)
proxy_ip = extract_proxy(proxy_sever)[0]
print(proxy_ip)
proxy_port = extract_proxy(proxy_sever)[1]
print(proxy_port)
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': f"{proxy_ip}:{proxy_port}",
    'ftpProxy': f"{proxy_ip}:{proxy_port}",
    'sslProxy': f"{proxy_ip}:{proxy_port}"
})
options.add_argument("--headless")
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu-sandbox')
options.add_argument('--disable-accelerated-2d-canvas')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-notifications')
# options.add_argument(f'--proxy-server={proxy_sever}:{proxy_port}')
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.864.75")
options.proxy = proxy
driver = webdriver.Edge(service=service, options=options)


def scrape_gdp(website):
    driver.get(website)
    driver.fullscreen_window()
    time.sleep(3.0)
    driver.set_page_load_timeout(20.0)
    driver.set_script_timeout(20.0)
    ######################################################################################################################################

    containers_contries= driver.find_elements(By.XPATH, '//table/tbody/tr/td[1]/a')
    print(len(containers_contries))
    contries = [containers_contry.text for containers_contry in containers_contries]
    contries_links = [containers_contry_link.get_attribute("href") for containers_contry_link in containers_contries]

    ########################################################################################################################################

    containers_GDP_s= driver.find_elements(By.XPATH, '//table/tbody/tr/td[2]/a')
    print(len(containers_GDP_s))
    GDP = [containers_GDP.text for containers_GDP in containers_GDP_s]
    GDP_links = [containers_GDP_link.get_attribute("href") for containers_GDP_link in containers_GDP_s]

    ########################################################################################################################################

    containers_GDP_YoY_s = driver.find_elements(By.XPATH, '//table/tbody/tr/td[3]/a')
    print(len(containers_GDP_YoY_s))
    GDP_YoY = [containers_GDP_YoY.text for containers_GDP_YoY in containers_GDP_YoY_s]
    GDP_YoY_links = [containers_GDP_YoY_link.get_attribute("href") for containers_GDP_YoY_link in containers_GDP_YoY_s]

    ########################################################################################################################################

    containers_GDP_QoQ_s = driver.find_elements(By.XPATH, '//table/tbody/tr/td[4]/a')
    print(len(containers_GDP_QoQ_s))
    GDP_QoQ = [containers_GDP_QoQ.text for containers_GDP_QoQ in containers_GDP_QoQ_s]
    GDP_QoQ_links = [containers_GDP_QoQ_link.get_attribute("href") for containers_GDP_QoQ_link in containers_GDP_QoQ_s]

    ########################################################################################################################################

    containers_Interest_Rate_s = driver.find_elements(By.XPATH, '//table/tbody/tr/td[5]/a')
    print(len(containers_Interest_Rate_s))
    Interest_Rate = [containers_Interest_Rate.text for containers_Interest_Rate in containers_Interest_Rate_s]
    Interest_Rate_links = [containers_Interest_Rate_link.get_attribute("href") for containers_Interest_Rate_link in containers_Interest_Rate_s]

    ########################################################################################################################################

    containers_Inflation_Rate_s = driver.find_elements(By.XPATH, '//table/tbody/tr/td[6]/a')
    print(len(containers_Inflation_Rate_s))
    Inflation_Rate = [containers_Inflation_Rate.text for containers_Inflation_Rate in containers_Inflation_Rate_s]
    Inflation_Rate_links = [containers_Inflation_Rate_link.get_attribute("href") for containers_Inflation_Rate_link in containers_Inflation_Rate_s]

    ########################################################################################################################################

    containers_Jobless_Rate_s = driver.find_elements(By.XPATH, '//table/tbody/tr/td[7]/a')
    print(len(containers_Jobless_Rate_s))
    Jobless_Rate = [containers_Jobless_Rate.text for containers_Jobless_Rate in containers_Jobless_Rate_s]
    Jobless_Rate_links = [containers_Jobless_Rate_link.get_attribute("href")for containers_Jobless_Rate_link in containers_Jobless_Rate_s]

    ########################################################################################################################################

    containers_Gov_Budget_s = driver.find_elements(By.XPATH, '//table/tbody/tr/td[8]/a')
    print(len(containers_Gov_Budget_s))
    Gov_Budget = [containers_Gov_Budget.text for containers_Gov_Budget in containers_Gov_Budget_s]
    Gov_Budget_links = [containers_Gov_Budget_link.get_attribute("href")for containers_Gov_Budget_link in containers_Gov_Budget_s]

    ########################################################################################################################################

    containers_Debt_GDP_s = driver.find_elements(By.XPATH, '//table/tbody/tr/td[9]/a')
    print(len(containers_Debt_GDP_s))
    Debt_GDP = [containers_Debt_GDP.text for containers_Debt_GDP in containers_Debt_GDP_s]
    Debt_GDP_links = [containers_Debt_GDP_link.get_attribute("href")for containers_Debt_GDP_link in containers_Debt_GDP_s]

    ########################################################################################################################################

    containers_Current_Account_s = driver.find_elements(By.XPATH, '//table/tbody/tr/td[10]/a')
    print(len(containers_Current_Account_s))
    Current_Account = [containers_Current_Account.text for containers_Current_Account in containers_Current_Account_s]
    Current_Account_links = [containers_Current_Account_link.get_attribute("href") for containers_Current_Account_link in containers_Current_Account_s]

    ########################################################################################################################################

    containers_Population_s= driver.find_elements(By.XPATH, '//table/tbody/tr/td[11]/a')
    print(len(containers_Population_s))
    Population = [containers_Population.text for containers_Population in containers_Population_s]
    Population_links = [containers_Population.get_attribute("href")for containers_Population in containers_Population_s]

    ########################################################################################################################################

    gdp_dict = {"Contries": contries,"contries_details": contries_links,
                "GDP": GDP, "GDP_details": GDP_links,
                "GDP YoY": GDP_YoY, "GDP YoY_details": GDP_YoY_links,
                "GDP QoQ": GDP_QoQ, "GDP QoQ_details": GDP_QoQ_links,
                "Interest Rate": Interest_Rate, "Interest Rate_details": Interest_Rate_links,
                "Inflation Rate": Inflation_Rate, "Inflation_details": Inflation_Rate_links,
                "Jobless Rate": Jobless_Rate, "Jobless_details": Jobless_Rate_links,
                "Gov. Budget": Gov_Budget, "Gov. Budget_details": Gov_Budget_links,
                "Debt/GDP": Debt_GDP, "Debt/GDP_details": Debt_GDP_links,
                "Current Account ": Current_Account, "Current Account_details": Current_Account_links,
                "Population": Population, "Population_details": Population_links
                }
    gdp_df = pd.DataFrame(gdp_dict)
    gdp_df.fillna("NaN", inplace=True)
    return gdp_df


def cleaning(df):
    if type(df) == list:
        return df.drop_duplicates()
    return df
    pass


def create_csv_file(df,file_name):
    file = f'{file_name}_indicate_{day_month_year}.csv'
    file_export = os.path.join(app_path, file)
    note_paragraph = driver.find_element(By.XPATH, value='//div[@class="col-lg-12"]/h2').text
    final_df = cleaning(df)
    final_df.to_csv(file_export, header=True, encoding="utf-8-sig", index=False)
    with open(file_export, "a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(note_paragraph)
    pass


def merge_df(dataframes):
    return pd.concat(dataframes, axis=0)
    pass
    

if __name__ == '__main__':
    df_world_gdp = scrape_gdp(website=world_gdp)
    df_america_gdp = scrape_gdp(website=america_gdp)
    df_eu_gdp = scrape_gdp(website=eu_gdp)
    df_asia_gdp = scrape_gdp(website=asia_gdp)
    create_csv_file(df_world_gdp, file_name="World_gdp")
    create_csv_file(df_america_gdp, file_name="America_gdp")
    create_csv_file(df_eu_gdp, file_name="EU_gdp")
    create_csv_file(df_asia_gdp, file_name="ASIA_gdp")
    driver.quit()
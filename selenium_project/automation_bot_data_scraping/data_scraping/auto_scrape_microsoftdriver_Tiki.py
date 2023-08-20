from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import os
from datetime import datetime
import sys, time


path = "D:\microsoftdriver_autotest_114\msedgedriver.exe"
service = Service(executable_path=path)
options = webdriver.EdgeOptions()
# options.add_argument("--headless")
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
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.864.75')

driver = webdriver.Edge(service=service, options=options)
app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")


def scrape_Tiki(website):
    driver.get(website)
    driver.fullscreen_window()
    time.sleep(5)
    driver.set_page_load_timeout(10.0)
    driver.set_script_timeout(10.0)
    for i in range(190):
        driver.execute_script(f"window.scrollTo(0, {str(i)}00);")

    ########################################################################################################################################

    containers_links = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/main/div[@class="Container-sc-itwfbd-0 hfMLFx"]/'
                                                      'div[@class="CategoryViewstyle__ContentWrap-sc-bhstkd-0 goUqEt"]/'
                                                      'div[@class="CategoryViewstyle__Right-sc-bhstkd-1 jxmsjJ"]/div/'
                                                      'div[@data-view-id="product_list_container"]/div/div/a')
    print(len(containers_links))
    links = [container_link.get_attribute("href") for container_link in containers_links]

    ########################################################################################################################################

    containers_name_products = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/main/div[@class="Container-sc-itwfbd-0 hfMLFx"]/'
                                                              'div[@class="CategoryViewstyle__ContentWrap-sc-bhstkd-0 goUqEt"]/'
                                                              'div[@class="CategoryViewstyle__Right-sc-bhstkd-1 jxmsjJ"]/div/'
                                                              'div[@data-view-id="product_list_container"]/div/div/a/span/div[2]'
                                                              '/div[@class="info"]/div[@class="style__StyledNameProduction-sc-7xd6qw-4 dDfbLj"]'
                                                              '/div[@class="name"]/h3')
    print(len(containers_name_products))
    name_products = [container_name_product.text for container_name_product in containers_name_products]

    ########################################################################################################################################

    containers_org_prices = driver.find_elements(By.CSS_SELECTOR, '.price-discount__price')
    print(len(containers_org_prices))
    org_prices = [container_org_price.text for container_org_price in containers_org_prices]

    ########################################################################################################################################

    containers_discounts = driver.find_elements(By.CSS_SELECTOR, ".price-discount__discount")
    print(len(containers_discounts))
    discounts = [containers_discount.text for containers_discount in containers_discounts]

    ########################################################################################################################################

    containers_saled_products = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/main/div[@class="Container-sc-itwfbd-0 hfMLFx"]'
                                                               '/div[@class="CategoryViewstyle__ContentWrap-sc-bhstkd-0 goUqEt"]'
                                                               '/div[@class="CategoryViewstyle__Right-sc-bhstkd-1 jxmsjJ"]/div/'
                                                               'div[@data-view-id="product_list_container"]/div/div/a/span/div[2]/'
                                                               'div[@class="info"]/div[@class="style__StyledNameProduction-sc-7xd6qw-4 dDfbLj"]'
                                                               '/div[@class="style__StyledRatingList-sc-7xd6qw-6 eMNcac"]/span')
    print(len(containers_saled_products))
    saled_products = [container_saled_product.text for container_saled_product in containers_saled_products]

    #######################################################################################################################################

    containers_images = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/main/div[@class="Container-sc-itwfbd-0 hfMLFx"]/'
                                                       'div[@class="CategoryViewstyle__ContentWrap-sc-bhstkd-0 goUqEt"]/'
                                                       'div[@class="CategoryViewstyle__Right-sc-bhstkd-1 jxmsjJ"]/div/'
                                                       'div[@data-view-id="product_list_container"]/div/div/a/'
                                                       'span/div[@class="styles__ThumbnailStyled-sc-54568x-0 cvfill thumbnail"]/'
                                                       'div/div/picture/img')
    print(len(containers_images))
    images = [container_image.get_attribute("src") for container_image in containers_images]

    ########################################################################################################################################

    max_len = max(len(links), len(name_products), len(images), len(org_prices), len(saled_products), len(discounts))

    links += [float('NaN')] * (max_len - len(links))
    name_products += [float('NaN')] * (max_len - len(name_products))
    images += [float('NaN')] * (max_len - len(images))
    org_prices += [float('NaN')] * (max_len - len(org_prices))
    saled_products += [float('NaN')] * (max_len - len(saled_products))
    discounts += [float('NaN')] * (max_len - len(discounts))

    tiki_dict = {"name_product": name_products,
               "price_org": org_prices, "discount": discounts,
               "saled": saled_products, "image": images, "link": links}
    tiki_df = pd.DataFrame(tiki_dict)
    tiki_df['discount'].fillna('-0%', inplace=True)
    tiki_df['saled'].fillna(0, inplace=True)
    time.sleep(1.5)
    return tiki_df


def scrape_Tiki_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_Tiki(url)
        list_df.append(df)
    return list_df


def create_csv_file(df,file_name):
    file = f'{file_name}_{day_month_year}.csv'
    file_export = os.path.join(app_path, file)
    df.to_csv(file_export, header=True, encoding="utf-8-sig", index=False)


def merge_df(dataframes):
    return pd.concat(dataframes, axis=0)


def cleaning(df):
    if type(df) == list:
        return df.drop_duplicates()
    return df


def read_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(line.strip())
    return data


def write_to_file(lst, filename):
    with open(filename, 'w') as f:
        for item in lst:
            f.write(str(item) + '\n')
    

list_tiki = read_file("url_list\\tiki_product_smart_digital.txt")


if __name__ == '__main__':
    start = time.time()
    df_Tiki = scrape_Tiki_s(list_tiki)
    final_dataframe_Tiki = merge_df(df_Tiki)
    create_csv_file(final_dataframe_Tiki, file_name="Info_Tiki_Product")
    now = time.time()
    time_process = now-start
    print(time_process)
    driver.quit()
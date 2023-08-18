import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import pandas as pd
import os
from datetime import datetime
import sys


app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")
path = "D:\microsoftdriver_autotest_114\msedgedriver.exe"
service = Service(executable_path=path)
options = webdriver.EdgeOptions()
options.add_argument("--headless")
# options.add_argument('--disable-extensions')
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-setuid-sandbox')
# options.add_argument('--remote-debugging-port=9222')
# options.add_argument('--disable-browser-side-navigation')
# options.add_argument('--disable-gpu-sandbox')
# options.add_argument('--disable-accelerated-2d-canvas')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--disable-popup-blocking')
# options.add_argument('--disable-notifications')
# options.add_argument(f'--proxy-server={proxy_sever}')
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.864.75")
# options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
# options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edge/86.0.622.63")
# options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299")
# options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134")
driver = webdriver.Edge(service=service, options=options)

def scrape_Nettruyen(website):
    time.sleep(3)
    driver.get(website)
    driver.set_page_load_timeout(10.0)
    driver.set_script_timeout(10.0)
    titles, links, lastest_chap_list, teasers, discriptions, types, conditions, views, follows = [], [], [], [], [], [], [], [], []
    containers = driver.find_elements(by="xpath", value='*//div[@class="row"]/div//div/div/div/div[@class="row"]/div[@class="item"]')
    for container in containers:
        title = container.find_element(by="xpath", value='./figure/figcaption/h3/a').text
        link = container.find_element(by="xpath", value='./figure/figcaption/h3/a').get_attribute("href")
        latest_chap = container.find_element(by="xpath", value='./figure/figcaption/ul/li[@class="chapter clearfix"][1]/a').text
        teaser = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div/a/img').get_attribute("data-original")
        sub_container_invisible = container.find_element(by="xpath", value='./div')
        driver.execute_script("return arguments[0].removeAttribute('style')", sub_container_invisible)
        discription = container.find_element(by="xpath", value='./div/div/div[@class="box_text"]').text
        type = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div[@class="message_main"]/p[label[contains(text(),"Thể loại:")]/following-sibling::text()]').text
        condition = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div[@class="message_main"]/p[label[contains(text(),"Tình trạng:")]/following-sibling::text()]').text
        view = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div[@class="message_main"]/p[label[contains(text(),"Lượt xem:")]/following-sibling::text()]').text
        follow = container.find_element(by="xpath", value='./div/div/div[@class="clearfix"]/div[@class="message_main"]/p[label[contains(text(),"Theo dõi:")]/following-sibling::text()]').text
        titles.append(title)
        links.append(link)
        lastest_chap_list.append(latest_chap)
        teasers.append(teaser)
        discriptions.append(discription)
        types.append(type)
        conditions.append(condition)
        views.append(view)
        follows.append(follow)
    topDay_manga_dict = {"titles": titles, "lastest_Chap": lastest_chap_list, "types": types, "views": views, "follows":follows,
                         "condition": conditions, "discription": discriptions, "teasers": teasers, "links ": links}
    topDay_manga_df = pd.DataFrame(topDay_manga_dict)
    time.sleep(1.5)
    return topDay_manga_df
    pass


def scrape_Nettuyen_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_Nettruyen(url)
        list_df.append(df)
    return list_df


def cleaning(df):
    if type(df) == list:
        return df.drop_duplicates()
    return df
    pass


def create_csv_file(df,file_name):
    file = f'{file_name}_manga_{day_month_year}.csv'
    file_export = os.path.join(app_path, file)
    final_df = cleaning(df)
    final_df.to_csv(file_export, header=True, encoding="utf-8-sig", index=False)
    pass


def merge_df(dataframes):
    return pd.concat(dataframes, axis=0)
    pass


def read_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(line.strip())
    return data


list_Nettruyen = read_file("url_list\\manga_nettruyen_for_testing.txt")

if __name__ == '__main__':
    df_Nettuyen = scrape_Nettuyen_s(list_Nettruyen)
    final_dataframe_Nettruyen = merge_df(df_Nettuyen)
    create_csv_file(final_dataframe_Nettruyen, file_name="topDayNettruyen")
    driver.quit()
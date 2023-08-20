import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import pandas as pd
import os
from datetime import datetime
import sys
from selenium.common.exceptions import NoSuchElementException


path = " D:\microsoftdriver_autotest_114\msedgedriver.exe"
service = Service(executable_path=path)
options = webdriver.EdgeOptions()
options.add_argument("--headless")
driver = webdriver.Edge(service=service, options=options)
app_path = os.path.dirname(sys.executable)
current_day = datetime.now()
day_month_year = current_day.strftime("%d%m%y")


def merge_df(dataframes):
    return pd.concat(dataframes, axis=0)


def cleaning(df):
    if type(df) == list:
        return df.drop_duplicates()
    return df


def create_csv_file(df,file_name):
    file = f'{file_name}_{day_month_year}.csv'
    file_export = os.path.join(app_path, file)
    final_df = cleaning(df)
    final_df.to_csv(file_export, header=True, encoding="utf-8-sig", index=False)


def scrape_TheSun(website):
    driver.get(website)
    driver.fullscreen_window()

    link_containers = driver.find_elements(by="xpath", value='//div/div[@class="teaser__copy-container"]/a')
    print(len(link_containers))

    title_containers = driver.find_elements(by="xpath", value='//div/div[@class="teaser__copy-container"]/a/h3')
    print(len(title_containers))

    try:
        discription_containers = driver.find_elements(by="xpath",
                                                      value='//div/div[@class="article-data teaser__social"]'
                                                            '//div[@class="article-data__item article-data__tag"]/a')
        print(len(discription_containers))
    except NoSuchElementException:
        discription_containers = driver.find_elements(by="xpath",
                                                      value='//div/div[@class="teaser__copy-container"]/a/p')
        print(len(discription_containers))

    illutration_containers = driver.find_elements(by="xpath", value='//div/div[@class="teaser__image-container"]'
                                                    '//div[@class="teaser__image-anchor-tag"]/picture/img')
    print(len(illutration_containers))

    links = [link.get_attribute("href") for link in link_containers]
    titles = [title.text for title in title_containers]
    discriptions = [discription.text for discription in discription_containers]
    illutrations = [illutration.get_attribute("data-src") for illutration in illutration_containers]

    max_len = max(len(links), len(titles), len(discriptions), len(illutrations))

    links += [float('NaN')] * (max_len - len(links))
    titles += [float('NaN')] * (max_len - len(titles))
    discriptions += [float('NaN')] * (max_len - len(discriptions))
    illutrations += [float('NaN')] * (max_len - len(illutrations))

    TheSun_dict = {"title": titles, "discription": discriptions,
                        "illutration": illutrations, "link": links}

    TheSun_df = pd.DataFrame(TheSun_dict)
    return TheSun_df


def scrape_Women_Heath_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_TheSun(url)
        list_df.append(df)
    return list_df


def scrape_Men_Heath_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_TheSun(url)
        list_df.append(df)
    return list_df


def scrape_WorldNews_s(list_url):
    list_df = []
    for url in list_url:
        df = scrape_TheSun(url)
        list_df.append(df)
    return list_df


def read_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(line.strip())
    return data

list_women_heath = read_file("url_list\\woman_heath.txt")
list_men_heath = read_file("url_list\\man_heath.txt")
list_world_news = read_file("url_list\\world_news.txt")


if __name__ == '__main__':
    '''Run each part (woman heath, man heath, world news) dependently'''
    women_heath_Df = scrape_Women_Heath_s(list_women_heath)
    men_heath_Df = scrape_Men_Heath_s(list_men_heath)
    worldnews_DF = scrape_WorldNews_s(list_world_news)
    final_women_heath_DF = merge_df(women_heath_Df)
    final_men_heath_DF = merge_df(men_heath_Df)
    final_worldnews_DF = merge_df(worldnews_DF)
    create_csv_file(final_women_heath_DF, "women_heath_TheSun")
    create_csv_file(final_men_heath_DF, "man_heath_TheSun")
    create_csv_file(final_worldnews_DF, "worldnews_TheSun")
    driver.quit()
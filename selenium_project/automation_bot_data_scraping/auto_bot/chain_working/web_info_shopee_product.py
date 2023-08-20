import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException
class web_info_():
    def __init__(self):
        path = "D:\microsoftdriver_autotest_114\msedgedriver.exe"
        service = Service(executable_path=path)
        options = webdriver.EdgeOptions()
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.864.75")
        options.add_argument('--disable-popup-blocking')
        self.driver = webdriver.Edge(service=service, options=options)
        self.urls = []
        self.website = "https://shopee.vn/"

        self.driver.implicitly_wait(15)

    def get_current_url(self):
        return self.driver.current_url

    def input_data(self):
        self.product_tag = input('Product tag for search : ')
        self.product_type = input('Product type for search : ')
        self.num_pages = int(input('Num pages scrape : '))
        self.file_name = input('File name store url : ')

    def search(self, product_tag, product_type):

        self.driver.get(self.website)
        self.driver.maximize_window()
        self.action = ActionChains(self.driver)

        #######################################################################################################################################

        self.driver.implicitly_wait(15)
        tag_to_find = f"{product_tag}"
        tag_xpath_expression =\
        "//*[@id='main']/div/div[2]/div/div/div[3]/div[2]/div[1]/div/div/div[2]/div/div[1]/ul/li/div/a//*[@class='K34m1x']" \
        " [contains(text(), '{}')]".format(tag_to_find)
        time.sleep(2)
        self.tag_choice = self.driver.find_element(By.XPATH, value=tag_xpath_expression)
        self.tag_choice.click()

        #######################################################################################################################################

        self.more_type_option = self.driver.find_element(By.XPATH,
        value='//*[@id="main"]/div/div[2]/div/div/div[4]/div[1]/div[1]/div/div/div[2]/div/div[1]/div')
        self.action.move_to_element(self.more_type_option)
        self.action.click()
        self.action.perform()

        #######################################################################################################################################

        self.driver.implicitly_wait(15)
        try:
            type_to_find = f"{product_type}"
            type_xpath_expression = "//*[@id='main']/div/div[2]/div/div[1]/div[4]/div[1]/div[1]/div/div/div[2]/div/div[2]/div/a " \
            "[contains(text(), '{}')]".format(type_to_find)
            time.sleep(2)
            self.type_choice = self.driver.find_element(By.XPATH, value=type_xpath_expression).get_attribute("href")
        except NoSuchElementException:
            type_to_find = f"{product_type}"
            type_xpath_expression = "//*[@id='main']/div/div[2]/div/div[1]/div[4]/div[1]/div[1]/div/div/div[2]/a" \
            "[contains(text(), '{}')]".format(type_to_find)
            time.sleep(2)
            self.type_choice = self.driver.find_element(By.XPATH, value=type_xpath_expression).get_attribute("href")
        self.driver.get(self.type_choice)

        #######################################################################################################################################

        self.move_to_lastest_area = self.driver.find_element(By.XPATH,
        value='//*[@id="main"]/div/div[2]/div/div/div[3]/div[2]/div/div[1]/div[1]/div[2]')
        self.action.move_to_element(self.move_to_lastest_area)
        self.action.click()
        self.action.perform()

        #######################################################################################################################################

        current_page = self.driver.current_url
        return current_page
        pass

    def navigate_to_next_page(self):
        next_button = self.driver.find_element(By.XPATH,
        value='//*[@id="main"]/div/div[2]/div/div[1]/div[3]/div[2]/div/div[1]/div[2]/button[2]')
        self.action.move_to_element(next_button)
        self.action.click()
        self.action.perform()

    def get_all_urls(self, page, num_pages, file_name):
        self.driver.get(page)
        current_page = self.driver.current_url
        for i in range(num_pages):
            self.urls.append(current_page)
            self.navigate_to_next_page()
            time.sleep(3)
            current_page = self.driver.current_url
        with open(f'.//url_list//{file_name}', 'w') as f:
            for url in self.urls:
                f.write(url + '\n')

    def execute(self):
        self.input_data()
        first_page = self.search(self.product_tag, self.product_type)
        self.get_all_urls(first_page, self.num_pages, file_name=self.file_name)
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
if __name__ == '__main__':
    ob = web_info_()
    ob.execute()
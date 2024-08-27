import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

class web_info_():
    def __init__(self):
        path = ""
        service = Service(executable_path=path)
        options = webdriver.EdgeOptions()
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.864.75")
        options.add_argument('--disable-popup-blocking')
        self.driver = webdriver.Edge(service=service, options=options)
        self.urls = []
        self.website = ""

        self.driver.implicitly_wait(15)

    def get_current_url(self):
        return self.driver.current_url

    def input_data(self):
        self.book_tag = input('Book tag for search : ')
        self.book_type = input('Book type for search : ')
        self.num_pages = int(input('Num pages scrape : '))
        self.file_name = input('File name store url : ')

    def search(self, book_tag, book_type):
        self.driver.get(self.website)
        self.driver.maximize_window()

        #######################################################################################################################################

        self.action = ActionChains(self.driver)
        self.menu = self.driver.find_element(By.XPATH, value='//*[@id="header"]/div[1]/div[2]/div/div[2]/span[@class="icon_menu"]')
        self.action.move_to_element(self.menu)
        self.action.perform()

        #######################################################################################################################################

        self.tag = self.driver.find_element(By.XPATH, value=f'//*[@id="header"]/div[1]/div[2]/div/div[2]/'
                                                            f'div[1]/div/div[1]/ul/li/a[@title="{book_tag}"]')
        self.action.move_to_element(self.tag)
        self.action.click()
        self.action.perform()

        #######################################################################################################################################

        self.driver.implicitly_wait(15)
        self.more_choice = self.driver.find_element(By.XPATH, value='//*[@id="m-more-less-left_category"]/a[2]')
        self.action.move_to_element(self.more_choice)
        self.action.click()
        self.action.perform()

        #######################################################################################################################################

        self.group_by = self.driver.find_element(By.XPATH,
        value='//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[5]/div[4]/div[1]/div/div[2]/div/div/div/div')
        self.action.move_to_element(self.group_by)
        self.action.click()
        self.action.perform()

        #######################################################################################################################################

        self.choose_group_by = self.driver.find_element(By.XPATH,
        value='//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[5]/div[4]/div[1]/div/div[2]/div/div/div/div/div/span[@value="48"]')
        self.action.move_to_element(self.choose_group_by)
        self.action.click()
        self.action.perform()

        #######################################################################################################################################

        time.sleep(2)
        self.choice = self.driver.find_element(By.XPATH, value=f'//*[@id="children-categories"]/li/a[@title="{book_type}"]')
        self.action.move_to_element(self.choice)
        self.action.click()
        self.action.perform()

        #######################################################################################################################################

        current_page = self.driver.current_url
        return current_page
        pass

    def navigate_to_next_page(self):
        for i in range(200):
            self.driver.execute_script(f"window.scrollTo(0, {str(i)}00);")
        next_button = self.driver.find_element(By.XPATH, value='//*[@id="pagination"]/ol/li/a/div[@class="icon-turn-right"]')
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
        first_page = self.search(self.book_tag, self.book_type)
        self.get_all_urls(first_page, self.num_pages, file_name=self.file_name)
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
if __name__ == '__main__':
    ob = web_info_()
    ob.execute()
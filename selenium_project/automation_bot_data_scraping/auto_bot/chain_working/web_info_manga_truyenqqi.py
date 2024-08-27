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
        # website can be changed, replace with a suitable url
        self.website = ""

        self.driver.implicitly_wait(15)

    def get_current_url(self):
        return self.driver.current_url

    def input_data(self):
        self.id_manga_type = int(input('Manga id for search : '))
        self.num_pages = int(input('Num pages scrape : '))
        self.file_name = input('File name store url : ')

    def search(self, id):

        self.driver.get(self.website)
        self.driver.maximize_window()
        time.sleep(2)

        #######################################################################################################################################

        self.action = ActionChains(self.driver)
        self.driver.implicitly_wait(15)
        self.find_ = self.driver.find_element(By.XPATH,
        value='//*[@id="header_left_menu"]/li[6]/a[@class="tags_name pc_hover"]').get_attribute("href")
        self.driver.get(self.find_)
        time.sleep(2)

        xpath_expression =f'//*[@id="main_homepage"]/div[2]/div[2]/div[3]/div[2]/div/span[@data-id={id}]'
        self.choice = self.driver.find_element(By.XPATH, value=xpath_expression)
        self.action.move_to_element(self.choice)
        self.action.click()
        self.action.perform()
        self.driver.implicitly_wait(15)
        self.start_finding = self.driver.find_element(By.XPATH,
        value='//*[@id="main_homepage"]/div[2]/div[2]/div[6]/div/button[@class="btn btn-success btn-search is-danger"]')

        self.start_finding.click()
        current_page = self.driver.current_url
        return current_page
        pass

    def navigate_to_next_page(self):
        for i in range(200):
            self.driver.execute_script(f"window.scrollTo(0, {str(i)}00);")
        next_button = self.driver.find_element(By.XPATH,
        value='//*[@id="main_homepage"]/div[5]/a[8]/p')
        self.action.move_to_element(next_button)
        self.action.click()
        self.action.perform()

    def get_all_urls(self, page, num_pages, file_name):
        self.driver.get(page)
        current_page = self.driver.current_url
        first_page_done = True
        for i in range(num_pages):
            self.urls.append(current_page)
            if(first_page_done):
                next_button = self.driver.find_element(By.XPATH,
                value='//*[@id="main_homepage"]/div[5]/a[6]/p')
                self.action.move_to_element(next_button)
                self.action.click()
                self.action.perform()
                first_page_done = False
                current_page = self.driver.current_url
                time.sleep(2)
                continue
            self.navigate_to_next_page()
            time.sleep(2)
            current_page = self.driver.current_url
        with open(f'.//url_list//{file_name}', 'w') as f:
            for url in self.urls:
                f.write(url + '\n')

    def execute(self):
        self.input_data()
        first_page = self.search(self.id_manga_type)
        self.get_all_urls(first_page, self.num_pages, file_name=self.file_name)
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
if __name__ == '__main__':
    ob = web_info_()
    ob.execute()
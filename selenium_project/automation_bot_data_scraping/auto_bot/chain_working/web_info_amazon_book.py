import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException
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
        self.product_tag = input('Product tag for search : ')
        self.product_type = input('Product type for search : ')
        self.product_type_details = input('Product type details for search : ')
        self.num_pages = int(input('Num pages scrape : '))
        self.file_name = input('File name store url : ')

    def search(self, product_tag, product_type, product_details):

        self.driver.get(self.website)
        self.driver.maximize_window()
        #######################################################################################################################################

        self.action = ActionChains(self.driver)

        #######################################################################################################################################

        self.driver.implicitly_wait(15)
        book_area = "Books"
        xpath = "//*[@id='nav-xshop']/a [contains(text(), '{}')]".format(book_area)
        time.sleep(2)
        self.book_store = self.driver.find_element(By.XPATH, value=xpath).get_attribute("href")
        self.driver.get(self.book_store)

        #######################################################################################################################################

        self.driver.implicitly_wait(15)
        tag_to_find = f"{product_tag}"
        tag_xpath_expression = "//*[@id='s-refinements']/div[3]/ul/li/span/a/span [contains(text(), '{}')]".format(tag_to_find)
        time.sleep(2)
        self.tag_choice = self.driver.find_element(By.XPATH, value=tag_xpath_expression)
        self.tag_choice.click()

        #######################################################################################################################################

        self.driver.implicitly_wait(15)
        type_xpath_expression = "//*[@id='s-refinements']//li[@class='a-spacing-micro apb-browse-refinements-indent-2']/span/a/span"
        time.sleep(2)
        self.type_choice = self.driver.find_elements(By.XPATH, value=type_xpath_expression)
        for elem in self.type_choice:
            if elem.text == product_type:
                elem.click()
                break

        #######################################################################################################################################

        self.driver.implicitly_wait(15)
        type_details_xpath_expression = '//*[@id="s-refinements"]//li[@class="a-spacing-micro apb-browse-refinements-indent-2"]' \
                                        '/span/a[@class="a-color-base a-link-normal"]/span'
        time.sleep(2)
        self.final_choice = self.driver.find_elements(By.XPATH, value=type_details_xpath_expression)
        for elem in self.final_choice:
            if elem.text == product_details:
                elem.click()
                break

        #######################################################################################################################################

        time.sleep(2)
        try:
            self.driver.implicitly_wait(15)
            self.show_more = self.driver.find_element(By.XPATH,
            value='//*[@class="a-section a-spacing-none"]//div[3]/div/div/a[@class="a-link-normal"]')
            self.action.move_to_element(self.show_more)
            self.action.click()
            self.action.perform()
        except NoSuchElementException:
            print('Go thorugh, no more selection . ')

        #######################################################################################################################################

        current_page = self.driver.current_url
        return current_page
        pass

    def navigate_to_next_page(self):
        for i in range(200):
            self.driver.execute_script(f"window.scrollTo(0, {str(i)}00);")
        text_to_find = 'Next'
        xpath_expression = '//*[@id="search"]//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]'.format(text_to_find)
        next_button = self.driver.find_element(By.XPATH, value=xpath_expression)
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
        first_page = self.search(self.product_tag, self.product_type, self.product_type_details)
        self.get_all_urls(first_page, self.num_pages, file_name=self.file_name)
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
if __name__ == '__main__':
    ob = web_info_()
    ob.execute()
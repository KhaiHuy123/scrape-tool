import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
try:
    website = 'https://www.fahasa.com/'
    driver_path = ""
    def select_place_product(product):
        search_field = driver.find_element(By.XPATH, value='//*[@id="search_desktop"]')
        search_field.send_keys(product)
        search_button = driver.find_element(By.XPATH, value='//*[@id="search_mini_form_desktop"]/div/div/span')
        search_button.click()
    def change_to_in_stock_area(driver):
        in_stock = driver.find_element(By.XPATH, value='//*[@class="selectBox selectBox-in-stock"]')
        in_stock.click()
        select_in_stock_option = driver.find_element(By.XPATH, value='//*[@class="selectOption selectOption-in-stock"]')
        select_in_stock_option.click()
    def choose_product(driver):
        driver.implicitly_wait(15)
        product = driver.find_element(By.XPATH,
        value='//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[5]/div[2]/ul/li[1]/div/div[2]/h2/a')
        WebDriverWait(driver, 5)
        product.click()
    def add_to_cart(driver):
        driver.implicitly_wait(15)
        cart = driver.find_element(By.CSS_SELECTOR, value='.btn-buy-now')
        cart.click()
    def payment(driver):
        driver.implicitly_wait(15)
        driver.refresh()
        payment = driver.find_element(By.XPATH, value='//*[@id="checkbox-all-products"]')
        payment.click()
    def submit(driver):
        driver.implicitly_wait(15)
        driver.refresh()

        ##################################################################################################################################

        pay_button = driver.find_element(By.XPATH, value='//*[@id="form-cart"]/div/div[2]/div/div/div[3]/div[2]/div/button')
        pay_button.click()

        ##################################################################################################################################

        name = driver.find_element(By.XPATH, value='//*[@id="fhs_shipping_fullname"]')
        name.send_keys(f'{name_client}')

        ##################################################################################################################################

        email = driver.find_element(By.XPATH, value='//*[@id="fhs_shipping_email"]')
        email.send_keys(f'{email_recv}')

        ##################################################################################################################################

        phone_number = driver.find_element(By.XPATH, value='//*[@id="fhs_shipping_telephone"]')
        phone_number.send_keys(f'{phone}')

        ##################################################################################################################################

        city_province = driver.find_element(By.CSS_SELECTOR,
        value='#select2-fhs_shipping_city_select-container')
        city_province.click()
        input_city = driver.find_element(By.XPATH,
        value='//*[@id="offcanvas-container"]/span/span/span[1]/input')
        input_city.send_keys(f'{city}')
        city_choice = driver.find_element(By.XPATH,
        value='//*[@id="select2-fhs_shipping_city_select-results"]/li[1]')
        city_choice.click()
        time.sleep(1)

        ##################################################################################################################################

        district = driver.find_element(By.CSS_SELECTOR,
        value='#select2-fhs_shipping_district_select-container')
        district.click()
        input_district = driver.find_element(By.XPATH,
        value='//*[@id="offcanvas-container"]/span/span/span[1]/input')
        input_district.send_keys(f'{district_name}')
        district_choice = driver.find_element(By.XPATH,
        value='//*[@id="select2-fhs_shipping_district_select-results"]/li[1]')
        district_choice.click()
        time.sleep(5)

        ##################################################################################################################################

        ward = driver.find_element(By.CSS_SELECTOR,
        value='#select2-fhs_shipping_wards_select-container')
        ward.click()
        input_ward = driver.find_element(By.XPATH,
        value='//*[@id="offcanvas-container"]/span/span/span[1]/input')
        input_ward.send_keys(f'{ward_name}')
        ward_choice = driver.find_element(By.XPATH,
        value='//*[@id="select2-fhs_shipping_wards_select-results"]/li')
        ward_choice.click()
        time.sleep(1)

        ##################################################################################################################################

        adress = driver.find_element(by='xpath', value='//*[@id="fhs_shipping_street"]')
        adress.send_keys(f'{adress_name}')
    def execute():
        # send keys to input field (product's name) and click search button
        select_place_product(name_product)
        # move to available product list
        change_to_in_stock_area(driver)
        # click to product
        choose_product(driver)
        # Add to cart
        add_to_cart(driver)
        # Start payment process
        payment(driver)
        # Submit
        submit(driver)
        time.sleep(15)
        driver.quit()
    def input_info():
        global name_product, name_client, email_recv, phone, city, district_name, ward_name, adress_name
        name_product = input('Name_product : ')
        name_client = input('Client : ')
        email_recv = input('Email : ')
        phone = input('Phone : ')
        city = input('City : ')
        district_name = input('District : ')
        ward_name = (input('Ward : '))
        adress_name = input('Adress : ')
    #################################################################################################################################

    input_info()

    #################################################################################################################################

    service = Service(executable_path=driver_path)
    options = webdriver.EdgeOptions()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko")
    driver = webdriver.Edge(service=service, options=options)
    driver.implicitly_wait(15)
    driver.maximize_window()
    driver.get(website)

    #################################################################################################################################

    execute()

except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:raise

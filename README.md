# Scrape Tool

Data collection is one of the most crucial steps before building any applications. We need to know where the data comes from. Does it come from heaven? No, data can be collected from various sources such as published databases, websites, the cloud, and more. In this repository, the main focus is on collecting data from websites, which is achieved through the use of two popular Python frameworks: Selenium and Scrapy.

Why Python? Well, the answer is simple. Python is straightforward and easy to use. I can just say that.

Each framework has its own advantages. Selenium is commonly used for automating web browsers and performing a series of actions on them (known as "chain-working"). This makes it useful for scenarios where complex interactions, like moving to specific elements, performing double-clicks, or right-clicking, are required. However, using Selenium for web scraping might not always be the best idea. There are cases where Selenium can handle complex websites with JavaScript-related issues that Scrapy struggles with. Maybe the structure of Java-Selenium program is more flexible to maintain than Python's. In some cases, developers even prefer using Java with Selenium due to these reasons. Selenium relies on a webdriver to work, which is a core-component for enabling Selenium to interact with browsers.

On the other hand, Scrapy is a more complex framework structured around Object-Oriented Programming (OOP) principles. Unlike Selenium, which can work effectively within a single module, Scrapy projects are organized into five modules: items.py, middleware.py, settings.py, spider.py, and pipelines.py. The complexity of Scrapy allows for more tasks beyond simple data collection, such as storing data in databases. This is the point, shines_data can be collected and structure in database system and later used in applications. For example, we can manage onlinebooks database like this :

![image](https://github.com/KhaiHuy123/scrape_tool/assets/86825653/748ab497-4b87-4bc7-b2f0-46d9ed7895c0)


A significant challenge with tools created by these frameworks is the need for occasional maintenance due to updates. The structure of the target websites may change several times in the future. Since data collection relies on web elements and their attributes (using CSS, XPath, etc.), these changes can affect the scraping process.

This repository is a work in progress. One future update is to run Scrapy spiders on the cloud. Nowadays, various services such as DigitalOcean and Scrapyd, provide solutions for running scraping tools and storing data on the cloud. Additionally, building applications like web apps or desktop apps ensures that the scraping efforts are not in vain. For this purpose, I created a simple desktop app using Python's Tkinter framework, which facilitates app development.

Please note that the information presented here might be incomplete or incorrect. For any questions or clarifications, feel free to contact me at nkhuy1109@gmail.com.

Thank you for your interest.

More Information:

**Selenium Framework:**
- [Selenium Python API Documentation](https://www.selenium.dev/selenium/docs/api/py/api.html)
- [Selenium with Python Documentation](https://selenium-python.readthedocs.io/index.html)
- [Selenium Example Gist](https://gist.github.com/baijum/1047207/1ac84b1ae076e3d59e994a00bada0bf4bee5fd63)

**Scrapy Framework:**
- [Scrapy Documentation](https://docs.scrapy.org/en/latest/)

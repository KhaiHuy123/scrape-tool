# scrape_tool

Data Colection seems to be one of the most important sections before building any applications. We just need to know where data came from. They come from Heaven ? No, data can be collected from different sources like published database, website, cloud, blah blah ... And yes, data collected from website is the main topic in this respository. 
Here, I'm using one ... oh sorry but two popular frameworks to solve this problem. 

Guess what, It's Automation-Web Scraping using Selenium and Scrapy in Python Programming Language
Why Python ? .... :) Because it's simple, I can just say that 

Each framework has advantages itself, Selenium usually used for automating web browser or we can say chain-working (chain of actions on web browser like : move to that object and perform double click or right click  and do next action like send keys to input field ... Consequence of these actions is the creation of chain-working on web browser ... ). But using this framework for web-scraping not supposed to be the good idea. In some case, Selenium can be used for excecuting complex website contains issue of JavaScript problems that Scrapy can not handle well. And people sometimes prefer using Java Programming Language to build a Selenium tool than Python Programming Language. When using Selenium, we need support form webdriver - this guy is the main key which helps our Selenium tool become available to work. About Scrapy, this framework is super complex ...  and structured by OOP (Oriented Objetc Programming). Unlike Selenium tool, which can fully work in just 1 module. Scrapy project includes 5 modules : items.py , middleware.py , settings.py , spider.py , pipeline.py . Scrapy with its complex nature allow us to do more tasks than just collect data from website like : storing data into database ... And this is the point. We can store data into database and later use it for our applications by using Scrapy.    

Another challenge is the tools created by those framework that they need to be maintained ocasionally for the update version. Why ? Because the structure of target website can change serveral times in the future. We colect data base on web element on website (using css, xpath, ...) so that is the reason

This respository is not completed yet. Two things think I need to update is to run Scrapy spider on cloud and create the application for using data collected. Nowadays, there are so many services that provide the answer for run application to scrape and store data on cloud like DigitalOcean, Scrapyd ... And after all, we need to build a application like web-app, destop-app to make sure that our scraping-job is not useless ...  I gonna complete remain problems in the future

Information here can be missed or incorrect anyway. If having any questions, contact me by this : nkhuy1109@gmail.com 

Thanks for your consideration

More info : 

Selenium FrameWork : 

  https://www.selenium.dev/selenium/docs/api/py/api.html
  
  https://selenium-python.readthedocs.io/index.html
  
  https://gist.github.com/baijum/1047207/1ac84b1ae076e3d59e994a00bada0bf4bee5fd63

Scrapy FrameWork :

  https://docs.scrapy.org/en/latest/
  

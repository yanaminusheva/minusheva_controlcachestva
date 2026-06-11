import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='function')
def driver():
    if not os.path.exists('report'):
        os.makedirs('report')
        
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1280,800')
    options.add_argument('--log-level=3')  
    
    try:
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
    except UnicodeDecodeError:
        service = Service()

    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()
import pathlib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
path_to_driver = pathlib.Path(__file__).parent.resolve() / 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=str(path_to_driver),
                          options=chrome_options)
from selenium import webdriver

options = webdriver.FirefoxOptions()

# headless mode

# user-agent
options.set_preference("general.useragent.override",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                       "like Gecko) Chrome/90.0.4430.212 Safari/537.36")
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.212 Safari/537.36 "
}
# disable webdriver mode
options.set_preference("dom.webdriver.enabled", False)
driver = webdriver.Firefox(
    executable_path="C:\\Users\\Admin\\Desktop\\python\\kwork\\Alex888\\geckodriver.exe",
    options=options
)

driver.get('https://www.instagram.com/satilazzer/')
print(driver.current_url)
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://toutiao.com/group/6819520651116675596")
driver.implicitly_wait(60)
text = driver.page_source()

print(text)
# driver.quit()

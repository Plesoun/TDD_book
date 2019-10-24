from selenium import webdriver

browser = webdriver.Firefox(executable_path='C:\\Users\\jakub\\OneDrive\\Documents\\Python Scripts\\TDD\\geckodriver.exe')
browser.get("http://localhost:8000")

assert "Django" in browser.title

browser.close()

# Selenium自動化測試 - 天攏書店搜尋書本 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import time
import pytest
import allure
import requests

# 開啟瀏覽器，並使用Cookie保持登入狀態
def OpenBrowser():  
    driver = webdriver.Chrome()
    driver.get("XXXXXXXX")
    driver.maximize_window()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    driver.delete_all_cookies()
    driver.add_cookie({'X1'})
    driver.add_cookie({'X2'})
    driver.add_cookie({'X3'})
    
    driver.refresh()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    return driver

def CloseBrowser(driver):
    driver.quit()

# 測試項目1:搜尋框空搜尋書本 > 預期因未輸入值，而會出現警示訊息，"請輸入搜尋關鍵字"
@pytest.mark.NullSearch   
def test_NullSearch(): 
    driver=OpenBrowser()

    try:
        driver.find_element(By.CSS_SELECTOR, ".top-search > form > #keyword")
    except:
        print('Search Element 請重新嘗試定位')

    driver.find_element(By.CSS_SELECTOR, ".h-5").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    
    空搜尋提示文字 = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div").text
    assert  "請輸入搜尋關鍵字喔" in 空搜尋提示文字

    driver.save_screenshot("測項1_空搜尋提示文字截圖.png")

    CloseBrowser(driver)

# 測項項目2:搜尋"探索網頁前端資安宇宙" > 預期搜尋結果，會出現輸入關鍵字的書名，且頁面資訊正確
@pytest.mark.SearchBook
def test_SearchBook(): 
    driver=OpenBrowser()

    driver.find_element(By.CSS_SELECTOR, ".top-search > form > #keyword").send_keys("探索網頁前端資安宇宙")
    driver.find_element(By.CSS_SELECTOR, ".h-5").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    search_keyword = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div[4]/ul/li[1]/div/div/strong/a').text 
                                                                
    assert  "探索網頁前端資安宇宙" in search_keyword

    driver.save_screenshot("測項2_前端搜尋結果截圖.png")

    CloseBrowser(driver)

# 測試項目3:點選書本(探索網頁前端資安宇宙) > 預期進入書本詳細頁面，且頁面資訊正確
@pytest.mark.ClickSearch
def test_ClickSearch(): 
    driver=OpenBrowser()

    driver.find_element(By.CSS_SELECTOR, ".top-search > form > #keyword").send_keys("探索網頁前端資安宇宙")
    driver.find_element(By.CSS_SELECTOR, ".h-5").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div/div/div/div[4]/ul/li[1]/div/div/strong/a").click()

    search_data = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div[1]/article/section[1]/div[1]/div[1]/h1').text 
    assert  "Beyond XSS：探索網頁前端資安宇宙" in search_data

    driver.save_screenshot("測項3_進入書本詳細頁.png")

    CloseBrowser(driver)

# 測試項目4:將書本(探索網頁前端資安宇宙)放入購物車 > 預期購屋車購買數量，會顯示"1"
@pytest.mark.Shopping
def test_Shopping():  # 測4 = 放入購物車 > 預期購物車數量顯示正確 
    driver=OpenBrowser()

    driver.find_element(By.CSS_SELECTOR, ".top-search > form > #keyword").send_keys("探索網頁前端資安宇宙")
    driver.find_element(By.CSS_SELECTOR, ".h-5").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div/div/div/div[4]/ul/li[1]/div/div/strong/a").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div[1]/article/section[1]/div[1]/div[2]/ul/div/div[2]/form[1]/input[1]").click()
    # 放入購物車
    time.sleep(5)

    Shopping = driver.find_element(By.XPATH,"/html/body/div[3]/nav[1]/nav/ul/li[5]").text
 
    assert  "1" in Shopping

    driver.save_screenshot("測項4_購買商品數量顯示.png")

    CloseBrowser(driver)
test_Shopping()


# 測試項目5:檢查購物車列表 > 預期購物車列表有所放書本
@pytest.mark.ShoppingList
def test_ShoppingList():   
    driver=OpenBrowser()

    driver.find_element(By.CSS_SELECTOR, ".top-search > form > #keyword").send_keys("探索網頁前端資安宇宙")
    driver.find_element(By.CSS_SELECTOR, ".h-5").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div/div/div/div[4]/ul/li[1]/div/div/strong/a").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div[1]/article/section[1]/div[1]/div[2]/ul/div/div[2]/form[1]/input[1]").click()

    driver.find_element(By.XPATH,"/html/body/div[3]/nav[1]/nav/ul/li[5]").click()
    # Shopping_Car

    ShoppingList = driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div[1]/div/table/tbody/tr/td[2]").text
    assert  "Beyond XSS：探索網頁前端資安宇宙" in ShoppingList

    driver.save_screenshot("測項5_購物車清單.png")

# 測試項目6 = 清空購物車 > 預期清除的資料不會顯示於購物車
@pytest.mark.CancelList
def test_CancelList():   
    driver=OpenBrowser()

    driver.find_element(By.CSS_SELECTOR, ".top-search > form > #keyword").send_keys("探索網頁前端資安宇宙")
    driver.find_element(By.CSS_SELECTOR, ".h-5").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div/div/div/div[4]/ul/li[1]/div/div/strong/a").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 
    
    driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div[1]/article/section[1]/div[1]/div[2]/ul/div/div[2]/form[1]/input[1]").click()
    # 放入購物車

    driver.find_element(By.XPATH,"/html/body/div[3]/nav[1]/nav/ul/li[5]").click()
    # Shopping_Car

    driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div[1]/div/table/tbody/tr/td[7]/a[2]").click()
    # CancelList

    購物車清空提示文字 = driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div[1]/div/div[1]/p").text
    assert  "購物車內目前沒有商品" in 購物車清空提示文字

    driver.save_screenshot("測項6_購物車清空.png")

# 測試項目7 = 連結驗證　＞　預期連結導向正確頁面
@pytest.mark.Linkcompany 
def test_Linkcompany():   
    driver=OpenBrowser()

    Linkcompany =  driver.find_element(By.XPATH,"/html/body/div[3]/nav[2]/ul/li[12]/a").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/footer'))) 

    company = driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div/div/div/h1").text
    assert  "台北總店" in company

    driver.save_screenshot("測項7_門市資訊頁面.png")





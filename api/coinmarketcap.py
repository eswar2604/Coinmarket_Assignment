# api/coinmarketcap.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException


class CoinMarketCap:
    def __init__(self):
        options = Options()
        options.headless = True
        service = Service('C:\\Users\\esuriset\\Documents\\crypto_scraper\\ChromeDriver\\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service, options=options)
        url = "https://coinmarketcap.com/currencies/"
        self.driver.get(url)
        self.driver.maximize_window()
        

    def get_coin_data(self, coin):

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.sc-e20acb0c-2.hOTbPo.tooltip'))).click()
        AB = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input.sc-d565189d-3.ctOzuc')))
        AB.send_keys(coin)
        time.sleep(3)  
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'sc-d1ede7e3-0 bwRagp BaseButton_labelWrapper__wzpX7') and .//text()='Cryptoassets']"))).click()
        AB.send_keys(Keys.SPACE)
        AB.send_keys(Keys.ENTER)
        time.sleep(3)  
        abc = self.driver.find_element(By.XPATH,'//*[@id="section-coin-stats"]/div/dl').text
        Contracts = self.driver.find_elements(By.CSS_SELECTOR,"div.sc-d1ede7e3-0.sc-7f0f401-0.sc-96368265-0.bwRagp.gQoblf.eBvtSa.flexStart")
        Source = self.driver.find_elements(By.XPATH,"//div[@class='sc-d1ede7e3-0 sc-7f0f401-0 gRSwoF gQoblf']")
        linkss =self.driver.find_elements(By.XPATH,"//div[@class='sc-d1ede7e3-0 sc-7f0f401-0 gRSwoF gQoblf']/a")
        data = {}
        d1={}
        contract=[]
        source=[]
        linkz=[]
        try:
           
            data['price'] = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="section-coin-overview"]/div[2]/span'))).text
            price_change= WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="section-coin-overview"]/div[2]/div/div/p'))).text
            price_change = price_change.split(' ')[0]
            colourz= self.driver.find_element(By.XPATH,'//*[@id="section-coin-overview"]/div[2]/div/div/p').get_attribute("color")
            if colourz=='red':
                price_change="-"+price_change
            else:
                price_change="+"+price_change
            data['market_cap'] = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="section-coin-stats"]/div/dl/div[1]/div[1]/dd'))).text.split('\n')[1]
            data[ abc.split('\n')[0]] = abc.split('\n')[2]
            data['Market_cap_rank'] = abc.split('\n')[3]
            data[abc.split('\n')[4]]= abc.split('\n')[6]
            data['volume_change'] = abc.split('\n')[5]
            data['Volume change rank'] = abc.split('\n')[7]
            data[abc.split('\n')[8]] = abc.split('\n')[9]
            data[abc.split('\n')[10]] = abc.split('\n')[11]

           
            
            for elem in Contracts:
                d1['name']=elem.text.split(':')[0]
                addresss = elem.find_element(By.XPATH,"//a[@class = 'chain-name']").get_attribute("href")
                addresss=addresss.split('/')[-1]
                d1['address']=addresss

            contract.append(d1)
            data['Contracts'] = contract


            for elem in Source:
                source.append(elem.text)
           
            for elem in linkss:
                linkz.append(elem.get_attribute("href"))

            l1_name = 'name'
            l2_name = 'link'
            combined_list = [{l1_name:item1 ,l2_name:item2} for item1,item2 in zip(source,linkz)]

            data['Official_And_Social_links'] = combined_list

        except ElementNotInteractableException:
            data['Failed']= {
                "Response": "Failed due to un interactable elements in script"
            }

            return data
        
        except NoSuchElementException:
            data['Failed']= {
                "Response": "Didn't fect anything , Plzz Check inputs"
            }
            return data
        
      


        except Exception as e:
            data['Failed']= {
                "Response": "Didn't fect anything , Plzz Check inputs"
            }
            return data
            
        
        print(data)
        return data

    def close(self):
        self.driver.quit()

'''
s1 = CoinMarketCap()
s1.get_coin_data('BTC')
'''

from .base import DNS_provider
from time import sleep
import selenium
from selenium.common.exceptions import TimeoutException
from selenium import webdriver           
import selenium.webdriver
from selenium.webdriver.common.by import By                                       
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.chrome.options import Options# Configure
from selenium.webdriver.chrome.service import Service

class nslookup(DNS_provider):
    def get_ip(self) -> str:
        base_url='https://www.nslookup.io/domains/github.com/dns-records/'

        map={
            'cloudflare':'#',
            'india':'#india',
            'google':'#google',
            'usa':'#usa',
            'russia':'#russia',
            'Australia':'#australia',
            'netherlands':'#thenetherlands',
            'canada':'#canada'
            }


        options= selenium.webdriver.ChromeOptions()   

        from typing import Tuple,List
        ips:List[Tuple[str,float,float,str]]=[]
        timeout = 16.0


        
        options.add_argument('--headless')
        # service = webdriver.ChromeService(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe")
        # driver = webdriver.Chrome(options=options,service=service)    
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(timeout)
        try:   
            pass 
            driver.get("https://www.nslookup.io/domains/github.com/dns-records/") #This is a dummy website UR
        except TimeoutException:    
            print("Page load timed out")
        try:
            pass
            # elem = WebDriverWait(driver, 8).until(                                       
            #     EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.flex-grow.bg-neutral-100 > main > div.bg-white.shadow.p-6.pb-10.rounded-t > p")) #This is a dummy element
            # )         
            #myDynamicElement = driver.find_element(
                # By.CSS_SELECTOR,
                # '#app > div.flex-grow.bg-neutral-100 > main > div.bg-white.shadow.p-6.pb-10.rounded-t > div.flex.gap-6 > div.shrink.w-full.lg\:max-w-2xl > div:nth-child(2) > table > tbody > tr.group > td.py-1 > span:nth-child(2)'
                # )
            # print(myDynamicElement.text)
        finally:
            pass
            #driver.close()

        for name in map:

            driver.get("https://www.nslookup.io/domains/github.com/dns-records/"+str(map.get(name)))

            try:
                elem = WebDriverWait(driver, timeout).until(                                       
                    EC.presence_of_element_located((By.CSS_SELECTOR, 
                    '#app > div.flex-grow.bg-neutral-100 > main > div.bg-white.shadow.p-6.pb-10.rounded-t > div.flex.gap-6 > div.shrink.w-full.lg\:max-w-2xl > div:nth-child(2) > table > tbody > tr.group > td.py-1 > span:nth-child(2)'
                                                    )) #This is a dummy element
                )         
                myDynamicElement = driver.find_element(
                    By.CSS_SELECTOR,
                    '#app > div.flex-grow.bg-neutral-100 > main > div.bg-white.shadow.p-6.pb-10.rounded-t > div.flex.gap-6 > div.shrink.w-full.lg\:max-w-2xl > div:nth-child(2) > table > tbody > tr.group > td.py-1 > span:nth-child(2)'
                    )
                ips.append([name,None,None,myDynamicElement.text])
                print(name,myDynamicElement.text)
                sleep(1)
            except TimeoutException:    
                print(f"region {name} fail!")
            finally:
                pass
        driver.quit()

        from ping3 import ping

        # Function to calculate average delay
        def get_average_delay(ip:str):
            total_delay = 0
            successful_pings = 0
            
        
            response = ping(ip, timeout=2)  # Ping each IP with a timeout of 2 seconds
            
            if response is not None:  # If the ping was successful
                total_delay += response
                successful_pings += 1
            else:
                pass
                #print(f"Failed to ping {ip}")
            
            if successful_pings > 0:
                average_delay = total_delay / successful_pings
                return average_delay
            else:
                return None




        # ping ips get avg delay
        for ip in ips:
            if ip[3] is not None:
                ip[2]=get_average_delay(ip[3])
                print(ip[0],ip[2])

        

        if len([i for i in ips if i[2] is not None]) ==0:
            raise Exception('all ip not accessable')
        min_index = min(enumerate([i for i in ips if i[2] is not None]), key=lambda x: x[1][2])[0]
        return [i for i in ips if i[2] is not None][min_index][3]

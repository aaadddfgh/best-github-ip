from .base import DNS_provider
from ping3 import ping
from typing import Dict
class dnschecker:
    def get_ip(self):
        data= self.get_all_ip()
        def get_average_delay(ip:str):
            total_delay = 0
            successful_pings = 0
            
        
            response = ping(ip, timeout=5)  # Ping each IP with a timeout of 2 seconds
            
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
        for i in data:
            item:Dict[str,str] = i
            ip_address = item.get("ip_address")
            item["avg_delay"]=get_average_delay(ip_address)
        result=[i for i in data if i.get("avg_delay") is not None]
        min_index = min(enumerate(result), key=lambda x: x[1]["avg_delay"])[0]
        return result[min_index].get("ip_address")



    def get_all_ip(self) -> list[Dict]:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        import time
        options= webdriver.ChromeOptions()   

        timeout = 16.0
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        # 初始化浏览器驱动（示例使用Chrome）
        # service = webdriver.ChromeService(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe")
        # driver = webdriver.Chrome(service=service,options=options)    

        driver.get("https://dnschecker.org/#A/github.com")  # 替换为实际网址

        # 等待页面加载
        time.sleep(5)  # 根据实际网络情况调整等待时间，建议改用显式等待（WebDriverWait）

        driver.find_element(By.ID, "s").click()

        time.sleep(5)

        data_list = []

        # 定位表格
        table = driver.find_element(By.ID, "results")

        # 获取所有行
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            # 从 tr 元素提取属性数据
            data_id = row.get_attribute("data-id")
            latitude = row.get_attribute("data-latitude")
            longitude = row.get_attribute("data-longitude")
            location = row.get_attribute("data-location")
            provider = row.get_attribute("data-provider").strip()
            
            # 从 td 元素提取其他数据
            name_td = row.find_element(By.CLASS_NAME, "name")
            
            # 提取国旗URL
            flag_url = name_td.find_element(By.TAG_NAME, "img").get_attribute("src")
            
            # 提取IP地址（需要定位到特定元素）
            ip_address = row.find_elements(By.TAG_NAME, "td")[1].text
            
            # 组织数据结构
            data_dict = {
                "location": location,
                "provider": provider,
                "ip_address": ip_address,
                "latitude": latitude,
                "longitude": longitude,
                "flag_url": flag_url,
                "data_id": data_id
            }
            
            data_list.append(data_dict)

        # 关闭浏览器
        driver.quit()
        return data_list
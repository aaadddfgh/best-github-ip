
import sys
import os

sys.path.append(os.getcwd())

from dnsProvider import dnschecker
from utils.utils import get_average_delay

temp = dnschecker.dnschecker()

data = temp.get_all_ip()

for i in data:
    assert i["ip_address"] is not None and len(str(i["ip_address"])) != 0

for i in data:
    item = i
    ip_address = item.get("ip_address")
    item["avg_delay"]=get_average_delay(ip_address)
result=[i for i in data if i.get("avg_delay") is not None]

print(result)

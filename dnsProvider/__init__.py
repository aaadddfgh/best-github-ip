
from .base import DNS_provider
from .nslookup import nslookup
def get_dns_provider(name:str=None)-> DNS_provider:
    return nslookup()
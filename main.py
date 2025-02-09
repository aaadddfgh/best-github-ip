from threading import Thread
from utils.HostsManage import HostsManager
from dnsProvider import get_dns_provider


HostsManager().remove_mappings_by_host("github.com")

dns = get_dns_provider()

HostsManager().add_mapping(dns.get_ip(),["github.com"])
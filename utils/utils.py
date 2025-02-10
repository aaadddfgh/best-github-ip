from ping3 import ping

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
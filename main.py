import requests
import json 
import logging
import argparse

URL = 'http://httpbin.org/ip'

class ProxyChecker:
    
    def __init__(self, proxt_list_path: str=None) -> None:
        self.proxy_list_path = proxt_list_path
    
    def save_proxy(self, proxy):
        with open('working_proxies.txt', 'a') as fp:
            fp.write(f'{proxy}\n')
    
    def _check_proxy(self, proxy, ip):
        return True if proxy == ip else False
    
    def check_proxy(self):
        
        if self.proxy_list_path == None:
            print("Proxy list cannot be None. Please specify the path of proxy list")
            return 
        
        try:
            with open(self.proxy_list_path, 'r') as fp:
                proxies = fp.read().split()
                
        except FileNotFoundError:
            print("Cannot find the proxy list. Please specify the correct path")
            return 

        # get through all proxies
        for proxy in proxies:
            
            _proxies =  {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}'
            }
                    
            # send the request
            response = requests.get(URL, _proxies)
            # get the response
            data = json.loads(response.text)
            ip = data['origin']
            print(f'{ip} response for {proxy} proxy')
            # check if the response matches the specified proxy
            if self._check_proxy(ip, proxy.split(':')[0]):
                # - save the proxy
                print(f"Working proxy found! - {proxy}")
                self.save_proxy(proxy)

            # save logs
            logging.basicConfig(
                    filename='logs.txt', 
                    filemode='a', 
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M%S',
                    level=logging.DEBUG)
            
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        prog='proxy_checker.py',
        description='Checks working proxies'
    )
    
    parser.add_argument('path', help='Path to proxy list')
    args = parser.parse_args()
    proxy_checker = ProxyChecker(args.path)
    proxy_checker.check_proxy()

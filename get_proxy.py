import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import json

@dataclass
class ProxiesScraper:

    def get_proxies(self):
        url = 'https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt'
        # url = 'https://github.com/TheSpeedX/PROXY-List/blob/master/socks5.txt'
        response = httpx.get(url)
        # print(response.text)
        json_data = response.json()
        formatted_json = json.dumps(json_data, indent=2)
        proxies = json_data['payload']['blob']['rawLines']

        return proxies

    def working_proxy(self, proxies):
        url = 'https://www.iherb.com/'
        proxy = []
        for i, item in enumerate(proxies):
            if i < len(proxies) and len(proxy) < 3:
                formated_proxy = {
                    "http://": f"http://{item}",
                    "https://": f"http://{item}"
                }
                headers = {
                    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
                }

                print(f'checking {formated_proxy}')
                try:
                    with httpx.Client(proxies=formated_proxy) as client:
                        response = client.get(url=url, headers=headers, timeout=3, follow_redirects=True)
                    proxy.append(item)
                    print(f'{item} selected')
                except Exception as e:
                    print(f"not working due to {e}")
                    continue
            else:
                break

        return proxy

    def run(self):
        proxies = self.get_proxies()
        selected_proxies = self.working_proxy(proxies)
        print(selected_proxies)

if __name__ == '__main__':
    s=ProxiesScraper()
    s.run()
import requests
from bs4 import BeautifulSoup
import json
import time
import csv

class ZillowScraper():
    results = []
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control':'max-age=0',
    'cookie': 'zguid=23|%24da21c159-1978-4d08-9127-393ea91450a6; zgsession=1|d2e4baad-2288-42e3-8d0b-ea785b88c6f3; _ga=GA1.2.1972454218.1653398016; _gid=GA1.2.794095907.1653398016; zjs_user_id=null; zg_anonymous_id=%226d474c0b-6b75-4def-8f7c-2abc5c3a2d08%22; zjs_anonymous_id=%22da21c159-1978-4d08-9127-393ea91450a6%22; pxcts=525c71c5-db63-11ec-bf5d-5471736c4b45; _pxvid=525c6142-db63-11ec-bf5d-5471736c4b45; _gcl_au=1.1.423879727.1653398018; KruxPixel=true; DoubleClickSession=true; __pdst=2ace2f29de9d4b32bc5c18bb852e473f; _hp2_id.1215457233=%7B%22userId%22%3A%223563158643822200%22%2C%22pageviewId%22%3A%227288494825981370%22%2C%22sessionId%22%3A%221117396064678233%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _cs_c=0; _hp2_ses_props.1215457233=%7B%22r%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22ts%22%3A1653398020517%2C%22d%22%3A%22www.zillow.com%22%2C%22h%22%3A%22%2F%22%7D; _derived_epik=dj0yJnU9LVZObTBoTWRJWWVjODFPbHh3M1dXcDlldkdURTdsbEombj1JWmxsS3JQVU9aN1dmaTUwQjlSU0F3Jm09MSZ0PUFBQUFBR0tNMmdjJnJtPTEmcnQ9QUFBQUFHS00yZ2M; _pin_unauth=dWlkPVl6bGtOVEExTmpJdE9EbGtNeTAwWW1KakxXRXdOR0l0TURnM1kyRTNaRE5sWlRVeg; _cs_id=e2cc3e15-8abc-aa9b-9bdc-981b4b201476.1653398025.1.1653398025.1653398025.1.1687562025363; _clck=xt30aw|1|f1q|0; JSESSIONID=0375CFFF4EA45F9D9DF4A73BDD662F27; _cs_s=1.5.0.1653399826300; KruxAddition=true; utag_main=v_id:0180f633a0df008c1c1242cc2cd805073001706b009dc$_sn:1$_se:1$_ss:1$_st:1653399820322$ses_id:1653398020322%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_visit:1$dc_event:1%3Bexp-session$dc_region:eu-central-1%3Bexp-session$ttd_uuid:9423f593-78c5-4d4f-8e58-7b9e1f54f5c9%3Bexp-session; _px3=aecda8f33cc9adc9b4ddacff2da04ac52f4672cea69319b492a77daf7636196d:v+JJcHNaGMw1YvMxIJMRr0gInAhBk88POT4ZxvSW4WX8OZ5HrCuE8CpbrIml4qkOUhp72FmbilqW+NdtTgweHg==:1000:F0J2T+aDPp75L+xa7S0i8v5XwI4VIrhz0EMiSdHgRNS0RDn0PstylVpzVKcIDWzY9i8f/ExPDe/0PC9RyUN+jPzjmyF7IqLXwh0Zsn774btXhJ4gXngY3ZpfJ9/U78AnYPDfCFv4J3vTbKEvCIxn51sXIVXw/1+jZLDkielgYUBtmU0S5CJvB2HLqreGhw+0zWZHR5DG3FgEjqRRW9rnLQ==; _uetsid=53d55210db6311ecb7b835deed271fa3; _uetvid=53d5b6c0db6311ec92498334856c7c02; AWSALB=Nqg7KiOMxSptoptrdy1x499EBl+IVpzHm4O9UkPC/zyN0BC/PqKZIj6riPrBWrJLrBRI8qT4k6t9gBqtWvC2bKXp6Cf8JIJ2lA+RZdYfbBxHkFisX9hMiOCAzm6p; AWSALBCORS=Nqg7KiOMxSptoptrdy1x499EBl+IVpzHm4O9UkPC/zyN0BC/PqKZIj6riPrBWrJLrBRI8qT4k6t9gBqtWvC2bKXp6Cf8JIJ2lA+RZdYfbBxHkFisX9hMiOCAzm6p; search=6|1655990271873%7Crect%3D45.3684164265581%252C-71.100851046875%252C40.095788110264685%252C-80.439229953125%26rid%3D43%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%0943%09%09%09%09%09%09; _clsk=gxo3kf|1653398273254|3|0|k.clarity.ms/collect',
    'referer': 'https://www.zillow.com/',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    }
    
    def fetch(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        
        return response

    def parse(self, response):
        content = BeautifulSoup(response, 'lxml')
        deck = content.find('ul', class_='photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution')
     

        for card in deck.contents:
            script = card.find('script', {'type': 'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])
                self.results.append({
                    'latitude': script_json['geo']['latitude'],
                    'longitude': script_json['geo']['longitude'],
                    'floorSize': script_json['floorSize']['value'],
                    'url': script_json['url'],
                    'price': card.find('div', {'class': 'list-card-price'}).text
                })
        print(self.results)
                
        


    def to_csv(self):
        with open ('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader

            for row in self.results:
                writer.writerow(row)

    def run(self):
        url = 'https://www.zillow.com/homes/for_sale/new-york_rb/'

        for page in range(1, 13):
            params = {
                'searchQueryState': '{"pagination":{"currentPage": %s},"mapBounds":{"west":-74.40093013281245,"east":-73.55498286718745,"south":40.4487909557045,"north":40.96202658306895},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":false,"filterState":{"isForSaleByAgent":{"value":false},"isNewConstruction":{"value":false},"isForSaleForeclosure":{"value":false},"isComingSoon":{"value":false},"isAuction":{"value":false}},"isListVisible":true}' %page
            }
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv()
        

    
        

if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()

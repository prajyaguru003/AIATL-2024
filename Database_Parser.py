import requests
from bs4 import BeautifulSoup
import json
import time
import csv


class Database_Parser():
    ret = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': 'zguid=24|%247c534f30-ae51-4b95-a9f1-a073ce047483; zgsession=1|605dd98c-84fc-421e-9e0c-dd4ebb41b740; _ga=GA1.2.777559362.1700269765; _gid=GA1.2.408979259.1700269765; pxcts=1e1bc4f8-85af-11ee-b1cb-404d23653c6d; _pxvid=1e1bb624-85af-11ee-b1cb-dcfd1a950357; zjs_user_id=null; zg_anonymous_id=%22a4c6b401-4329-4a0f-b722-cb43dc8f2938%22; _gcl_au=1.1.607156370.1700269766; DoubleClickSession=true; _fbp=fb.1.1700269766605.757669649; __pdst=13f35418dbcd498fb0f4db905d1e4b55; _clck=153zyri%7C2%7Cfgt%7C0%7C1417',
        'Pragma': 'no-cache',
        'Referer': 'https://www.zillow.com/utm_medium=cpc&utm_source=google&utm_content=1471764169|65545421228|kwd-570802407|655686053248|&semQue=null&gad_source=1&gclid=CjwKCAiAu9yqBhBmEiwAHTx5p1UvU4aFnneEVfEgmo0hfe9emlpdxfqx3RX4Dk0S5oSqwkpjiGaqGxoC3boQAvD_BwE',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    def get(self, url, params):
        give = requests.get(url, headers=self.headers, params=params)
        print(give.status_code)
        return give

    def parse(self, responce):
        houseData = BeautifulSoup(responce, 'lxml')
        imageList = houseData.find('ul', {'class': 'photo-cards photo-cards_wow photo-cards_short'})
        for image in imageList.contents:
            hold = image.find('script', {'type', 'application/ld+json'})
            if hold:
                holdJSON = json.loads(hold.contents[0])
                self.ret.append({
                    'Price': hold.find('div', {'class': 'list-card-price'}).text,
                    'Address': holdJSON['address']['streetAddress'],
                    'City': holdJSON['address']['addressLocality'],
                    'State': holdJSON['address']['addressRegion'],
                    'Postal': holdJSON['address']['postalCode'],
                    'Floor Size': holdJSON['floorSize']['value'],
                    'Longitude': holdJSON['geo']['longitude'],
                    'Latitude': holdJSON['geo']['latitude'],
                    'URL': holdJSON['url'],
                    'Picture': image.find('picture', {'source': 'srcset'})
                })

    def convert(self):
        with open('Open_Housing_ForSale.csv', 'w') as csv_file:
            type = csv.DictWriter(csv_file, fieldnames=self.ret[0].keys())
            type.writeheader()
            for row in self.ret:
                type.writerow(row)

    def start(self):
        page = 'https://www.zillow.com/homes/for_sale/'

        for index in range(1, 3):
            params = {
                'searchQueryState': '{"pagination":{"currentPage": %s},"mapBounds":{"west":-74.40093013281245,"east":-73.55498286718745,"south":40.4487909557045,"north":40.96202658306895},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":false,"filterState":{"isForSaleByAgent":{"value":false},"isNewConstruction":{"value":false},"isForSaleForeclosure":{"value":false},"isComingSoon":{"value":false},"isAuction":{"value":false}},"isListVisible":true}' %page
            }
            result = self.get(page, params)
            self.parse(result.text)
            time.sleep(2)
        self.convert()

if __name__ == '__main__':
    web_parser = Database_Parser()
    web_parser.start()
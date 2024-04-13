import re
import requests
from bs4 import BeautifulSoup

class Item:
    def __init__(self,code,image,title,expire) -> None:
        self.code = int(code)
        self.image = image
        self.title = title
        self.expire = expire
        self.url = f'https://www.meembom.com/giveaways/{code}'

class Meembom:
    def login(self,instaid,email):
        self.email = email
        self.api_url = 'https://www.meembom.com/api/createGiveawayItem/?email_id={email}&insta_id={instaid}&insta_code={code}&giveaway_id={id}&csrfmiddlewaretoken={token}'
        self.instaid = instaid
    def get_page(self,id):
        response = requests.get(f'https://www.meembom.com/giveaways/{id}')
        csrftoken = response.cookies['csrftoken']
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('body')
        script = body.find('script')
        giveaway_code = re.search(r'var giveawayCode = "(.*?)";', script.string).group(1)
        csrfmiddlewaretoken = re.search(r'csrfmiddlewaretoken: "(.*?)"', script.string).group(1)
        giveaway_id = re.search(r'giveaway_id: "(.*?)"', script.string).group(1)
        self.csrftoken = csrftoken
        self.giveaway_code = giveaway_code
        self.csrfmiddlewaretoken = csrfmiddlewaretoken
        self.giveaway_id = giveaway_id
        self.url = f'https://www.meembom.com/giveaways/{id}'
    def send_api(self):
        url = self.api_url.format(email=self.email,instaid=self.instaid,code=self.giveaway_code,id=self.giveaway_id,token=self.csrfmiddlewaretoken)
        headers = {
            'Host': 'www.meembom.com',
            'Sec-Ch-Ua': '"Chromium";v="121", "Not A(Brand";v="99"',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': self.url,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Priority': 'u=1, i'
        }
        cookies = {
            'csrftoken': self.csrftoken
        }
        response = requests.get(url, headers=headers, cookies=cookies)
        return response.text
    def get_last(self):
        response = requests.get('https://www.meembom.com/giveaways')
        soup = BeautifulSoup(response.text,'html.parser')
        div = soup.find_all('div',{'class':'col-12 col-lg-4 mt-4'})[-1]
        code = div.find('a').get('href').split('/')[-2]
        image = div.find('img',{'class':'banner-img'}).get('src')
        h3s = div.find('div',{'class':'pl-2'}).find_all('h3')
        title = h3s[1].text
        expire = h3s[0].text
        return Item(code,image,title,expire)
    def get_all(self):
        response = requests.get('https://www.meembom.com/giveaways')
        soup = BeautifulSoup(response.text,'html.parser')
        divs = soup.find_all('div',{'class':'col-12 col-lg-4 mt-4'})
        data = []
        for div in divs:
            code = div.find('a').get('href').split('/')[-2]
            image = div.find('img',{'class':'banner-img'}).get('src')
            h3s = div.find('div',{'class':'pl-2'}).find_all('h3')
            title = h3s[1].text
            expire = h3s[0].text
            data.append(Item(code,image,title,expire))
        return data
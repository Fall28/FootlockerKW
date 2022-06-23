import email
from email.mime import image
import json
from bs4 import BeautifulSoup
import requests
import time
from dhooks import Webhook,File,Embed
import datetime as rawr





def login(user,password):
    FL=requests.session()
    
    Payload={'name': user,
            'pass' : password, 
            'form_build_id': 'form-2DtEyRuGlZMGewjq5ykhTK6-09NiId72r88x62wDEqM',
            'form_id': 'user_login_form',
            'op': 'sign in'}

    loginPost=FL.post('https://www.footlocker.com.kw/en/user/login',data=Payload)
    loginSoup=BeautifulSoup(loginPost.text,'lxml')
    usernum=str(loginSoup.find_all('a')[3]).split('/')[7].split('"')[0]


    UserPage=FL.get(f'https://www.footlocker.com.kw/en/user/{usernum}')
    userSoup=BeautifulSoup(UserPage.text,'lxml')
    token=str(userSoup.find('script',type="application/json")).split('Token":')[1].split('"')[1]
    print(f'TOKEN:[{token}]')  
    
    FL.headers.update({
        'authorization':f'Bearer {token}',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        

    })
    

    # with open ('./log', 'w', encoding='utf-8') as f:
    #         f.write(loginPost.text)
    if "My Account" in loginPost.text:
            print (f'Login Success[{user}]')

    return FL



class footLockerKW:
    def __init__(self,url,taskNO,session,email,discordurl):
        self.session=session
        self.url=url
        self.taskNO=taskNO
        self.email=email
        self.hook=discordurl
        self.sku=""
        self.qouteid=""
        self.name=""
        self.imageurl=""
        self.checkout=""

    def send(self):
            embed = {
                "avatar_url": "https://seeklogo.com/images/F/Foot_Locker-logo-5615BC5594-seeklogo.com.png",
                'embeds': [{
                    "title": f"{self.email}",
                    'color':'16734349',
                    # "image": {
                    # "url": self.imageurl
                    # },
                    "fields": [
                    {"name": f"{self.name} added to cart", "value": f'SKU: {self.sku}', "inline": False},
                    
                    ],
                    'timestamp': str(rawr.datetime.utcfromtimestamp(time.time())),
                    'footer': {
                        "text": 'added',
                        "icon_url": 'https://seeklogo.com/images/F/Foot_Locker-logo-5615BC5594-seeklogo.com.png',
                    },
                }]
            }
            r = requests.post(self.hook, json=embed)

    def log(self, status):
        print(f"<{self.email}>[Task:{self.taskNO}] {status}")

    def monitor(self):
        ProductPage=self.session.get(self.url).text
        
        while "Page not found" in ProductPage:
            ProductPage=self.session.get(self.url).text
            self.log("Product not available")
            time.sleep(5)
        
        if self.atc()=="200":
            self.send()
            self.log("Item succesfully added to cart")
            print(self.session.get("https://www.footlocker.com.kw/en/checkout").url)
            
            




    def atc(self):
        
        
        while self.sku=="":
            try:
                ProductPage=self.session.get(self.url).text
                ProductPageSoup = BeautifulSoup(ProductPage , 'lxml')
                self.sku = ProductPageSoup.find(id="pdp-layout")['data-sku']
                self.name =str(ProductPageSoup.find_all('script', type="application/ld+json")[1]).split(',')[5].split(":")[1]
                self.imageurl=str(ProductPageSoup.find_all('script', type="application/ld+json")[1]).split(',')[6].split('"image": ')[1]
                

            except:
                pass
        while self.qouteid=="":
            try:
                cartPage=self.session.get('https://www.footlocker.com.kw/rest/kwt_en/V1/carts/mine/getCart')
                cartSoup=BeautifulSoup(cartPage.text,'lxml')
                self.qouteid=str(cartSoup.find('p')).split('"id"')[1].split(':')[1].split(',')[0]
            except:
                pass

        self.log('QuoteID:[{self.qouteid}]')
        self.log(f'SKU: [{self.sku}]')
        #print(FL.headers)

        with open ('./log', 'w', encoding='utf-8') as f:
            f.write(ProductPage)

        Payload={
            "cartItem":{
                "sku":self.sku,"qty":"1","product_option":{
                    "extension_attributes":{
                        "configurable_item_options":[
                            {
                                "option_id":"625","option_value":1663
                                }
                                ]
                                }
                                },"quote_id":self.qouteid
                                }
                                }

        

        productPost=self.session.post('https://www.footlocker.com.kw/rest/kwt_en/V1/carts/mine/items', json=Payload,headers=self.session.headers)
        
        if str(productPost.status_code)!="200":
            option_values=[1624,1630,1666,1669,1675]
            
            for x in range(len(option_values)):
                Payload={
            "cartItem":{
                "sku":self.sku,"qty":"1","product_option":{
                    "extension_attributes":{
                        "configurable_item_options":[
                            {
                                "option_id":"625","option_value":option_values[x]
                                }
                                ]
                                }
                                },"quote_id":self.qouteid
                                }
                                }
                
                if str(productPost.status_code)!="200":
                    self.log('Checking another size')
                    productPost=self.session.post('https://www.footlocker.com.kw/rest/kwt_en/V1/carts/mine/items', json=Payload,headers=self.session.headers)
                    time.sleep(5)
                else:
                    break
        
        return str(productPost.status_code)

        
#l=login('spam.hussein2@gmail.com','Man@kaka52')
#footLockerKW('https://www.footlocker.com.kw/en/buy-jordan-retro-4-mens-shoes-white-black.html','x',login('husseinalanjawi@gmail.com','Man@kaka52')).monitor()
#footLockerKW('https://www.footlocker.com.kw/en/buy-jordan-retro-4-mens-shoes-white-black.html','x',l,"husseinalanjawi@gmail.com","https://discord.com/api/webhooks/989341736843214858/8BJJOhaUF4DDkA-B3C4pnEoshtI5Nn02xcz-w3c60esf_zHZCiAQioH7vlvY8R1MqmPS").monitor()
#footLockerKW('https://www.footlocker.com.kw/en/buy-air-jordan-1-retro-high-og-mens-shoes-white-red.html','x',l).monitor()



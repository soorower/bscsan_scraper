import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}

links = []
values = []
tokens = []
lists = []
data = {}
pages = int(input('How many pages, you want to scrape: '))
output_name = input('Output file name: ')
print('Output File Type')
print('1. Excel')
print('2. CSV')
check = int(input('Enter choice: '))

for i in range(1,pages+1):
    print(f'Scraping Page: {i}')
    r = requests.get(f'https://bscscan.com/tokentxns?p={i}',headers = headers)
    soup = bs(r.content,'html.parser')

    table_trs = soup.find('table',attrs = {'class':'table table-hover'}).find('tbody').findAll('tr')



    for table in table_trs:
        token = table.findAll('td')[-1].text.strip()
        value = table.findAll('td')[-2].text
        link = "https://bscscan.com/" + table.findAll('td')[-1].find('a')['href']
        
        tokens.append(token)
        values.append(value)
        links.append(link)


for lin, tok, val in zip(links,tokens,values):
    print(f'Scraping total Supply of token: {tok}')
    r = requests.get(lin,headers = headers)
    soup = bs(r.content,'html.parser')
    total_supply = soup.find('div',attrs = {'class':'col-md-8 font-weight-medium'}).text
    toke = lin.split('/')[-1]

    address_url = f'https://bscscan.com/token/generic-tokenholders2?m=normal&a={toke}&p=1'
    r = requests.get(address_url,headers = headers)
    soup = bs(r.content,'html.parser')
    address = soup.find('table').find('tbody').find('tr').findAll('td')[1].text
    data = {
        'Token': tok,
        'Value': val,
        'Total Supply': total_supply,
        'Address': address
    }
    lists.append(data)

if check == 1:
    df = pd.DataFrame(lists)
    df.to_excel(f'{output_name}.xlsx',encoding='utf-8', index=False)
    print('Done!')
else:
    df = pd.DataFrame(lists)
    df.to_csv(f'{output_name}.csv',encoding='utf-8', index=False)
    print('Done!')
    
    
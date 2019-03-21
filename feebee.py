import requests, json, jsonparser, re
from lxml import etree


def web_to_json(message):
    item = message.split('!比價')
    print('item', item[1])
    if ' ' in item[1]:
        obj = item.split(' ')
        r_url = 'https://feebee.com.tw/s/?q='
        for obj_1 in obj:
            r_url += obj_1
    else:
        r_url = 'https://feebee.com.tw/s/?q=' + item[1]
    print('r_url', r_url)
    r = requests.get(r_url)
    r_1 = etree.HTML(r.text)
    name = r_1.xpath('//li[starts-with(@class, "pure-g")]')
    t = r_1.xpath("//span[starts-with(@class,'price ellipsis xlarge')]|//li[starts-with(@class,'price ellipsis xlarge')]")
    price = ''
    name_l = list()
    price_l = list()
    url_l = list()
    if len(t) == 0:
        return 'no such thing'
    for cnt in range(len(t)-1):
        """
        name_2 = name[cnt].xpath('span')
        name_3 = name_2[0].xpath('a')
        name_4 = name_3[0].attrib['title']
        """
        name_1 = t[cnt].getparent() # -> 找到父標籤
        name_1 = name_1.getparent()
        if cnt == 0 :
            name_1 = name_1.getparent()
            print(name_1)
        name_1 = name_1.xpath('a')
        if len(name_1) < 1:
            return 'no such thing'
        url = name_1[0].attrib['href']
        url_s = get_shorten(url)
        url_l.append(url_s)
        name_1 = name_1[0].xpath('string(.)')
        name_1 = name_1.replace('\n', '')
        name_1 = name_1.replace(' ', '')
        name_1 = name_1.replace('價格', '')
        if name_1 != None:
            name_l.append(name_1)
        try:
            price = t[cnt].xpath('string(.)')
            price = price.replace('\n', '')
            price = price.replace(' ', '')
            price = price.replace('價格', '')
            price_l.append(price)
        except:
            print('')
    reply = ''
    if len(price_l) >= 4:
        for cnt in range(4):
            reply += name_l[cnt] + ' $' +  price_l[cnt] + '\n' + url_l[cnt] + '\n'
    else:
        for cnt in range(len(price_l)):
            reply += name_l[cnt] + ' $' +  price_l[cnt] + '\n' + url_l[cnt] + '\n'
    print(reply)
    return reply
  
def get_shorten(url):
    print('url', url)
    r = requests.post('https://api.pics.ee/v1/links/?access_token=20f07f91f3303b2f66ab6f61698d977d69b83d64', data = {'url':str(url)})
    r_1 = json.loads(r.content)
    print(r_1["data"]["picseeUrl"])
    return r_1["data"]["picseeUrl"]
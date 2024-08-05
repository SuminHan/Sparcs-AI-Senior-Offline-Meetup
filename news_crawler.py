import os
import sys
import urllib.request
import datetime
import time
import json

client_id = '###'
client_secret = '###'

YMDH_FORMAT = '%Y%m' #'%Y%m%d%H'


#[CODE 1]
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s]Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e :
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE 2]
def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&sort=date&start=%s&display=%s" % (urllib.parse.quote(srcText), start, display)

    url = base + node + parameters
    print(url)
    responseDecode = getRequestUrl(url)     #[CODE 1]

    if(responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

#[CODE 3]
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    #pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d, %b, %Y, %H:%M:%S+0900')
    #pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')
    pDate = post['pubDate']

    jsonResult.append({'cnt':cnt, 'title':title, 'description':description,
                       'org_link':org_link, 'link':org_link, 'pDate':pDate})
    return

#[CODE 0]
def crawl(srcText):
    nowhour = datetime.datetime.now().strftime(YMDH_FORMAT)
    filename = f'naver_news/{srcText}_{nowhour}.json'

    if os.path.isfile(filename):
        with open(f'naver_news/{srcText}_{nowhour}.json') as fp:
            json_data = json.load(fp)
        return json_data
    else:
        node = 'news'  #크롤링한 대상
        # srcText = input('검색어를 입력하세요: ')
        cnt = 0
        jsonResult = []
        
        jsonResponse = getNaverSearch(node, srcText, 1, 100)  #[CODE 2]
        total = jsonResponse['total']
        
        while((jsonResponse != None) and (jsonResponse['display'] != 0)):
            for post in jsonResponse['items']:
                cnt+= 1
                getPostData(post, jsonResult, cnt)   #[CODE 3]
                
            start = jsonResponse['start'] + jsonResponse['display']
            jsonResponse = getNaverSearch(node, srcText, start, 100)   #[CODE 2]
            if cnt > 200:
                break
            
        print('전체 검색 : %d 건' %total)
            
        with open(f'naver_news/{srcText}_{nowhour}.json', 'w', encoding='utf8') as outfile:
            jsonFile = json.dumps(jsonResult, indent=4, sort_keys = True, ensure_ascii = False)
            outfile.write(jsonFile)
                
        print("가져온 데이터 : %d 건" %(cnt))

        return jsonFile



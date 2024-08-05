# -*- coding: utf-8 -*-

import base64
import json
import http.client
import datetime
import requests

import news_crawler

YMDH_FORMAT = '%Y%m' #'%Y%m%d%H'


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/api-tools/summarization/v2/###', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        if res['status']['code'] == '20000':
            return res['result']['text']
        else:
            return 'Error'

def clova_summarize(srcText, latest=30):
    nowhour = datetime.datetime.now().strftime(YMDH_FORMAT)
    filename = f'naver_news_summary/{srcText}_{nowhour}.txt'
    if os.path.isfile(filename):
        with open(filename) as fp:
            response_text = fp.read()
        return response_text
    else:
        json_data = news_crawler.crawl(srcText)
        latest_text = ''
        count = 0
        for data in json_data:
            try:
                if srcText not in data['title']:
                    continue
                latest_text += data['description'] + '\n\n'
            except:
                pass
            count += 1
            if count > latest:
                break

        completion_executor = CompletionExecutor(
            host='clovastudio.apigw.ntruss.com',
            api_key='###'
            api_key_primary_val = '###'
            request_id='###'
        )

        rdata = {
        "texts" : [ latest_text ],
        "segMinSize" : 300,
        "includeAiFilters" : True,
        "autoSentenceSplitter" : True,
        "segCount" : -1,
        "segMaxSize" : 1000
        }
        request_data = json.loads(json.dumps(rdata), strict=False)

        response_text = completion_executor.execute(request_data)
        #print(request_data)
        if response_text != 'Error':
            print(response_text)
            with open(filename, 'w') as fp:
                fp.write(response_text)
        else:
            print('ERROR:', response_text)
        return response_text



import os
def clova_summarize_aegyo(srcText, username, latest=100):
    nowhour = datetime.datetime.now().strftime(YMDH_FORMAT)
    filename = f'naver_news_summary_aegyo/{srcText}_{username}_{nowhour}.txt'
    if os.path.isfile(filename):
        with open(filename) as fp:
            response_text = fp.read()
        return response_text
    else:
        response_text = clova_summarize(srcText, latest=latest)
        response_text = '- '.join([sent for sent in response_text.split('-') if srcText in sent][:10])
        ask_clova_text = response_text + f""" 위 내용은 {srcText}에 관한 최신 뉴스야. 
    이 내용중 일부를 요약해서 '{srcText}'이 '{username}' 에게 애교를 섞어 말하듯이 '{srcText}'의 평소 말투로 1분가량 분량으로 얘기해줘. 이야기 시작전 {srcText}보다 나이가 많은 '{username}'의 이름을 부르면서 인사해줘."""

        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': '###'
            'X-NCP-APIGW-API-KEY': '###'
            'X-NCP-CLOVASTUDIO-REQUEST-ID': '###'
            'Content-Type': 'application/json',
        #     'Accept': 'text/event-stream',
        }

        json_data = {
            'topK': 0,
            'includeAiFilters': True,
            'maxTokens': 256,
            'temperature': 0.2,
            'messages': [
                {
                    'role': 'system',
                    'content': f'너는 가수 {srcText}이고 너의 팬인 {username}에게 너의 평소 말투와 애교를 섞어 말할거야',
                },
                {
                    'role': 'user',
                    'content': ask_clova_text,
                },
        #         {
        #             'role': 'assistant',
        #             'content': '알겠습니다. 무엇을 테스트해볼까요?',
        #         },
            ],
            'stopBefore': [],
            'repeatPenalty': 5.0,
            'topP': 0.8,
        }

        response = requests.post(
            'https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003',
            headers=headers,
            json=json_data,
        )

        response_text = response.json()['result']['message']['content']
        #print(request_data)
        print(response_text)
        with open(filename, 'w') as fp:
            fp.write(response_text)
        return response_text

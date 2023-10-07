import requests

cookies = {
    '_jl_uid': 'vETZ4WUILvEgftokBER4Ag==',
    '_gcl_au': '1.1.1801966748.1695035050',
    'referrer': 'https://client.work-zilla.com/',
    '_ym_uid': '1695035051576708091',
    '_ym_d': '1695035051',
    'tmr_lvid': '79a9abd783270f5e68cbc6f0ba57bfa2',
    'tmr_lvidTS': '1695035055405',
    '_tt_enable_cookie': '1',
    '_ttp': 'rALbsDXw_v8KYn8xszNzyrPqCrx',
    '_gid': 'GA1.2.367854592.1696489017',
    'csrftoken': 'KHWlZUY6eRMNeMoHIazJyoOlj9yyy6nM',
    'sessionid': 'l7u2s28gwebixr2jfejzs3qqsbqpxqz9',
    'jl_features': 'headerFeatures%3Dheader_1_counter%3BfeedbacksFeature%3Ddefault%3BpopUpInvestorFeature%3Ddefault',
    '_ym_isad': '1',
    '_clck': 'flvtcj|2|ffn|0|1373',
    'tmr_detect': '1%7C1696650802576',
    '_clsk': 'kwsvui|1696650815907|3|1|v.clarity.ms/collect',
    '_ga_NR0DV46HQK': 'GS1.1.1696650787.9.1.1696651215.60.0.0',
    '_ga': 'GA1.2.97225234.1695035049',
    '_gat': '1',
}

headers = {
    'authority': 'jetlend.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json;charset=utf-8',
    # 'cookie': '_jl_uid=vETZ4WUILvEgftokBER4Ag==; _gcl_au=1.1.1801966748.1695035050; referrer=https://client.work-zilla.com/; _ym_uid=1695035051576708091; _ym_d=1695035051; tmr_lvid=79a9abd783270f5e68cbc6f0ba57bfa2; tmr_lvidTS=1695035055405; _tt_enable_cookie=1; _ttp=rALbsDXw_v8KYn8xszNzyrPqCrx; _gid=GA1.2.367854592.1696489017; csrftoken=KHWlZUY6eRMNeMoHIazJyoOlj9yyy6nM; sessionid=l7u2s28gwebixr2jfejzs3qqsbqpxqz9; jl_features=headerFeatures%3Dheader_1_counter%3BfeedbacksFeature%3Ddefault%3BpopUpInvestorFeature%3Ddefault; _ym_isad=1; _clck=flvtcj|2|ffn|0|1373; tmr_detect=1%7C1696650802576; _clsk=kwsvui|1696650815907|3|1|v.clarity.ms/collect; _ga_NR0DV46HQK=GS1.1.1696650787.9.1.1696651215.60.0.0; _ga=GA1.2.97225234.1695035049; _gat=1',
    'referer': 'https://jetlend.ru/invest/v3/market',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
}

params = {
    'limit': '100000',
    'offset': '0',
    'sort_dir': 'desc',
    'sort_field': 'ytm',
}

response = requests.get('https://jetlend.ru/invest/api/exchange/loans', params=params, cookies=cookies, headers=headers).json()

for num in response['data']:
    print(num['loan_id'])
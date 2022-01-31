import requests
import json

kakao_url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '948e978ef57e71c189ebedce930f6256'
redirect_uri = 'https://www.naver.com'
authorize_code = 'P3IIsfUj6tH_UfFWebGZ1RXG7weYCuCS-h_xrIT_qhCso-OKKttPx4NL9qhJIg7x5oiDTwo9dZwAAAF-rkR9GA'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
}


def set_token():
    response = requests.post(kakao_url, data=data)
    tokens = response.json()
    with open('kakao_code.json', 'w') as fp:
        json.dump(tokens, fp)
    
def get_token():
    with open('kakao_code.json', 'r') as fp:
        tokens = json.load(fp)
    
    return tokens

def send_kakao():
    tokens = get_token()
    
    headers={
        "Authorization" : "Bearer " + tokens["access_token"]
    }
    
    data={
        "template_object": json.dumps({
            "object_type": "text",
            "text": "안녕? 나는 잉빈이야",
            "link": {
                "web_url" : "헤헤. text와 link 객체는 필수로 넣어야 하는 거구나? button_title과 buttons는 안 넣어도 상관 없지만 말이야!",
                "mobile_web_url" : "헤헤. text와 link 객체는 필수로 넣어야 하는 거구나? button_title과 buttons는 안 넣어도 상관 없지만 말이야!"
            },
            "button_title" : "헤헤"   
        })
    }
    response = requests.post(kakao_me_url, headers=headers, data=data)
    response.status_code
import base64
import hashlib
import hmac
import urllib2

import simplejson as json

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "=" * padding_factor 
    return base64.urlsafe_b64decode(str(inp))

def parse_signed_request(cookie, appid, secret):
    encoded_sig, payload = cookie['fbsr_' + appid].split('.', 2) 
    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        raise Exception('Unknown algorithm')
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    
    req = urllib2.Request(
        'https://graph.facebook.com/oauth/access_token?client_id=' + appid + '&redirect_uri=&client_secret=' + secret + '&code=' + data['code'], 
        None, 
        {'user-agent':'syncstream/vimeo'}
    )
    opener = urllib2.build_opener()
    f = opener.open(req)
    access_data = f.read()
    parsed_access_data = dict([x.split('=') for x in access_data.split('&')])
    for key in parsed_access_data:
        data[key] = parsed_access_data[key]

    return data

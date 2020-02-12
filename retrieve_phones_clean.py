import base64, email, hmac, hashlib, urllib, requests, pprint, json

def sign(method, host, path, params, skey, ikey):
    """
    Return HTTP Basic Authentication ("Authorization" and "Date") headers.
    method, host, path: strings from request
    params: dict of request parameters
    skey: secret key
    ikey: integration key
    """

    # create canonical string
    now = email.Utils.formatdate()
    canon = [now, method.upper(), host.lower(), path]
    args = []
    for key in sorted(params.keys()):
        val = params[key]
        if isinstance(val, unicode):
            val = val.encode("utf-8")
        args.append(
            '%s=%s' % (urllib.quote(key, '~'), urllib.quote(val, '~')))
    canon.append('&'.join(args))
    canon = '\n'.join(canon)

    # sign canonical string
    sig = hmac.new(skey, canon, hashlib.sha1)
    auth = '%s:%s' % (ikey, sig.hexdigest())

    # return headers
    return {'Date': now, 'Authorization': 'Basic %s' % base64.b64encode(auth)}

ikey = ''
skey = ''
api_host = ''
params = {}

# Retrieve Phones
p_phones = sign('GET', api_host, '/admin/v1/phones', params, skey, ikey)
r_phones = requests.get(('https://' + api_host + '/admin/v1/phones'), headers={'username': ikey, 'Authorization': p_phones["Authorization"], 'date': p_phones["Date"]}, params=params)
phones = r_phones.json()
# print(json.dumps(phones, indent=4))

for phone in phones['response']:
    if phone['number'] == "":
        print("NULL. " + "Activated? " + str(phone['activated']))
    elif phone['number'] != "":
        print(str(phone['number']) + " Activated? " + str(phone['activated']))
    else:
        print("No phone found.")











with open("token.txt", "r") as f:
    tinder_token = f.read()
    f.close()

headers = {
    'app_version': '11.4.0',
    'platform': 'ios',
    'content-type': 'application/json',
    'User-agent': 'Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)',
    'X-Auth-Token': tinder_token
}

host = 'https://api.gotinder.com'

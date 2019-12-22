from configparser import ConfigParser

config= ConfigParser()
config['leetcode'] = {
'language':"python",
'overwrite': True,
'cookies' : [{'domain': 'leetcode.com', 'httpOnly': False, 'name': 'csrftoken', 'path': '/', 'secure': True, 'value': 'AVSAV'}, {'domain': '.leetcode.com',  'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.289916893.1577009081'}, {'domain': '.leetcode.com', 'httpOnly': True, 'name': 'LEETCODE_SESSION', 'path': '/', 'secure': True, 'value': 'AVAV'}, {'domain': '.leetcode.com',  'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'ASDASD'}, {'domain': '.leetcode.com',  'httpOnly': False, 'name': '_gat', 'path': '/', 'secure': False, 'value': 'CDE'}, {'domain': '.leetcode.com', 'httpOnly': True, 'name': '__cfduid', 'path': '/', 'secure': False, 'value': 'ABC'}],
'list_names': ['top-amazon-questions', 'top-google-questions', 'top-interview-questions', 'top-linkedin-questions', 'top-100-liked-questions',"top-facebook-questions"]
}

config['mail'] = {
    'key': 'aasd@gmail.com',
    'password':'ABC',
    'people_to_send_email_to': ["abc@gmail.com", "dbdbdb@gmail.com"]
}

with open('./dev.ini.example', 'w') as f:
    config.write(f)

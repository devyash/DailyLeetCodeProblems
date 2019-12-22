import requests
import pprint
from selenium import webdriver
from time import sleep
import os
import json
from configparser import ConfigParser
import ast
parser= ConfigParser()
parser.read('./../dev.ini')

list_names=json.loads(parser.get('leetcode', 'list_names'))
all_questions = []

language=parser.get('leetcode', 'language')
overwrite=parser.getboolean('leetcode', 'overwrite')
#put the appropriate value here was not able to get it from parser
cookies = [{'domain': 'leetcode.com', 'httpOnly': False, 'name': 'csrftoken', 'path': '/', 'secure': True, 'value': 'AVSAV'}, {'domain': '.leetcode.com', 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.289916893.1577009081'}, {'domain': '.leetcode.com', 'httpOnly': True, 'name': 'LEETCODE_SESSION', 'path': '/', 'secure': True, 'value': 'AVAV'}, {'domain': '.leetcode.com', 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'ASDASD'}, {'domain': '.leetcode.com', 'httpOnly': False, 'name': '_gat', 'path': '/', 'secure': False, 'value': 'CDE'}, {'domain': '.leetcode.com', 'httpOnly': True, 'name': '__cfduid', 'path': '/', 'secure': False, 'value': 'ABC'}]


#cookies
new_cookies={}
for cookie in cookies:
    if 'expiry' in cookie:
       del cookie['expiry']
new_cookies['path'] = '/'
new_cookies['domain'] = '.leetcode.com'
for cookie in cookies:
    new_cookies[cookie['name']] = cookie['value']

def get_question_data(question_title):
    data = {"operationName": "questionData", "variables": {"titleSlug": question_title},
            "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
    r = requests.post('https://leetcode.com/graphql', cookies=new_cookies, json=data).json()
    data = r['data']['question']
    return data


# initialise browser
browser = webdriver.Chrome(os.getcwd()+'\chromedriver')
# login
browser.get('https://leetcode.com/accounts/login/')
# wait page to load
sleep(3)

# user_name=browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div/div/div/form/span[1]/input')
# password=browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/form/span[2]/input")
# user_name.send_keys("USERNAME")
# sleep(3)
# password.send_keys("PASSWORD")
# sleep(2)
#manually sign in after this step putting a break point here
#browser.get_cookies()
#use this cookies to update the settings file (will need to remove the expire attribute)


for cookie in cookies:
    browser.add_cookie(cookie)

for list_name in list_names:
    all_questions = []
    if overwrite:
        with open(list_name + ".json", mode='w', encoding='utf-8') as f:
            json.dump([], f)
    data=browser.get(f"https://leetcode.com/api/problems/favorite_lists/{list_name}/")
    td=browser.find_element_by_tag_name("body").text
    tq=json.loads(td)['stat_status_pairs']
    result=[]
    for q in tq:
        rq={}
        rq['article']=q['stat']["question__article__slug"]
        rq["title"]=q['stat']['question__title_slug']
        rq['difficulty']=q['difficulty']['level']
        rq['frequency']=q['frequency']
        result.append(rq)
    question_details={}
    for q in result:
        try:
            question_details = {}
            question_title=q['title']
            details=get_question_data(question_title)
            question_details['title']=q['title']
            question_details['difficulty']=q['difficulty']
            question_details['article'] = q['article']
            question_details['frequency'] = q['frequency']
            question_details['details'] = details
            question_details["discussion_url"] = f"https://leetcode.com/problems/{q['title']}/discuss/?currentPage=1&orderBy=most_votes&query={language}"
            question_details["article_url"] = f"https://leetcode.com/articles/{q['article']}/"
            question_details["youtube_url"] = f"https://www.youtube.com/results?search_query={q['title']}"
            all_questions.append(question_details)
        except Exception as e:
            print(q['title'] + f":{str(e)}")

    with open(list_name + ".json", mode='w', encoding='utf-8') as questions_json:
        json.dump(all_questions, questions_json, indent=4)

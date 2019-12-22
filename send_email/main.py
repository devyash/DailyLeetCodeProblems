import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configparser import ConfigParser
import ast
parser= ConfigParser()
parser.read('./../dev.ini')

folder_path=os.path.join(os.getcwd(),"..","parsed_questions_list")
files=os.listdir(folder_path)
next_question = {}
last_email=None
TEMP_LOCATION=os.path.join(os.getcwd(), "temp.json")
file_name=""

key= parser.get('mail', 'key')
password= parser.get('mail', 'password')
#read the list of people to send the email to
people_to_send_email_to = json.loads(parser.get('mail', 'people_to_send_email_to'))

try:
    with open(TEMP_LOCATION, mode='r', encoding='utf-8') as f:
        last_email=f.read()
except FileNotFoundError:
    pass
last_email = "0,0" if last_email == None else last_email
last_file= int(last_email.split(',')[0])
last_question= int(last_email.split(',')[1])

with open(os.path.join(folder_path, files[last_file]), mode='r', encoding='utf-8') as questions_json:
    questions=json.load(questions_json)
    if last_question >= len(questions):
        last_file=last_file+1
        last_question=0
        with open(os.path.join(folder_path, files[last_file] ), mode='r', encoding='utf-8') as questions_json:
            questions=json.load(questions_json.read())
            next_question=questions[last_question]
    else:
        next_question = questions[last_question + 1]
        last_question+=1
    file_name=files[last_file]

with open(TEMP_LOCATION, mode='w', encoding='utf-8') as f:
    f.write(f"{str(last_file)},{str(last_question)}")
# print(file_name[:-5])
# print(next_question)

difficulty=next_question['details']['difficulty']
stats= json.loads(next_question['details']['stats'])
ac_rate= stats['acRate'] if "acRate" in stats.keys() else ''
likes = next_question['details']['likes'] if 'likes' in next_question['details'] else ''
dislikes = next_question['details']['dislikes'] if 'dislikes' in next_question['details'] else ''
similar=""
if 'similarQuestions' in next_question['details']:
    similarqs=json.loads(next_question['details']['similarQuestions'])
    for q in similarqs:
        similar+= f"{q['title']}, "
similar=similar[:-2]

topics=""
if 'topicTags' in  next_question['details']:
    topicsqs= next_question['details']['topicTags']
    for topic in topicsqs:
        topics += f"{topic['name']}, "
topics=topics[:-2]

frequency = str(int(next_question['frequency'])/5 * 100)

article_url = "" if 'None' in next_question['article_url'] else f"{next_question['article_url']} "
hints=""
if "hints" in next_question['details']:
    for hint in next_question['details']['hints']:
        hints+=f"""
            <tr>
            <td>{str(hint)}&nbsp;</td>
            </tr>
            """
hints_table=""
if hints != "":
    hints_table=f"""
    <h2 style="color: #2e6c80;">Hints:</h2>
<p>&nbsp;</p>
<table class="editorDemoTable">
<thead>
<tr>
<td>Hints</td>
</tr>
</thead>
<tbody>
{hints}
</tbody>
</table>"""
# get the content and clean it up and be short
content_text=f"""
List: {file_name[:-5]}
Question {last_question}
Title: {next_question["details"]["title"]}
Difficulty: {difficulty}
Frequency: {frequency} %
Content: {next_question["details"]["content"]}
{article_url}
Discussion Link: {next_question['discussion_url']}
Youtube Link: {next_question['youtube_url']}
acceptance rate: {ac_rate}
similar questions: {similar}
likes: {likes}
dislikes : {dislikes}
topics: {topics}
"""
content_html=f'''
<h1 style="color: #5e9ca0;">Daily LeetCode Problem</h1>
<h2 style="color: #2e6c80;"> #{next_question["details"]["title"]}</h2>
<p>&nbsp;</p>
{next_question["details"]["content"]}
<p><a class="btn" href="{next_question['youtube_url']}"><button style="background-color: #2b2301; color: #fff; display: inline-block; padding: 3px 10px; font-weight: bold; border-radius: 5px;">Youtube </button> </a>
<a class="btn" href="{next_question['discussion_url']}"><button style="background-color: #2b2301; color: #fff; display: inline-block; padding: 3px 10px; font-weight: bold; border-radius: 5px;" >Discussion </button></a>
<a class="btn" href="{article_url}"><button style="background-color: #2b2301; color: #fff; display: inline-block; padding: 3px 10px; font-weight: bold; border-radius: 5px;">Article</button></a></p>
<h2 style="color: #2e6c80;">Facts:</h2>
<ol style="list-style: none; font-size: 14px; line-height: 32px; font-weight: bold;">
<li style="clear: both;"><img style="float: left;" />Frequency: {frequency}%&nbsp;&nbsp;</li>
<li style="clear: both;"><img style="float: left;" />Difficulty: {difficulty}&nbsp;&nbsp;</li>
<li style="clear: both;"><img style="float: left;" />Acceptance rate: {ac_rate}&nbsp;&nbsp;</li>
<li style="clear: both;"><img style="float: left;" />Similar questions: {similar}&nbsp;&nbsp;</li>
<li style="clear: both;"><img style="float: left;" />Likes: {likes} &nbsp;&nbsp;</li>
<li style="clear: both;"><img style="float: left;" />Dislikes : {dislikes}&nbsp;&nbsp;</li>
<li style="clear: both;"><img style="float: left;" />Topics : {topics}&nbsp;&nbsp;</li>
<li style="clear: both;"><img style="float: left;" />List:  {file_name[:-5]} number #{last_question} &nbsp;&nbsp;</li>
<li style="clear: both;"><img style="float: left;" />&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</li>
</ol>
{hints_table}
<p><strong>&nbsp;</strong></p>
'''

#print(content_html)


# send email
mail=smtplib.SMTP('smtp.gmail.com', 587)
mail.starttls()
mail.login(key, password)

msg = MIMEMultipart('alternative')
part1=MIMEText(content_text, 'html')
part2 = MIMEText(content_html, 'html')
msg.attach(part1)
msg.attach(part2)
msg['Subject'] = f'Daily Leetcode problem: {next_question["details"]["title"]}'
msg['From'] = key


for people in people_to_send_email_to:
    msg['To'] = people
    mail.sendmail(from_addr=msg['From'], to_addrs=people, msg=msg.as_string())

mail.quit()


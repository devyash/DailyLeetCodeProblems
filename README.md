# DailyLeetCodeProblems
Project to parse and send myself leetcode questions
The project will parse leet code daily and send me an email with the problem, the top 3 solutions with most votes based on the language I looked up also maybe a youtube link of the search with the problem, incase I still can't understand the problem

Installation Steps:
1.  install python 3.6+, venv, activate venv```
2. ``` pip install -r requirements.text```
3. run ```python config_setup.py```
4. update the `dev.ini` file with asked value(for cookies you will need to look at the comments in generate_list.py`
5. copy the jsons in parsed_question_list folder
6. run `python main.py` in the send_email folder


Sample Email:

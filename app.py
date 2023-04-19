from flask import Flask, render_template, jsonify, request
import pandas as pd
import random
import sqlite3
from hangeul_jamo_splitter import *

def name_split(name):
    res = []
    for syl in list(name):
        res += split_syllable(syl)
    return ''.join(res)


app = Flask(__name__)


# 데이터 불러오기
df = pd.read_csv('baseball_player.csv')
age_ls = list(map(lambda x: str(2023 - int(x.split('년')[0])), df['생일'].to_list()))
df['나이'] = age_ls
df['ID'] = df['ID'].astype('str')
df['번호'] = df['번호'].astype('str')
name_split_ls = []
name_ls = df['이름'].to_list()

for name in name_ls:
    name_split_ls.append(name_split(name))

df['이름분할'] = name_split_ls




# 랜덤한 ID 하나 선택하기
def select_random_player():
    random_id = random.choice(df['ID'].values)
    player = df[df['ID'] == random_id].iloc[0]
    return player

# 사용자가 입력한 선수와 정답 선수 비교하기
def compare_players(user_input, answer):
    result = {}
    for column in ['팀', '번호', '나이', '포지션', '투타유형']:
        if user_input[column] == answer[column]:
            result[column] = True
        else:
            result[column] = False
    return result

# answer = ''
# answer = select_random_player()
# print(answer.to_dict())

# 첫 화면
@app.route('/')
def index():


    return render_template('index.html')

# 재시작
@app.route('/restart', methods = ['GET'])
def restart():


    return render_template('index.html')

# 사용자가 입력한 값을 받아서 선수와 비교하기
@app.route('/guess', methods = ['POST'])
def guess():
    user_input = request.get_json()
    player = df[df['이름'] == user_input['player_name']].iloc[0]
    result = {}
    result['id'] = player['ID']
    result['name'] = player['이름']
    result['team'] = player['팀']
    result['number'] = player['번호']
    result['age'] = player['나이']
    result['position'] = player['포지션']
    result['hand'] = player['투타유형']
    return result

# 정답 얻기
@app.route('/answer', methods = ['POST'])
def answer():
    temp_answer = select_random_player().to_dict()
    answer = {}
    answer['id'] = str(temp_answer['ID'])
    answer['name'] = str(temp_answer['이름'])
    answer['team'] = str(temp_answer['팀'])
    answer['number'] = str(temp_answer['번호'])
    answer['age'] = str(temp_answer['나이'])
    answer['position'] = str(temp_answer['포지션'])
    answer['hand'] = str(temp_answer['투타유형'])
    print(answer)
    return answer

# 정답 얻기
@app.route('/search', methods = ['GET'])
def search():
    word = request.args.get('keyword')
    split_word = name_split(word)
    if word != '':
        conn = sqlite3.connect('test_db.sqlite')
        df.to_sql('players', conn, if_exists='replace', index=False)

        SQL = rf"""
        SELECT ID, 이름, 팀, 포지션 FROM players
        WHERE 이름분할 LIKE '{split_word}%'
        """
        df_temp = pd.read_sql(SQL,conn)
        # name_search_list = df_temp['이름'].to_list()
        temp_ls = list(zip(df_temp['이름'].to_list(), df_temp['팀'].to_list(), df_temp['포지션'].to_list()))
        temp_ls = list(map(lambda x: x[0] +' '+ x[1] +' '+ x[2], temp_ls))
        
    else:
        temp_ls = ['']
        
    return '\n'.join(temp_ls)


if __name__ == '__main__':
    app.run(debug=True)

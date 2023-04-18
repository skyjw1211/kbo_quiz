from flask import Flask, render_template, jsonify, request
import pandas as pd
import random

app = Flask(__name__)


# 데이터 불러오기
df = pd.read_csv('baseball_player.csv')
age_ls = list(map(lambda x: str(2023 - int(x.split('년')[0])), df['생일'].to_list()))
df['나이'] = age_ls
df['ID'] = df['ID'].astype('str')
df['번호'] = df['번호'].astype('str')


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


if __name__ == '__main__':
    app.run(debug=True)

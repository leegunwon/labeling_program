# app.py
from dash import Dash, dcc, html, Input, Output
from pymongo import MongoClient
import plotly.express as px

# MongoDB 연결 설정
client = MongoClient('mongodb://localhost:27017/')
db = client['my_db']  # 여기에 자신의 데이터베이스 이름을 입력하세요
collection = db['source']
cursor = collection.find({})

app = Dash(__name__)

# 초기 값 설정
answer = None
sequence = 0
seq = 0

# 간트 차트를 위한 예시 데이터
gantt_data =[dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
      dict(Task="Job-1", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete'),
      dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Not Started'),
      dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Complete'),
      dict(Task="Job-3", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
      dict(Task="Job-3", Start='2017-04-01', Finish='2017-04-20', Resource='Not Started'),
      dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
      dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')]

fig=px.timeline(gantt_data, x_start='Start', x_end='Finish', y='Task', color='Resource')

# Dash 애플리케이션 레이아웃 정의
app.layout = html.Div(children=[
    html.H1(children='Gantt Chart Dashboard'),

    html.Div(children=[
        # Left Gantt Chart와 버튼을 수평으로 배열
        html.Div(children=[
            dcc.Graph(
                id='left-gantt-chart',
                figure=fig,
                style={'height': '80vh'}  # 차트의 높이 조절
            ),
            html.Button('Left Button', id='left-button', n_clicks=0, style={'font-size': '60px'})  # 버튼의 크기 조절
        ], style={'display': 'inline-block', 'width': '48%'}),

        # Right Gantt Chart와 버튼을 수평으로 배열
        html.Div(children=[
            dcc.Graph(
                id='right-gantt-chart',
                figure=fig,
                style={'height': '80vh'}  # 차트의 높이 조절
            ),
            html.Button('Right Button', id='right-button', n_clicks=0, style={'font-size': '60px'})  # 버튼의 크기 조절
        ], style={'display': 'inline-block', 'width': '48%'}),
    ]),
])

# Left Button 클릭 시 MongoDB에 데이터 저장
@app.callback(
    Output('left-gantt-chart', 'figure'),
    [Input('left-button', 'n_clicks')]
)
def update_left_gantt_chart(n_clicks):
    global answer, sequence, seq
    answer = 0
    sequence += 1
    seq += 1
    # MongoDB에 데이터 저장
    collection.insert_one({'answer': answer})
    print(cursor[seq])
    # 갱신된 간트 차트 반환
    return gantt_data

# Right Button 클릭 시 MongoDB에 데이터 저장
@app.callback(
    Output('right-gantt-chart', 'figure'),
    [Input('right-button', 'n_clicks')]
)
def update_right_gantt_chart(n_clicks):
    global answer, sequence, seq
    answer = 1
    sequence += 1
    seq += 1

    print(cursor[seq])
    # MongoDB에 데이터 저장
    collection.insert_one({'answer': answer})
    # 갱신된 간트 차트 반환
    return gantt_data

if __name__ == '__main__':
    app.run_server(debug=True)

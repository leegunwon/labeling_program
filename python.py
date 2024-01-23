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
gantt_data1 = [
    dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
    dict(Task="Job-1", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete'),
    dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Not Started'),
    dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Complete'),
    dict(Task="Job-3", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
    dict(Task="Job-3", Start='2017-04-01', Finish='2017-04-20', Resource='Not Started'),
    dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
    dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')
]
gantt_data2 = [
    dict(Task="Task-1", Start='2023-03-01', Finish='2023-04-01', Resource='Complete'),
    dict(Task="Task-2", Start='2023-04-15', Finish='2023-05-15', Resource='Incomplete'),
    dict(Task="Task-3", Start='2023-03-17', Finish='2023-04-17', Resource='Not Started'),
    dict(Task="Task-4", Start='2023-03-17', Finish='2023-04-17', Resource='Complete'),
    dict(Task="Task-5", Start='2023-05-10', Finish='2023-05-20', Resource='Not Started'),
    dict(Task="Task-6", Start='2023-06-01', Finish='2023-06-20', Resource='Not Started'),
    dict(Task="Task-7", Start='2023-07-18', Finish='2023-08-18', Resource='Not Started'),
    dict(Task="Task-8", Start='2023-03-14', Finish='2023-05-14', Resource='Complete')
]

fig1 = px.timeline(gantt_data1, x_start='Start', x_end='Finish', y='Task', color='Resource')
fig2 = px.timeline(gantt_data2, x_start='Start', x_end='Finish', y='Task', color='Resource')

# Dash 애플리케이션 레이아웃 정의
app.layout = html.Div(children=[
    html.H1(children='Gantt Chart Dashboard'),

    html.Div(children=[
        # Top Gantt Chart
        html.Div(children=[
            dcc.Graph(
                id='top-gantt-chart',
                figure=fig1,
                style={'width': '100%', 'height': '40vh'}  # 차트의 너비와 높이 조절
            ),
            html.Div(children=[
                html.Button('Top Button', id='top-button', n_clicks=0, style={'font-size': '30px', 'width': '30%'}),
            ], style={'text-align': 'center', 'margin-top': '20px'}),
        ]),

        # Bottom Gantt Chart
        html.Div(children=[
            dcc.Graph(
                id='bottom-gantt-chart',
                figure=fig2,
                style={'width': '100%', 'height': '40vh'}  # 차트의 너비와 높이 조절
            ),
            html.Div(children=[
                html.Button('Bottom Button', id='bottom-button', n_clicks=0, style={'font-size': '30px', 'width': '30%'}),
            ], style={'text-align': 'center', 'margin-top': '20px'}),
        ]),
    ]),
])

# Top Button 클릭 시 MongoDB에 데이터 저장
@app.callback(
    Output('top-gantt-chart', 'figure'),
    [Input('top-button', 'n_clicks')]
)
def update_top_gantt_chart(n_clicks):
    global answer, sequence, seq
    answer = 0
    sequence += 1
    seq += 1
    # MongoDB에 데이터 저장
    collection.insert_one({'answer': answer})
    print("top")
    # 갱신된 간트 차트 반환
    return fig1

# Bottom Button 클릭 시 MongoDB에 데이터 저장
@app.callback(
    Output('bottom-gantt-chart', 'figure'),
    [Input('bottom-button', 'n_clicks')]
)
def update_bottom_gantt_chart(n_clicks):
    global answer, sequence, seq
    answer = 1
    sequence += 1
    seq += 1

    print(cursor[seq])
    # MongoDB에 데이터 저장
    collection.insert_one({'answer': answer})
    print("bottom")
    # 갱신된 간트 차트 반환
    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)

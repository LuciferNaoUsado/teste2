######################
# BIBLIOTECAS
import numpy as np
import openpyxl
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.figure_factory as ff

######################
# TRATAMENTO DOS DADOS

bd = pd.read_excel('BD.xlsx')
ref = pd.read_excel('Riscos.xlsx')

lista_orgao = bd.loc[:,'orgao'].unique()

ref['TODOS'] = [0,0,0,0]
for o in lista_orgao:
    bd_aux = bd.loc[bd['orgao'] == o,:].reset_index()
    ref[o] = [0,0,0,0]
    for i in range(4):
       for j in range(bd_aux.shape[0]):
           if ref.loc[i,'referencia'] in bd_aux.loc[j,'referencia']:
               ref.at[i,'TODOS'] += 1
               ref.at[i,o] += 1
# print(ref)

#######################
# DASHBOARD

app = Dash(__name__)
server = app.server

# dados
df = ref
lista_orgao = np.concatenate((np.array(['TODOS']), lista_orgao))

# criando gráfico
fig = ff.create_table(df.loc[:, ['referencia','risco','TODOS']].sort_values(by='TODOS',ascending=False))

app.layout = html.Div(children=[
    html.H1(children='TOP 4 RISCOS MAIS FREQUENTES'),

    dcc.Dropdown(lista_orgao, value='TODOS', id='drop'),

    dcc.Graph(
        id='tabela',
        figure=fig
    ),
    html.H1(children=''),
    html.H1(children='ATENÇÃO: DADOS FICTÍCIOS PARA TESTE!')
])

@app.callback(
    Output('tabela', 'figure'),
    Input('drop', 'value')
)
def update_output(value):
    fig = ff.create_table(df.loc[:, ['referencia','risco',value]].sort_values(by=value,ascending=False))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
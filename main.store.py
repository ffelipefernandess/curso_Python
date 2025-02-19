import plotly.graph_objs as graph_ob
import plotly.express as px
import pandas as pd
import dash 
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.dependencies import Input, Output
from dash import html, dcc, Input, Output

#configurando cores para os temos
dark_theme = 'darkly'
vapor_theme = 'vapor'
url_dark_theme = dbc.themes.DARKLY
url_vapor_theme = dbc.themes.VAPOR

#---------------dados---------------#
#importando os dados da tabela em csv
df = pd.read_csv('dataset_comp.csv')
df['dt_Venda'] = pd.to_datetime(df['dt_Venda'])
df['Mes'] = df['dt_Venda'].dt.strftime('%b').str.upper()

#---------------Listas---------------#
#cria lista de clientes
lista_cliente = []
for cliente in df['Cliente'].unique():
    lista_cliente.append ({'label': cliente,'value': cliente})

lista_cliente.append ({'label': 'Todos os Clientes', 'value': 'todos_cliente' })
#criando lista de meses
meses_br = dict (
    JAN = 'JAN', 
    FEV = 'FEV', 
    MAR = 'MAR', 
    APR = 'ABR', 
    MAY = 'MAI', 
    JUN = 'JUN', 
    JUL = 'JUL',
    AUG = 'AGO',
    SEP = 'SET',
    OCT = 'OUT',
    NOV = 'NOV',
    DEC = 'DEZ'
)
#cria lista de meses
lista_meses = []
for mes in df['Mes'].unique():
    mes_pt = meses_br.get(mes, mes)
    lista_meses.append({'label': mes_pt,'value':mes})

lista_meses.append ({'lavel': 'Ano Completo', 'value': 'ano_completo'})

#criando lista de categoria
lista_categorias = []
for categoria in df['Categorias'].unique():
    lista_categorias.append({'label': categoria, 'value': categoria})
    
lista_categorias.append ({'label': 'Todas as Categorias', 'value':'todas_categorias'})

#inicio do server
app = dash.Dash(__name__)
server = app.server

#---------------Layout---------------#
#elemento do select no superior esquerdo
layout_titulo = html.Div([
    html.Div(
        dcc.Dropdown(
            id='dropdown_cliente',
            options=lista_cliente,
            placeholder= lista_cliente[-1]['label'],
            style={
                'background-color':'transparent',
                'border':'none',
                'color':'black'
            }
        ), style={'width':'25%'}
    ),
    html.Div(
        html.Legend(
            'Sebrae Maranhão',
            style={
                'font-size':'150%',
                'text-align':'center'
            }
        ),
    style={'width':'50%'}
    ),
    html.Div(
        ThemeSwitchAIO(
            aio_id='theme',
            themes=[url_dark_theme,url_vapor_theme]
        ),
    style={'width':'25%'}
    )
],
    style={
       'text-align':'center',
        'display':'flex',
        'justify-content':'space-around',
        'align-items':'center',
        'font-family':'Fira Code',
        'margin-top':'20px'
    })
layout_linha01 = html.Div([
    html.Div([
        html.H4(id='output_cliente'),
        dcc.Graph(id='visual01')
    ],
    style={
        'width':'65%',
        'text-align':'center'
    }
    ),
    #primeira linha da segunda coluna
    html.Div([
        dbc.Checklist(
            id='radio_mes',
            options=lista_meses,
            inline=True
        ),
        dbc.RadioItems(
            id='radio_categorias',
            options=lista_categorias,
            inline=True
        )
    ],
    style={
        'width':'30%',
        'display':'flex',
        'flex-direction':'column',
        'justify-content':'space-evenly'
    })
],
    style={
        'display':'flex',
        'justify-content':'space-around',
        'margin-top':'40px',
        'height':'300px'
    }
)
layout_linha02 = html.Div([
    html.Div([
        html.H4('Vendas por Mês e Lojas/Cidade'),
        dcc.Graph(id='visual02')
    ],
    style={
        'width':'60%',
        'text-align':'center'
    }),
    html.Div(dcc.Graph(id='visual03'),style={'width':'35%'})
    ],
    style={
        'display':'flex',
        'justify-content':'space-around',
        'margin-top':'40px',
        'height':'150px'
    })  
 #carrega o layout
app.layout = html.Div([
    layout_titulo,
    layout_linha01,
    layout_linha02
])

#---------------Funções---------------#
def filtro_cliente(cliente_selecionado):
    if cliente_selecionado in Nome:
        return pd.Series(True, index=df.index)
    return df['Cliente'] == cliente_selecionado
    
def filtro_categoria(categoria_selecionado):
    if categoria_selecionado is None:
        return pd.Series(True, index=df.index)
    elif categoria_selecionado == 'todas_categorias':
        return pd.Series(True, index=df.index)
    return df['Categorias'] == categoria_selecionado
 
def filtro_mes(meses_selecionado):
    if not meses_selecionado:
        return pd.Series(True, index=df.index)
    elif 'ano_completo' in meses_selecionado:
        return pd.Series(True, index=df.index)
    else:
        return df['Mes'].isin(meses_selecionado)
#---------------Callbacks---------------#
@app.callback(
    Output('output_cliente','children'),
    [
        Input('dropdown_cliente','value'),
        Input('radio_categorias','value')
    ]
)
def atualizar_texto(cliente_selecionado,categoria_selecionado):
    if cliente_selecionado and categoria_selecionado:
        return f'TOP5{categoria_selecionado} | Cliente: {cliente_selecionado}'
    elif cliente_selecionado:
        return f'TOP5 Produtos | Cliente: {cliente_selecionado}'
    elif categoria_selecionado:
        return f'TOP5 {categoria_selecionado}'
    return f'TOP5 Categorias'

@app.callback(
   Output('visual01','figure'),
  [
        Input('dropdown_cliente','value'),
        Input('radio_mes','value'),
        Input('radio_categorias','value'),
        Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
    ]
)

#subindo servidor
if __name__ == '__main__':
    app.run_server(debug=True)

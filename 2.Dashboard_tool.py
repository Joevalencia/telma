# -*- coding: utf-8 -*-
"""

Dashboard Tools

"""
import os
import base64
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
import calendar
import pandas as pd
import warnings
from dash.dependencies import Input, Output
warnings.filterwarnings("ignore", category=UserWarning)

par_dir = os.path.dirname(__file__)



#f = r'C:\Users\Josè Valencia\Desktop\Barcelona Master\Semestre lV\CatedraUBZ\Provisions\rentas_P2.xlsx'

#image_path = r'C:\Users\jvalenciaf001\Documents\Python Files\Generali_imagen.jpg'

image_path = os.path.join(par_dir+'\\Generali_imagen.jpg')

with open(image_path, 'rb') as f:
    encoded_image = base64.b64encode(f.read()).decode('utf-8')


#par_dir = r'C:\Users\jvalenciaf001\Desktop\PwC\Clienti\Generali\Progetto UL\Dash_App'



# Get a list of all files in the folder
file_list = os.listdir(par_dir)

# GEnerali Logo
#logos_gene = r'C:\Users\jvalenciaf001\Documents\Python Files\Generali_investment.png'





#feather_file_path = r'C:\Users\jvalenciaf001\Desktop\PwC\Clienti\2050\data_converted\FUL90.feather'

feather_file_path = os.path.join(par_dir+'\\data_converted')
feather_file_path_ful90 = os.path.join(feather_file_path+'\\FUL90.feather')


df = pd.read_feather(feather_file_path_ful90)
# print('Numero de productos fichero completo.', len(df.PRODUCTO.unique())) ## 43 pero quitar los que no son G
# print('Numero de fondos fichero completo', len(df.FONDO.unique())-2) ## -2 porque era un Non Value
    
# Cambio a NaN donde llenaba con C y P
# df['FONDO'] = df['FONDO'].replace(['C', 'P'], np.nan)
# df['VALORADO'] = pd.Series([np.nan if x is None else x for x in df.VALORADO])
# df['CTA_DES'] = pd.Series([np.nan if x is None else x for x in df.CTA_DES])
# df['GENERADO'] = pd.Series([np.nan if x is None else x for x in df.GENERADO])
# df['FMOVTO'] = pd.to_datetime(df.FMOVTO, dayfirst=True)
# df['FVALOR'] = pd.to_datetime(df.FVALOR, dayfirst=True)
# df['IMPORT'] = pd.to_numeric(df.IMPORT, errors='coerce')
# df = df[df['FMOVTO'] >= '2023-01-01']

# df['FMOVTO'] = pd.to_datetime(df['FMOVTO'])

# df_no_mov = df[~df.duplicated(subset='IMPORT', keep=False)]
# df = df[df.duplicated(subset='IMPORT', keep=False)]
# print('Número de pólizas que seràn eliminadas porque no tienen un fondo de CU/VU destino: ', str(len(df_no_mov.POLIZA.unique())))




# Diccionario vacío para almacenar los DataFrames por mes.
# Es decir habrán 12 matrices de los movimientos, cada una representa los movimientos en ese mes Mes_1 = ENERO, Mes_2 = FEBRERO.
df_por_mes = {}

for mes in range(1, 13):
    # Filtra el DataFrame original por el mes actual
    df_mes_actual = df[df['FMOVTO'].dt.month == mes]
    df_por_mes[f'Mes_{mes}'] = df_mes_actual
df.sort_values(by='FMOVTO')
df = df[df.CIA.isin(['G', '1', '5'])]
df_mov_2023 = df  ### df_mov_2023 contiene todos los movimiento del 2023
df_mov_2023 = df_mov_2023[df_mov_2023.CIA.isin(['G', '1', '5'])] #  Obtengo df G, 1, 5, movimientos 2023


# Diccionario para almacenar meses del año de modo acumulado
df_acumulado_por_mes = {}

for mes in range(1, 13):
    
    # Filtracion del DataFrame original hasta el mes actual
    df_hasta_mes = df[df['FMOVTO'].dt.month <= mes]
    df_acumulado_por_mes[f'Mes_{mes}'] = df_hasta_mes


# Lista de productos
lista_productos = list(df_mov_2023.PRODUCTO.unique())
marks_dict_productos = {i: producto for i, producto in enumerate(lista_productos)}

## Lista producto para desplegable del gráfico de Sankey 
options_list = [{'label': producto.strip(), 'value': producto.strip()} for producto in lista_productos]

#options_list for sunburst
options_list_sunburst = options_list + [{'label': 'Todos', 'value': 'Todos'}]
# Nombres de los meses
nombres_meses = [calendar.month_name[i] for i in range(1, 13)]


# Funcion para el sunburst plot acumulativos mes por mes PI, PU, CA, EE, AE, EE, EI
def grafico_mes_acc_sunburst(df, mes):
     
    filtro2 = df.get(mes)[df.get(mes).PROMOV.isin(['PU', 'PI',
                                                   'CA', 'EE', 
                                                   'AE', 'EI'])].query('RAZMOV =="CU"').groupby(['PRODUCTO',
                                                                                                 'FONDO']).agg({'IMPORT':'sum'})
    filtro2 = filtro2.reset_index()
    sunburst_plot_acumulativo = px.sunburst(filtro2, path = ['PRODUCTO', 'FONDO'], values = 'IMPORT',
                                            title=f'Importes por Producto y Fondo (CU) acumulado hasta el {mes}',
                                            width=800, height=600, color_continuous_scale='Reds',# color ='IMPORT', 
                                           color_continuous_midpoint=0,  range_color=[0, filtro2['IMPORT'].max()])
    return sunburst_plot_acumulativo

##############################################################
##               SOLO PRODUCTO AGREGADO  CU     ##############
##############################################################
def sunburst_prod_standalone_agg(df, mes, producto):
    
    q1= df.get(mes)[df.get(mes).PROMOV.isin(['PU', 
                                             'PI', 'CA', 'AE', 'EE',
        'EI'])].query(f'PRODUCTO == "{producto}"').query('RAZMOV == "CU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':'sum'})
    q1 = q1.reset_index()
    plot_trial = px.sunburst(q1, path = ['PRODUCTO',
                                        'FONDO'], values = 'IMPORT',
                            title=f'Importes por Producto y Fondo (CU) en el {mes} del producto {producto}',
                                                width=800, height=600, color_continuous_scale='Reds',# color ='IMPORT', 
                                               color_continuous_midpoint=0,  range_color=[0, q1['IMPORT'].max()])
    return plot_trial


## SOLO PRODUCTO NO AGREGADO para compra de unidades

def sunburst_prod_standalone_no(df, mes, producto):
    
    q1= df.get(mes)[df.get(mes).PROMOV.isin(['PU', 
                                             'PI', 'CA', 'AE', 'EE',
        'EI'])].query(f'PRODUCTO == "{producto}"').query('RAZMOV == "CU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':'sum'})
    q1 = q1.reset_index()
    plot_trial = px.sunburst(q1, path = ['PRODUCTO',
                                        'FONDO'], values = 'IMPORT',
                            title=f'Importes por Producto y Fondo (CU) acumulado hasta el {mes} del producto {producto}',
                                                width=800, height=600, color_continuous_scale='Reds',# color ='IMPORT', 
                                               color_continuous_midpoint=0,  range_color=[0, q1['IMPORT'].max()])
    return plot_trial




##############################################################
##               SOLO PRODUCTO AGREGADO  VU     ##############
##############################################################
def sunburst_prod_standalone_agg_vu(df, mes, producto):
    
    q1= df.get(mes)[df.get(mes).PROMOV.isin(['RT',
                    'RP'])].query(f'PRODUCTO == "{producto}"').query('RAZMOV == "VU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':'sum'})
    q1 = q1.reset_index()
    plot_trial = px.sunburst(q1, path = ['PRODUCTO',
                                        'FONDO'], values = 'IMPORT',
                            title=f'Importes por Producto y Fondo (VU) en el {mes} del producto {producto}',
                                                width=800, height=600, color_continuous_scale='Reds',# color ='IMPORT', 
                                               color_continuous_midpoint=0,  range_color=[0, q1['IMPORT'].max()])
    return plot_trial


## SOLO PRODUCTO NO AGREGADO para compra de unidades

def sunburst_prod_standalone_no_vu(df, mes, producto):
    
    q1= df.get(mes)[df.get(mes).PROMOV.isin(['RT', 
                    'RP'])].query(f'PRODUCTO == "{producto}"').query('RAZMOV == "VU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':'sum'})
    q1 = q1.reset_index()
    plot_trial = px.sunburst(q1, path = ['PRODUCTO',
                                        'FONDO'], values = 'IMPORT',
                            title=f'Importes por Producto y Fondo (VU) acumulado hasta el {mes} del producto {producto}',
                                                width=800, height=600, color_continuous_scale='Reds',# color ='IMPORT', 
                                               color_continuous_midpoint=0,  range_color=[0, q1['IMPORT'].max()])
    return plot_trial




# Funcion para el sunburst plot acumulativo mes por mes RT, RP
def grafico_mes_acc_sunburst_rp_rt(df, mes):
     
    filtro2 = df.get(mes)[df.get(mes).PROMOV.isin(['RP', 'RT'])].query('RAZMOV =="VU"').groupby(['PRODUCTO',
                                                                                                 'FONDO']).agg({'IMPORT':'sum'})
    filtro2 = filtro2.reset_index()
    sunburst_plot_acumulativo = px.sunburst(filtro2, path = ['PRODUCTO', 'FONDO'], values = 'IMPORT',
                                            title=f'Importes por Producto y Fondo (VU) acumulado hasta el {mes}',
                                            width=800, height=600, color_continuous_scale='Reds',# color ='IMPORT', 
                                           color_continuous_midpoint=0,  range_color=[0, filtro2['IMPORT'].max()])
    return sunburst_plot_acumulativo



## FUNCION PARA GRAFICA EL SANKEY PLOT

#PRIMO SANKEY PLOT
def sankey_primo_all(df, mes='Mes_1', producto_type='OILX4', traspaso_type='TT'):
    filtro3 = df.get(mes)
    filtro3 = filtro3[filtro3.RAZMOV.isin(['CU', 'VU'])].query(f'PROMOV == "{traspaso_type}"')
    filtro3 = filtro3.query(f'PRODUCTO == "{producto_type}"')#.groupby(['PRODUCTO', 'RAZMOV']).agg({'IMPORT':'sum'})
    filtro3 = filtro3[filtro3.duplicated(subset='IMPORT', keep=False)]
    
    data =filtro3[['RAZMOV', 'FONDO','POLIZA', 'IMPORT']].values.tolist()

    data = pd.DataFrame(data, columns=['RAZMOV', 'FONDO', 'POLIZA', 'IMPORT'])

    # Crear listas únicas de nodos y enlaces
    nodes = list(set([item for sublist in data.values for item in sublist[0:3]]))
    links = []
    for _, row in data.iterrows():
        links.append({"source": nodes.index(row['RAZMOV']), "target": nodes.index(row['FONDO']), "value": row['IMPORT']})

    # Sankey Plot
    node_labels = nodes  # Utilizar directamente la lista de nodos como etiquetas
    link_labels = [dict(source=link["source"], target=link["target"], value=link["value"]) for link in links]

    # Figura Sankey
    fig = go.Figure(go.Sankey(
        node=dict(label=node_labels),
        link=dict(source=[link["source"] for link in links], 
                  target=[link["target"] for link in links], 
                  value=[link["value"] for link in links])
    ))

    fig.update_layout(title_text=f"Sankey Plot CU/VU para el producto {producto_type} en PROMOV {traspaso_type} ", 
                      font_size=10)
    return fig


# Secondo Sankey
def sankey_secondo_all(df, mes='Mes_1', producto_type='OILX4', traspaso_type='TT'):
    filtro3 = df.get(mes)
    filtro3 = filtro3[filtro3.RAZMOV.isin(['CU', 'VU'])].query(f'PROMOV == "{traspaso_type}"')
    filtro3 = filtro3.query(f'PRODUCTO == "{producto_type}"')#.groupby(['PRODUCTO', 'RAZMOV']).agg({'IMPORT':'sum'})
    filtro3 = filtro3[filtro3.duplicated(subset='IMPORT', keep=False)]
    
    data =filtro3[['RAZMOV', 'FONDO','POLIZA', 'IMPORT']].values.tolist()
    
    data = pd.DataFrame(data, columns=['RAZMOV', 'FONDO', 'POLIZA', 'IMPORT'])
    data2 = data
    
    ## Definicion de nodos
    nodos_origen = pd.unique(data2.query('RAZMOV == "CU"')['FONDO'])
    nodos_destino = pd.unique(data2.query('RAZMOV == "VU"')['FONDO'])

    # Combinar listas de nodos
    nodos_combinados = pd.concat([pd.Series(nodos_origen), pd.Series(nodos_destino)], ignore_index=True).unique()

    source_index = data2.query('RAZMOV == "CU"')['FONDO'].map(lambda x: nodos_combinados.tolist().index(x) if x in nodos_combinados else None)
    target_index = data2.query('RAZMOV == "VU"')['FONDO'].map(lambda x: nodos_combinados.tolist().index(x) + len(nodos_origen) if x in nodos_combinados else None)


    # Crear el Sankey plot
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=nodos_combinados
        ),
        link=dict( 
            source=data.query('RAZMOV == "CU"')['FONDO'].map(lambda x: nodos_combinados.tolist().index(x)),
            target=data.query('RAZMOV == "VU"')['FONDO'].map(lambda x: nodos_combinados.tolist().index(x) + len(nodos_origen)),
            value=data.query('RAZMOV == "CU"')['IMPORT']
        )
    )])

    # 
    fig.update_layout(title_text=f"Sankey del producto {producto_type} en PROMOV {traspaso_type}")

    return fig

# Terzo Sankey plot

def sankey_terzo_all(df, mes, producto_type, traspaso_type):
    filtro3 = df.get(mes)
    filtro3 = filtro3[filtro3.RAZMOV.isin(['CU', 'VU'])].query(f'PROMOV == "{traspaso_type}"')
    filtro3 = filtro3.query(f'PRODUCTO == "{producto_type}"')#.groupby(['PRODUCTO', 'RAZMOV']).agg({'IMPORT':'sum'})
    filtro3 = filtro3[filtro3.duplicated(subset='IMPORT', keep=False)]
    
    data =filtro3[['RAZMOV', 'FONDO','POLIZA', 'IMPORT']].values.tolist()
    
    data = pd.DataFrame(data, columns=['RAZMOV', 'FONDO', 'POLIZA', 'IMPORT'])
    data2 = data
    
    # nodos únicos de origen y destino
    nodos_origen = pd.unique(data2.query('RAZMOV == "VU"')['FONDO'])
    nodos_destino = pd.unique(data2.query('RAZMOV == "CU"')['FONDO'])

    # Combinar listas de nodos
    nodos_combinados = pd.concat([pd.Series(nodos_origen), pd.Series(nodos_destino)], ignore_index=True).unique()

    # Duplicar los labels para mostrar en ambos lados
    nodos_combinados = list(nodos_combinados) + list(nodos_combinados)

    # Crear un diccionario para mapear nodos a Indices
    nodo_a_indice = {nodo: indice for indice, nodo in enumerate(nodos_combinados)}

    # Crear listas de índices de origen y destino
    source_index = data2.query('RAZMOV == "VU"')['FONDO'].map(nodo_a_indice)
    target_index = data2.query('RAZMOV == "CU"')['FONDO'].map(lambda x: nodo_a_indice.get(x, None))

    # Crear el Sankey plot
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=nodos_combinados
        ),
        link=dict(
            source=source_index,
            target=target_index,
            value=data2.query('RAZMOV == "VU"')['IMPORT']
        )
    )])

    # Añadir título
    fig.update_layout(title_text=f"Sankey Plot nodos unicos VU/CU del {producto_type} en {traspaso_type}")

    # Mostrar el gráfico
    return fig

    

# Figuras del Dashboard

## APP DASH
#app = JupyterDash(__name__)

app = dash.Dash(__name__)
app.layout = html.Div(      
    style={'backgroundColor': 'rgba(183, 40, 26, 1)', 'display': 'inline-block'},
                      children=[
                          
                          html.Div([
                              html.Img(src=f'data:image/jpeg;base64,{encoded_image}', 
                                       style={'width': '10%',
                                              'height':'20%',
                                              'textAlign':'top-right'}),
                              
                              html.H1(children='Cierre de Individual Savings & Investments - Análisis de FUL90.',
                                      style={'backgroundColor': 'rgba(183, 40, 26, 1)',
                                             'textAlign': 'center',
                                             'padding': '16px 0 16px 20px',
                                             'color': 'ivory',
                                             'font-family': 'Computer Modern Roman',
                                             'font-size': '450%'},
                                      
                                       
                                          )
                              ]

                                  ), #          Papyrus

                          html.P(children='Demo para el tool lanzamiento cierre en sus ficheros CVUL, PATR, FUL90',
                                 style={'backgroundColor': 'rgba(183, 40, 26, 1)',
                                        'textAlign': 'center',
                                        'padding': '10px 0 10px 14px',
                                        'color': 'gold',
                                        'font-family': 'ZERO HOUR',
                                        'font-size': '150%'

                                        }
                                 ),
                          
                          html.Div(children='''
                                   Lanzamiento: A tool built-on WEB app-like for UL life insurance product business analysis.
                                   ''', style={'textAlign': 'center', 'color': 'ivory',
                                   'font-family': 'ZERO HOUR', 'font-size': '170%'}),

                  
                       
                            
                          html.Br(),
                          # INIZIO 1 PLOT por CU, en PI, PU, EE, EI, CA, AE

                          html.H3(children='Deslizar para visualizar los movimientos por meses del FUL90 en gráfico Sunburst Plot de PU PI CA AE EE EI.',
                                  style={'backgroundColor': 'rgba(183, 40, 26, 1)',
                                         'textAlign': 'center',
                                         'padding': '10px 0 10px 14px',
                                         'color': 'gold',
                                         'font-family': 'ZERO HOUR',
                                         'font-size': '150%'

                                         }),
                          
                          
                          html.Br(),
                          # Desplegable de los productos para el sunburst plot
                          
                          
                            ## Desplegable Productos
                            dcc.Dropdown(
                                            id='producto_dropdown_standalone_CU',
                                            options=options_list_sunburst,
                                            value='Todos',  
                                            style={'width': '50%', 'display':'center'}
                                        )
                                        ,
                          
                          html.Br(),
                          
                          

                          html.Div(
                              dcc.Slider(   min=1,
                                            max=12,
                                            step=None,
                                            tooltip={"placement": "bottom", "always_visible": True},
                                            id='annata',
                                            value=1,
                                            marks={i: {
                                                "label": str(mes),
                                                "style": {"color": "yellow"}
                                            } for i, mes in enumerate(nombres_meses, start=1)}
                                        ), style={
                                            'display': 'center',
                                            'color': 'ivory',
                                            'font-weight': 'bold'}
                                            ),

                                            
                          html.Br(),
                          
               
                          
        
                          html.Div([
                                                            
                              dcc.Graph(id='gra33', style={'color': 'navy'},
                                        figure={}),
                              dcc.Graph(id='gra33_acumulado_por_mes', style={'color': 'navy'},
                                        figure={})
                             
                              ], style={'width': '80%',
                                     'height':'80%', 'margin':'auto',
                                     'display': 'flex'}
                          ),
                       
                          # FINE 1 PLOT por CU, en PI, PU, EE, EI, CA, AE
                          
                          html.Br(),
                          
                          # INIZIO 2 PLOT por VU, en RT y RP
                          
                          html.H3(children='Deslizar para visualizar los movimientos por meses del FUL90 en gráfico Sunburst Plot de RT y RP.',
                                  style={'backgroundColor': 'rgba(183, 40, 26, 1)',
                                         'textAlign': 'center',
                                         'padding': '10px 0 10px 14px',
                                         'color': 'gold',
                                         'font-family': 'ZERO HOUR',
                                         'font-size': '150%'

                                         }),
                          
                          
                          
                          html.Br(),
                          # Desplegable de los productos para el sunburst plot
                          
                          
                            ## Desplegable Productos
                            dcc.Dropdown(
                                            id='producto_dropdown_standalone_VU',
                                            options=options_list_sunburst,
                                            value='Todos',  
                                            style={'width': '50%', 'display':'center'}
                                        )
                                        ,
                          
                          html.Br(),
                          
                          
                          

                          html.Div(
                              dcc.Slider(   min=1,
                                            max=12,
                                            step=None,
                                            tooltip={"placement": "bottom", "always_visible": True},
                                            id='annata_2',
                                            value=1,
                                            marks={i: {
                                                "label": str(mes),
                                                "style": {"color": "yellow"}
                                            } for i, mes in enumerate(nombres_meses, start=1)}
                                        ), style={
                                            'display': 'center',
                                            'color': 'ivory',
                                            'font-weight': 'bold'}
                                            ),

                                            
                          html.Br(),
        
                          html.Div([
                                                            
                              dcc.Graph(id='gra33_2', style={'color': 'navy'},
                                        figure={}),
                              dcc.Graph(id='gra33_2_acumulado_por_mes', style={'color': 'navy'},
                                        figure={})
                             
                              ], style={'width': '80%',
                                     'height':'80%',
                                    'margin': 'auto', 'display':'flex'}
                          ),
                          
 



                            # FINE 2 PLOT por VU, en RT y RP
                            
                            
                            # COMPRA COMPARACION PRODCUTOS
                            html.Br(),
                            
                            html.H3(children='Deslizar para visualizar la comparativa por meses del FUL90 en gráfico Sunburst Plot de PU PI CA AE EE EI de COMPRAS.',
                                    style={'backgroundColor': 'rgba(183, 40, 26, 1)',
                                           'textAlign': 'center',
                                           'padding': '10px 0 10px 14px',
                                           'color': 'gold',
                                           'font-family': 'ZERO HOUR',
                                           'font-size': '150%'

                                           }),
                            
                            html.Div([
                                       dcc.Dropdown(
                                           id='producto_dropdown_standalone_CU_p1',
                                           options=options_list_sunburst,
                                           value='Todos',  
                                           style={'width': '50%'}
                                       ),
                                   ], style={'display': 'inline-block', 'width': '48%'}),
                                   
                                   html.Div([
                                       dcc.Dropdown(
                                           id='producto_dropdown_standalone_CU_p2',
                                           options=options_list_sunburst,
                                           value='Todos',  
                                           style={'width': '50%'}
                                       ),
                                   ], style={'display': 'inline-block', 'width': '48%', 'float': 'right'}),
                                   
                            html.Br(),
                            
                            html.Div(
                                dcc.Slider(   min=1,
                                              max=12,
                                              step=None,
                                              tooltip={"placement": "bottom", "always_visible": True},
                                              id='annata_compare',
                                              value=1,
                                              marks={i: {
                                                  "label": str(mes),
                                                  "style": {"color": "yellow"}
                                              } for i, mes in enumerate(nombres_meses, start=1)}
                                          ), style={
                                              'display': 'center',
                                              'color': 'ivory',
                                              'font-weight': 'bold'}
                                              ),
                            
                            
                            
                            html.Br(),
                            
                            html.Div([
                                                              
                                dcc.Graph(id='compare_p1', style={'color': 'navy'},
                                          figure={}),
                                dcc.Graph(id='compare_p2', style={'color': 'navy'},
                                          figure={})
                               
                                ], style={'width': '80%',
                                       'height':'80%',
                                      'margin': 'auto', 'display':'flex'}
                            ),
                            
                            html.Br(),
                            
                            ####################################
                            # VENTAS COMPARACIOIN PRODUCTOS ###
                            ###################################
                            
                            html.Div([
                                       dcc.Dropdown(
                                           id='producto_dropdown_standalone_VU_p1',
                                           options=options_list_sunburst,
                                           value='Todos',  
                                           style={'width': '50%'}
                                       ),
                                   ], style={'display': 'inline-block', 'width': '48%'}),
                                   
                                   html.Div([
                                       dcc.Dropdown(
                                           id='producto_dropdown_standalone_VU_p2',
                                           options=options_list_sunburst,
                                           value='Todos',  
                                           style={'width': '50%'}
                                       ),
                                   ], style={'display': 'inline-block', 'width': '48%', 'float': 'right'}),
                                   
                            html.Br(),
                            
                            html.H3(children='Deslizar para visualizar la comparativa por meses del FUL90 en gráfico Sunburst Plot de RT y RP de VENTAS.',
                                    style={'backgroundColor': 'rgba(183, 40, 26, 1)',
                                           'textAlign': 'center',
                                           'padding': '10px 0 10px 14px',
                                           'color': 'gold',
                                           'font-family': 'ZERO HOUR',
                                           'font-size': '150%'

                                           }),
                            
                            html.Div(
                                dcc.Slider(   min=1,
                                              max=12,
                                              step=None,
                                              tooltip={"placement": "bottom", "always_visible": True},
                                              id='annata_compare_VU',
                                              value=1,
                                              marks={i: {
                                                  "label": str(mes),
                                                  "style": {"color": "yellow"}
                                              } for i, mes in enumerate(nombres_meses, start=1)}
                                          ), style={
                                              'display': 'center',
                                              'color': 'ivory',
                                              'font-weight': 'bold'}
                                              ),
                            
                            
                            
                            html.Br(),
                            
                            html.Div([
                                                              
                                dcc.Graph(id='compare_p1_VU', style={'color': 'navy'},
                                          figure={}),
                                dcc.Graph(id='compare_p2_VU', style={'color': 'navy'},
                                          figure={})
                               
                                ], style={'width': '80%',
                                       'height':'80%',
                                      'margin': 'auto', 'display':'flex'}
                            ),
                            
                            
                                          
                                          
                                          
                                          
                                          
                            html.Br(),        
                            
                            
                            ## INIZIO SANKEY PLOT
                            
                            html.H3(children='Deslizar para visualizar los movimientos por meses del FUL90 en gráfico SANKEY de traspasos.',
                                    style={'backgroundColor': 'rgba(183, 40, 26, 1)',
                                           'textAlign': 'center',
                                           'padding': '10px 0 10px 14px',
                                           'color': 'gold',
                                           'font-family': 'ZERO HOUR',
                                           'font-size': '150%'

                                           }),

                            html.Div(
                                dcc.Slider(   min=1,
                                              max=12,
                                              step=None,
                                              tooltip={"placement": "bottom", "always_visible": True},
                                              id='annata_3',
                                              value=1,
                                              marks={i: {
                                                  "label": str(mes),
                                                  "style": {"color": "yellow"}
                                              } for i, mes in enumerate(nombres_meses, start=1)}
                                          ), 
                            
                            
                             
                                
                                style={
                                              'display': 'center',
                                              'color': 'ivory',
                                              'font-weight': 'bold'}
                                
                                
                                              ),
                            
                            html.Br(),
                            
                            
                            
                            ## Desplegable Productos
                            dcc.Dropdown(
                                            id='producto_dropdown',
                                            options=options_list,
                                            value='OILX4',  
                                            style={'width': '50%', 'display':'left'}
                                        )
                                        ,
                                        
                          
                            
                            ## Desplegable para traspasos (TT) y (TP)
                            dcc.Dropdown(
                                            id='traspaso_dropdown',
                                            options=[
                                                {'label': 'TT', 'value': 'TT'},
                                                {'label': 'TP', 'value': 'TP'}
                                            ],
                                            value='TT',  
                                            style={'width': '50%', 'display': 'right'}
                                        ),

                            
                            
                            
                            
                            
                            html.Br(),
                                              
                            
                            
                                              
                            # GRAFICOS SANKEY
                            
                            #### SANKEY EN TT
                             html.Div([
                                 dcc.Graph(id='PRIMO_SANKEY_TT', style={'color': 'navy'},
                                           figure={}),
                                 dcc.Graph(id='SECONDO_SANKEY_TT', style={'color': 'gold'},
                                           figure={}),
                                 dcc.Graph(id='TERZO_SANKEY_TT', style={'color': 'navy'},
                                           figure={})
                                 ], style={'width': '50%', 'display': 'flex'}),
                            
                            html.Br(),
                            
                            #### SANKEY EN TP
                            # html.Div([
                            #     dcc.Graph(id='PRIMO_SANKEY_TP', style={'color': 'navy'},
                            #               figure={}),
                            #     dcc.Graph(id='SECONDO_SANKEY_TP', style={'color': 'gold'},
                            #               figure={}),
                            #     dcc.Graph(id='TERZO_SANKEY_TP', style={'color': 'navy'},
                            #               figure={})
                            #  ], style={'width': '50%', 'display': 'flex'}),
                            
                            
                            
                            ## FINE SANKEY PLOT
                            






                            
                          
                         
]) # fin dashapp


## PRINMA COMPARATIVA INDEPENDIENTE VENTAS

@app.callback(
      Output('compare_p1_VU', 'figure'),
           
      [Input('annata_compare_VU', 'value'),
        Input('producto_dropdown_standalone_VU_p1', 'value'),
      
      
      
])                                             
                                              
def vender_dos_p1(value, productos_1):
    if productos_1 == 'Todos':
        
        
        
        
        # Funcion para obtener la agrupacion mes por mes
        def df_pu_pi_agg_function(df, mes):
            
            filtro1 = df.get(mes)[df.get(mes).PROMOV.isin(['RT',
                'RP'])].query('RAZMOV == "CU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':'sum'})
                    
            fig = px.sunburst(filtro1.reset_index(), path=['PRODUCTO', 'FONDO'], values='IMPORT', 
                              title=f'Importes por Producto y Fondo (VU) en el {mes}',
                              width=800, height=600, color_continuous_scale='Reds',
                              color_continuous_midpoint=0,  range_color=[0, filtro1['IMPORT'].max()])
            
            return fig
        
        
        if value == 1: ## Mes de ENERO
            #g1 = df_pu_pi_agg_function(df_por_mes, 'Mes_1')
            g1_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_1')
            return g1_acc
            
        elif value == 2:  ## Mes de FEBRERO
            #g2 = df_pu_pi_agg_function(df_por_mes, 'Mes_2')
            g2_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_2')
            return g2_acc
        
        elif value == 3:  ## Mes de MARZO
            #g3 = df_pu_pi_agg_function(df_por_mes, 'Mes_3')
            g3_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_3')
            return g3_acc
        
        elif value == 4:  ## Mes de ABRIL
            #g4 = df_pu_pi_agg_function(df_por_mes, 'Mes_4')
            g4_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_4')
            return g4_acc
        
        elif value == 5:  ## Mes de MAYO
            #g5 = df_pu_pi_agg_function(df_por_mes, 'Mes_5')
            g5_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_5')
            return g5_acc
        
        elif value == 6:  ## Mes de JUNIO
            #g6 = df_pu_pi_agg_function(df_por_mes, 'Mes_6')
            g6_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_6')
            return g6_acc
        
        elif value == 7:  ## Mes de JULIO
            #g7 = df_pu_pi_agg_function(df_por_mes, 'Mes_7')
            g7_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_7')
            return g7_acc
        
        elif value == 8:  ## Mes de AGOSTO
            #g8 = df_pu_pi_agg_function(df_por_mes, 'Mes_8')
            g8_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_8')
            return g8_acc
        
        elif value == 9:  ## Mes de SEPTIEMBRE
            #g9 = df_pu_pi_agg_function(df_por_mes, 'Mes_9')
            g9_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_9')
            return g9_acc
        
        elif value == 10:  ## Mes de OCTUBRE
            #g10 = df_pu_pi_agg_function(df_por_mes, 'Mes_10')
            g10_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_10')
            return g10_acc
        
        elif value == 11:  ## Mes de NOVIEMBRE
            #g11 = df_pu_pi_agg_function(df_por_mes, 'Mes_11')
            g11_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_11')
            return g11_acc
        
        elif value == 12:  ## Mes de DICIEMBRE
            #g12 = df_pu_pi_agg_function(df_por_mes, 'Mes_12')
            g12_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_12')
            return g12_acc
        
    else:
        
        if value == 1:
            #g1 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_1', productos_1)
            g11 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_1', productos_1)
            return g11
        elif value == 2:
            #g2 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_2', productos_1)
            g22 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_2', productos_1)
            return g22
        elif value == 3:
            #g3 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_3', productos_1)
            g33 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_3', productos_1)
            return g33
        elif value == 4:
            #g4 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_4', productos_1)
            g44 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_4', productos_1)
            return g44
        elif value == 5:
            #g5 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_5', productos_1)
            g55 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_5', productos_1)
            return g55
        elif value == 6:
            #g6 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_6', productos_1)
            g66 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_6', productos_1)
            return g66
        elif value == 7:
            #g7 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_7', productos_1)
            g77 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_7', productos_1)
            return g77
        elif value == 8:
            #g8 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_8', productos_1)
            g88 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_8', productos_1)
            return g88
        elif value == 9:
            #g9 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_9', productos_1)
            g99 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_9', productos_1)
            return g99
        elif value == 10:
            #g10 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_10', productos_1)
            g100 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_10', productos_1)
            return g100
        elif value == 11:
            #g11 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_11', productos_1)
            g110 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_11', productos_1)
            return g110
        elif value == 12:
            #g12 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_12', productos_1)
            g120 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_12', productos_1)
            return g120                                         



# SEGUNDA COMPARATIVA VENTAS


@app.callback(
      Output('compare_p2_VU', 'figure'),
           
      [Input('annata_compare_VU', 'value'),
        Input('producto_dropdown_standalone_VU_p2', 'value'),
      
      
      
])                                             
                                              
def vender_dos_p2(value, productos_1):
    if productos_1 == 'Todos':
        
        
        
        
        # Funcion para obtener la agrupacion mes por mes
        def df_pu_pi_agg_function(df, mes):
            
            filtro1 = df.get(mes)[df.get(mes).PROMOV.isin(['RT',
                'RP'])].query('RAZMOV == "CU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':'sum'})
                    
            fig = px.sunburst(filtro1.reset_index(), path=['PRODUCTO', 'FONDO'], values='IMPORT', 
                              title=f'Importes por Producto y Fondo (VU) en el {mes}',
                              width=800, height=600, color_continuous_scale='Reds',
                              color_continuous_midpoint=0,  range_color=[0, filtro1['IMPORT'].max()])
            
            return fig
        
        
        if value == 1: ## Mes de ENERO
            #g1 = df_pu_pi_agg_function(df_por_mes, 'Mes_1')
            g1_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_1')
            return g1_acc
            
        elif value == 2:  ## Mes de FEBRERO
            #g2 = df_pu_pi_agg_function(df_por_mes, 'Mes_2')
            g2_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_2')
            return g2_acc
        
        elif value == 3:  ## Mes de MARZO
            #g3 = df_pu_pi_agg_function(df_por_mes, 'Mes_3')
            g3_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_3')
            return g3_acc
        
        elif value == 4:  ## Mes de ABRIL
            #g4 = df_pu_pi_agg_function(df_por_mes, 'Mes_4')
            g4_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_4')
            return g4_acc
        
        elif value == 5:  ## Mes de MAYO
            #g5 = df_pu_pi_agg_function(df_por_mes, 'Mes_5')
            g5_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_5')
            return g5_acc
        
        elif value == 6:  ## Mes de JUNIO
            #g6 = df_pu_pi_agg_function(df_por_mes, 'Mes_6')
            g6_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_6')
            return g6_acc
        
        elif value == 7:  ## Mes de JULIO
            #g7 = df_pu_pi_agg_function(df_por_mes, 'Mes_7')
            g7_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_7')
            return g7_acc
        
        elif value == 8:  ## Mes de AGOSTO
            #g8 = df_pu_pi_agg_function(df_por_mes, 'Mes_8')
            g8_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_8')
            return g8_acc
        
        elif value == 9:  ## Mes de SEPTIEMBRE
            #g9 = df_pu_pi_agg_function(df_por_mes, 'Mes_9')
            g9_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_9')
            return g9_acc
        
        elif value == 10:  ## Mes de OCTUBRE
            #g10 = df_pu_pi_agg_function(df_por_mes, 'Mes_10')
            g10_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_10')
            return g10_acc
        
        elif value == 11:  ## Mes de NOVIEMBRE
            #g11 = df_pu_pi_agg_function(df_por_mes, 'Mes_11')
            g11_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_11')
            return g11_acc
        
        elif value == 12:  ## Mes de DICIEMBRE
            #g12 = df_pu_pi_agg_function(df_por_mes, 'Mes_12')
            g12_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_12')
            return g12_acc
        
    else:
        
        if value == 1:
            #g1 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_1', productos_1)
            g11 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_1', productos_1)
            return g11
        elif value == 2:
            #g2 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_2', productos_1)
            g22 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_2', productos_1)
            return g22
        elif value == 3:
            #g3 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_3', productos_1)
            g33 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_3', productos_1)
            return g33
        elif value == 4:
            #g4 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_4', productos_1)
            g44 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_4', productos_1)
            return g44
        elif value == 5:
            #g5 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_5', productos_1)
            g55 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_5', productos_1)
            return g55
        elif value == 6:
            #g6 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_6', productos_1)
            g66 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_6', productos_1)
            return g66
        elif value == 7:
            #g7 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_7', productos_1)
            g77 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_7', productos_1)
            return g77
        elif value == 8:
            #g8 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_8', productos_1)
            g88 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_8', productos_1)
            return g88
        elif value == 9:
            #g9 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_9', productos_1)
            g99 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_9', productos_1)
            return g99
        elif value == 10:
            #g10 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_10', productos_1)
            g100 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_10', productos_1)
            return g100
        elif value == 11:
            #g11 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_11', productos_1)
            g110 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_11', productos_1)
            return g110
        elif value == 12:
            #g12 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_12', productos_1)
            g120 = sunburst_prod_standalone_agg_vu(df_acumulado_por_mes, 'Mes_12', productos_1)
            return g120                                         







                                          
# PRIMA COMPARATIVA DIPENDENTE                                          
                                          
                                          
@app.callback(
      Output('compare_p1', 'figure'),
           
      [Input('annata_compare', 'value'),
        Input('producto_dropdown_standalone_CU_p1', 'value'),
      
      
      
])                                             
                                              
def comparar_dos_p1(value, productos_1):
    if productos_1 == 'Todos':
        
        
        
        
        # Funcion para obtener la agrupacion mes por mes
        def df_pu_pi_agg_function(df, mes):
            
            filtro1 = df.get(mes)[df.get(mes).PROMOV.isin(['PU', 'CA',
                                      'AE', 'EE', 'EI',
                                      'PI'])].query('RAZMOV == "CU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':'sum'})
                    
            fig = px.sunburst(filtro1.reset_index(), path=['PRODUCTO', 'FONDO'], values='IMPORT', 
                              title=f'Importes por Producto y Fondo (CU) en el {mes}',
                              width=800, height=600, color_continuous_scale='Reds',
                              color_continuous_midpoint=0,  range_color=[0, filtro1['IMPORT'].max()])
            
            return fig
        
        
        if value == 1: ## Mes de ENERO
            #g1 = df_pu_pi_agg_function(df_por_mes, 'Mes_1')
            g1_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_1')
            return g1_acc
            
        elif value == 2:  ## Mes de FEBRERO
            #g2 = df_pu_pi_agg_function(df_por_mes, 'Mes_2')
            g2_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_2')
            return g2_acc
        
        elif value == 3:  ## Mes de MARZO
            #g3 = df_pu_pi_agg_function(df_por_mes, 'Mes_3')
            g3_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_3')
            return g3_acc
        
        elif value == 4:  ## Mes de ABRIL
            #g4 = df_pu_pi_agg_function(df_por_mes, 'Mes_4')
            g4_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_4')
            return g4_acc
        
        elif value == 5:  ## Mes de MAYO
            #g5 = df_pu_pi_agg_function(df_por_mes, 'Mes_5')
            g5_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_5')
            return g5_acc
        
        elif value == 6:  ## Mes de JUNIO
            #g6 = df_pu_pi_agg_function(df_por_mes, 'Mes_6')
            g6_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_6')
            return g6_acc
        
        elif value == 7:  ## Mes de JULIO
            #g7 = df_pu_pi_agg_function(df_por_mes, 'Mes_7')
            g7_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_7')
            return g7_acc
        
        elif value == 8:  ## Mes de AGOSTO
            #g8 = df_pu_pi_agg_function(df_por_mes, 'Mes_8')
            g8_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_8')
            return g8_acc
        
        elif value == 9:  ## Mes de SEPTIEMBRE
            #g9 = df_pu_pi_agg_function(df_por_mes, 'Mes_9')
            g9_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_9')
            return g9_acc
        
        elif value == 10:  ## Mes de OCTUBRE
            #g10 = df_pu_pi_agg_function(df_por_mes, 'Mes_10')
            g10_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_10')
            return g10_acc
        
        elif value == 11:  ## Mes de NOVIEMBRE
            #g11 = df_pu_pi_agg_function(df_por_mes, 'Mes_11')
            g11_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_11')
            return g11_acc
        
        elif value == 12:  ## Mes de DICIEMBRE
            #g12 = df_pu_pi_agg_function(df_por_mes, 'Mes_12')
            g12_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_12')
            return g12_acc
        
    else:
        
        if value == 1:
            #g1 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_1', productos_1)
            g11 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_1', productos_1)
            return g11
        elif value == 2:
            #g2 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_2', productos_1)
            g22 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_2', productos_1)
            return g22
        elif value == 3:
            #g3 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_3', productos_1)
            g33 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_3', productos_1)
            return g33
        elif value == 4:
            #g4 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_4', productos_1)
            g44 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_4', productos_1)
            return g44
        elif value == 5:
            #g5 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_5', productos_1)
            g55 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_5', productos_1)
            return g55
        elif value == 6:
            #g6 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_6', productos_1)
            g66 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_6', productos_1)
            return g66
        elif value == 7:
            #g7 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_7', productos_1)
            g77 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_7', productos_1)
            return g77
        elif value == 8:
            #g8 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_8', productos_1)
            g88 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_8', productos_1)
            return g88
        elif value == 9:
            #g9 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_9', productos_1)
            g99 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_9', productos_1)
            return g99
        elif value == 10:
            #g10 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_10', productos_1)
            g100 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_10', productos_1)
            return g100
        elif value == 11:
            #g11 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_11', productos_1)
            g110 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_11', productos_1)
            return g110
        elif value == 12:
            #g12 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_12', productos_1)
            g120 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_12', productos_1)
            return g120                                              
                                          
                                          
                                          
# SEGUNGA COMPARATIVA INDIPENDENTE

@app.callback(
    
    Output('compare_p2', 'figure'),
    
    [Input('annata_compare', 'value'),
    Input('producto_dropdown_standalone_CU_p2', 'value'),
    
    
])                                              
                                           
def comparar_dos_p2(value, productos_2):
    
    if productos_2 == 'Todos':
        
        def df_pu_pi_agg_function(df, mes):
            
            filtro1 = df.get(mes)[df.get(mes).PROMOV.isin(['PU', 'CA',
                                      'AE', 'EE', 'EI',
                                      'PI'])].query('RAZMOV == "CU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':sum})
                    
            fig = px.sunburst(filtro1.reset_index(), path=['PRODUCTO', 'FONDO'], values='IMPORT', 
                              title=f'Importes por Producto y Fondo (CU) en el {mes}',
                              width=800, height=600, color_continuous_scale='Reds',
                              color_continuous_midpoint=0,  range_color=[0, filtro1['IMPORT'].max()])
            
            return fig
        
        
        if value == 1: ## Mes de ENERO
            #g1 = df_pu_pi_agg_function(df_por_mes, 'Mes_1')
            g1_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_1')
            return g1_acc
            
        elif value == 2:  ## Mes de FEBRERO
            #g2 = df_pu_pi_agg_function(df_por_mes, 'Mes_2')
            g2_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_2')
            return g2_acc
        
        elif value == 3:  ## Mes de MARZO
            #g3 = df_pu_pi_agg_function(df_por_mes, 'Mes_3')
            g3_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_3')
            return g3_acc
        
        elif value == 4:  ## Mes de ABRIL
            #g4 = df_pu_pi_agg_function(df_por_mes, 'Mes_4')
            g4_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_4')
            return g4_acc
        
        elif value == 5:  ## Mes de MAYO
            #g5 = df_pu_pi_agg_function(df_por_mes, 'Mes_5')
            g5_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_5')
            return g5_acc
        
        elif value == 6:  ## Mes de JUNIO
            #g6 = df_pu_pi_agg_function(df_por_mes, 'Mes_6')
            g6_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_6')
            return g6_acc
        
        elif value == 7:  ## Mes de JULIO
            #g7 = df_pu_pi_agg_function(df_por_mes, 'Mes_7')
            g7_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_7')
            return g7_acc
        
        elif value == 8:  ## Mes de AGOSTO
            #g8 = df_pu_pi_agg_function(df_por_mes, 'Mes_8')
            g8_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_8')
            return g8_acc
        
        elif value == 9:  ## Mes de SEPTIEMBRE
            #g9 = df_pu_pi_agg_function(df_por_mes, 'Mes_9')
            g9_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_9')
            return g9_acc
        
        elif value == 10:  ## Mes de OCTUBRE
            #g10 = df_pu_pi_agg_function(df_por_mes, 'Mes_10')
            g10_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_10')
            return g10_acc
        
        elif value == 11:  ## Mes de NOVIEMBRE
            #g11 = df_pu_pi_agg_function(df_por_mes, 'Mes_11')
            g11_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_11')
            return g11_acc
        
        elif value == 12:  ## Mes de DICIEMBRE
            #g12 = df_pu_pi_agg_function(df_por_mes, 'Mes_12')
            g12_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_12')
            return g12_acc
        
        
        
    else:    
        if value == 1:
            #g1 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_1', productos_2)
            g11 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_1', productos_2)
            return g11
        elif value == 2:
            #g2 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_2', productos_1)
            g22 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_2', productos_2)
            return g22
        elif value == 3:
            #g3 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_3', productos_1)
            g33 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_3', productos_2)
            return g33
        elif value == 4:
            #g4 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_4', productos_1)
            g44 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_4', productos_2)
            return g44
        elif value == 5:
            #g5 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_5', productos_1)
            g55 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_5', productos_2)
            return g55
        elif value == 6:
            #g6 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_6', productos_1)
            g66 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_6', productos_2)
            return g66
        elif value == 7:
            #g7 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_7', productos_1)
            g77 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_7', productos_2)
            return g77
        elif value == 8:
            #g8 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_8', productos_1)
            g88 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_8', productos_2)
            return g88
        elif value == 9:
            #g9 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_9', productos_1)
            g99 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_9', productos_2)
            return g99
        elif value == 10:
            #g10 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_10', productos_1)
            g100 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_10', productos_2)
            return g100
        elif value == 11:
            #g11 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_11', productos_1)
            g110 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_11', productos_2)
            return  g110
        elif value == 12:
            #g12 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_12', productos_1)
            g120 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_12', productos_2)
            return g120                                          
                                          
                                          
# FIN COMPARATIVAS                                                                                   
                                          
                                          
                                          
                                              
@app.callback([
              Output('PRIMO_SANKEY_TT', 'figure'),
              Output('SECONDO_SANKEY_TT', 'figure'),
             Output('TERZO_SANKEY_TT', 'figure'),
          ], [Input('annata_3', 'value'),
              Input('producto_dropdown', 'value'),
              Input('traspaso_dropdown', 'value')
])
              

def zero_plot_3(value, producto_seleccionado, promov_seleccionado):
    
    if value == 1: ## Mes de ENERO
        g1 = sankey_primo_all(df_por_mes, 'Mes_1', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_1' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_1',  producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
        
    elif value == 2:  ## Mes de FEBRERO
        g1 = sankey_primo_all(df_por_mes, 'Mes_2', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_2' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_2',  producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 3:  ## Mes de MARZO
        g1 = sankey_primo_all(df_por_mes, 'Mes_3', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_3' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_3',  producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 4:  ## Mes de ABRIL
        g1 = sankey_primo_all(df_por_mes, 'Mes_4', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_4' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_4',  producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 5:  ## Mes de MAYO
        g1 = sankey_primo_all(df_por_mes, 'Mes_5', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_5' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_5',  producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 6:  ## Mes de JUNIO
        g1 = sankey_primo_all(df_por_mes, 'Mes_6', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_6' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_6',  producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 7:  ## Mes de JULIO
        g1 = sankey_primo_all(df_por_mes, 'Mes_7', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_7' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_7',  producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 8:  ## Mes de AGOSTO
        g1 = sankey_primo_all(df_por_mes, 'Mes_8', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_8',  producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_8', producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 9:  ## Mes de SEPTIEMBRE
        g1 = sankey_primo_all(df_por_mes, 'Mes_9', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_9' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_9', producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 10:  ## Mes de OCTUBRE
        g1 = sankey_primo_all(df_por_mes, 'Mes_10', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_10', producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_10', producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 11:  ## Mes de NOVIEMBRE
        g1 = sankey_primo_all(df_por_mes, 'Mes_11', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_11' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_11',  producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]
    
    elif value == 12:  ## Mes de DICIEMBRE
        g1 = sankey_primo_all(df_por_mes, 'Mes_12', producto_seleccionado, promov_seleccionado)
        g2 = sankey_secondo_all(df_por_mes, 'Mes_12' , producto_seleccionado, promov_seleccionado)
        g3 = sankey_terzo_all(df_por_mes, 'Mes_12',  producto_seleccionado, promov_seleccionado)
        return [g1, g2, g3]







                   
## Hombres
@app.callback([
    Output('gra33', 'figure'),
    Output('gra33_acumulado_por_mes', 'figure')
    ],
    [Input('annata', 'value'),
     Input('producto_dropdown_standalone_CU', 'value')
     ])

def zero_plot(value, productos_1):
    
    if productos_1 == 'Todos':
        
        
        
        # Funcion para obtener la agrupacion mes por mes
        def df_pu_pi_agg_function(df, mes):
            
            filtro1 = df.get(mes)[df.get(mes).PROMOV.isin(['PU', 'CA',
                                     'AE', 'EE', 'EI',
                                     'PI'])].query('RAZMOV == "CU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':'sum'})
                    
            fig = px.sunburst(filtro1.reset_index(), path=['PRODUCTO', 'FONDO'], values='IMPORT', 
                              title=f'Importes por Producto y Fondo (CU) en el {mes}',
                              width=800, height=600, color_continuous_scale='Reds',
                              color_continuous_midpoint=0,  range_color=[0, filtro1['IMPORT'].max()])
            
            return fig
        
        
        if value == 1: ## Mes de ENERO
            g1 = df_pu_pi_agg_function(df_por_mes, 'Mes_1')
            g1_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_1')
            return [g1, g1_acc]
            
        elif value == 2:  ## Mes de FEBRERO
            g2 = df_pu_pi_agg_function(df_por_mes, 'Mes_2')
            g2_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_2')
            return [g2, g2_acc]
        
        elif value == 3:  ## Mes de MARZO
            g3 = df_pu_pi_agg_function(df_por_mes, 'Mes_3')
            g3_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_3')
            return [g3, g3_acc]
        
        elif value == 4:  ## Mes de ABRIL
            g4 = df_pu_pi_agg_function(df_por_mes, 'Mes_4')
            g4_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_4')
            return [g4, g4_acc]
        
        elif value == 5:  ## Mes de MAYO
            g5 = df_pu_pi_agg_function(df_por_mes, 'Mes_5')
            g5_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_5')
            return [g5, g5_acc]
        
        elif value == 6:  ## Mes de JUNIO
            g6 = df_pu_pi_agg_function(df_por_mes, 'Mes_6')
            g6_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_6')
            return [g6, g6_acc]
        
        elif value == 7:  ## Mes de JULIO
            g7 = df_pu_pi_agg_function(df_por_mes, 'Mes_7')
            g7_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_7')
            return [g7, g7_acc]
        
        elif value == 8:  ## Mes de AGOSTO
            g8 = df_pu_pi_agg_function(df_por_mes, 'Mes_8')
            g8_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_8')
            return [g8, g8_acc]
        
        elif value == 9:  ## Mes de SEPTIEMBRE
            g9 = df_pu_pi_agg_function(df_por_mes, 'Mes_9')
            g9_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_9')
            return [g9, g9_acc]
        
        elif value == 10:  ## Mes de OCTUBRE
            g10 = df_pu_pi_agg_function(df_por_mes, 'Mes_10')
            g10_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_10')
            return [g10, g10_acc]
        
        elif value == 11:  ## Mes de NOVIEMBRE
            g11 = df_pu_pi_agg_function(df_por_mes, 'Mes_11')
            g11_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_11')
            return [g11, g11_acc]
        
        elif value == 12:  ## Mes de DICIEMBRE
            g12 = df_pu_pi_agg_function(df_por_mes, 'Mes_12')
            g12_acc = grafico_mes_acc_sunburst(df_acumulado_por_mes, 'Mes_12')
            return [g12, g12_acc]
        
    else:
        
        if value == 1:
            g1 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_1', productos_1)
            g11 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_1', productos_1)
            return [g1, g11]
        elif value == 2:
            g2 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_2', productos_1)
            g22 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_2', productos_1)
            return [g2, g22]
        elif value == 3:
            g3 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_3', productos_1)
            g33 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_3', productos_1)
            return [g3, g33]
        elif value == 4:
            g4 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_4', productos_1)
            g44 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_4', productos_1)
            return [g4, g44]
        elif value == 5:
            g5 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_5', productos_1)
            g55 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_5', productos_1)
            return [g5, g55]
        elif value == 6:
            g6 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_6', productos_1)
            g66 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_6', productos_1)
            return [g6, g66]
        elif value == 7:
            g7 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_7', productos_1)
            g77 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_7', productos_1)
            return [g7, g77]
        elif value == 8:
            g8 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_8', productos_1)
            g88 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_8', productos_1)
            return [g8, g88]
        elif value == 9:
            g9 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_9', productos_1)
            g99 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_9', productos_1)
            return [g9, g99]
        elif value == 10:
            g10 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_10', productos_1)
            g100 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_10', productos_1)
            return [g10, g100]
        elif value == 11:
            g11 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_11', productos_1)
            g110 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_11', productos_1)
            return [g11, g110]
        elif value == 12:
            g12 = sunburst_prod_standalone_agg(df_por_mes, 'Mes_12', productos_1)
            g120 = sunburst_prod_standalone_no(df_acumulado_por_mes, 'Mes_12', productos_1)
            return [g12, g120]
    
## VENTA DE UNIDADES POR RT Y RP

@app.callback([
    Output('gra33_2', 'figure'),
    Output('gra33_2_acumulado_por_mes', 'figure')
    ],
    [Input('annata_2', 'value'),
     Input('producto_dropdown_standalone_VU', 'value')
])

def zero_plot_2(value, productos_1):
    
    if productos_1 == 'Todos':
        
        # Funcion para obtener la agrupacion mes por mes
        
        def df_rt_rp_agg_function(df, mes):
            
            filtro2 = df.get(mes)[df.get(mes).PROMOV.isin(['RT', 
                                                'RP'])].query('RAZMOV == "VU"').groupby(['PRODUCTO', 'FONDO']).agg({'IMPORT':'sum'})
            fig = px.sunburst(filtro2.reset_index(), path=['PRODUCTO', 'FONDO'], values='IMPORT', 
                              title=f'Importes por Producto y Fondo (VU) en el {mes}',
                              width=800, height=600, color_continuous_scale='Reds',
                              color_continuous_midpoint=0,  range_color=[0, filtro2['IMPORT'].max()])
                
            return fig
        
        
        if value == 1: ## Mes de ENERO
            g1 = df_rt_rp_agg_function(df_por_mes, 'Mes_1')
            g1_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_1')
            return [g1, g1_acc]
            
        elif value == 2:  ## Mes de FEBRERO
            g2 = df_rt_rp_agg_function(df_por_mes, 'Mes_2')
            g2_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_2')
            return [g2, g2_acc]
        
        elif value == 3:  ## Mes de MARZO
            g3 = df_rt_rp_agg_function(df_por_mes, 'Mes_3')
            g3_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_3')
            return [g3, g3_acc]
        
        elif value == 4:  ## Mes de ABRIL
            g4 = df_rt_rp_agg_function(df_por_mes, 'Mes_4')
            g4_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_4')
            return [g4, g4_acc]
        
        elif value == 5:  ## Mes de MAYO
            g5 = df_rt_rp_agg_function(df_por_mes, 'Mes_5')
            g5_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_5')
            return [g5, g5_acc]
        
        elif value == 6:  ## Mes de JUNIO
            g6 = df_rt_rp_agg_function(df_por_mes, 'Mes_6')
            g6_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_6')
            return [g6, g6_acc]
        
        elif value == 7:  ## Mes de JULIO
            g7 = df_rt_rp_agg_function(df_por_mes, 'Mes_7')
            g7_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_7')
            return [g7, g7_acc]
        
        elif value == 8:  ## Mes de AGOSTO
            g8 = df_rt_rp_agg_function(df_por_mes, 'Mes_8')
            g8_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_8')
            return [g8, g8_acc]
        
        elif value == 9:  ## Mes de SEPTIEMBRE
            g9 = df_rt_rp_agg_function(df_por_mes, 'Mes_9')
            g9_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_9')
            return [g9, g9_acc]
        
        elif value == 10:  ## Mes de OCTUBRE
            g10 = df_rt_rp_agg_function(df_por_mes, 'Mes_10')
            g10_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_10')
            return [g10, g10_acc]
        
        elif value == 11:  ## Mes de NOVIEMBRE
            g11 = df_rt_rp_agg_function(df_por_mes, 'Mes_11')
            g11_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_11')
            return [g11, g11_acc]
        
        elif value == 12:  ## Mes de DICIEMBRE
            g12 = df_rt_rp_agg_function(df_por_mes, 'Mes_12')
            g12_acc = grafico_mes_acc_sunburst_rp_rt(df_acumulado_por_mes, 'Mes_12')
            return [g12, g12_acc]

    else:
        
        if value == 1:
            g1 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_1', productos_1)
            g11 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_1', productos_1)
            return [g1, g11]
        elif value == 2:
            g2 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_2', productos_1)
            g22 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_2', productos_1)
            return [g2, g22]
        elif value == 3:
            g3 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_3', productos_1)
            g33 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_3', productos_1)
            return [g3, g33]
        elif value == 4:
            g4 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_4', productos_1)
            g44 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_4', productos_1)
            return [g4, g44]
        elif value == 5:
            g5 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_5', productos_1)
            g55 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_5', productos_1)
            return [g5, g55]
        elif value == 6:
            g6 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_6', productos_1)
            g66 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_6', productos_1)
            return [g6, g66]
        elif value == 7:
            g7 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_7', productos_1)
            g77 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_7', productos_1)
            return [g7, g77]
        elif value == 8:
            g8 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_8', productos_1)
            g88 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_8', productos_1)
            return [g8, g88]
        elif value == 9:
            g9 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_9', productos_1)
            g99 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_9', productos_1)
            return [g9, g99]
        elif value == 10:
            g10 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_10', productos_1)
            g100 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_10', productos_1)
            return [g10, g100]
        elif value == 11:
            g11 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_11', productos_1)
            g110 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_11', productos_1)
            return [g11, g110]
        elif value == 12:
            g12 = sunburst_prod_standalone_agg_vu(df_por_mes, 'Mes_12', productos_1)
            g120 = sunburst_prod_standalone_no_vu(df_acumulado_por_mes, 'Mes_12', productos_1)
            return [g12, g120]




host = 'localhost'
port = 8049


# ### EXPORTANDO ARCHIVOS EXCEL
# data_results = "Resultado_cierre"
# ruta_carpeta = os.path.join(os.path.dirname(__file__), data_results)  
# if not os.path.exists(ruta_carpeta):
#     os.makedirs(ruta_carpeta)

# print('Exportando Resultados en formato CSV en la siguiente carpeta: ', data_results)










print("Para visualizar la Herramienta de Cierre clicar ctrl +",
      host, "8049 que aparece en el terminal (cmd) de windows que aparece a continuación.")

if __name__ == '__main__':
    app.run_server(host=host, port=port,debug=True)



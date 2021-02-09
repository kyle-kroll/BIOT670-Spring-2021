'''
    BIOT670 Capstone Project - Quad Viewer
    plotting functions
'''
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
choices = ['DB_CORO_MEAN', 'HET_CORO_MEAN', 'KOHET_CORO_MEAN', 'KOKO_CORO_MEAN']
'''
xpos = 'DB_CORO_MEAN'
ypos = 'HET_CORO_MEAN'
xneg = 'KOHET_CORO_MEAN'
yneg = 'KOKO_CORO_MEAN'
'''
df = pd.read_csv('coro_data.tsv', sep='\t')

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        #figure=fig,
        clear_on_unhover=True
    ),
    html.Div(
        className="row", children=[

            html.Div(className='six columns', children=[
                html.Label('Positive X'),
                dcc.Dropdown(
                    id="xpos-dropdown",
                    options=[{'label': name, 'value': name} for name in choices],
                    value=choices[0],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='25%')),
            html.Div(className='six columns', children=[
                html.Label('Positive Y'),
                dcc.Dropdown(
                    id="ypos-dropdown",
                    options=[{'label': name, 'value': name} for name in choices],
                    value=choices[0],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='25%')),
            html.Div(className='six columns', children=[
                html.Label('Negative X'),
                dcc.Dropdown(
                    id="xneg-dropdown",
                    options=[{'label': name, 'value': name} for name in choices],
                    value=choices[0],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='25%')),
            html.Div(className='six columns', children=[
                html.Label('Negative Y'),
                dcc.Dropdown(
                    id="yneg-dropdown",
                    options=[{'label': name, 'value': name} for name in choices],
                    value=choices[0],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='25%'))
        ], style=dict(display='flex')),
    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns')
    ])
])

@app.callback(
Output('basic-interactions', 'figure'),
[Input('xpos-dropdown', 'value'),
 Input('ypos-dropdown', 'value'),
 Input('xneg-dropdown', 'value'),
 Input('yneg-dropdown', 'value')])
def create_figure(xpos, ypos, xneg, yneg):
    dff = df
    fig = go.Figure()
    fig.add_scatter(x=dff[xpos],
                    y=dff[ypos],
                    mode='markers',
                    marker_color='blue',
                    text=dff['Accession_Number'])
    fig.add_scatter(x=dff[xneg].apply(lambda x: x * -1),
                    y=dff[ypos],
                    mode='markers',
                    marker_color='blue',
                    text=dff['Accession_Number'])
    fig.add_scatter(x=dff[xneg].apply(lambda x: x * -1),
                    y=dff[yneg].apply(lambda x: x * -1),
                    mode='markers',
                    marker_color='blue',
                    text=dff['Accession_Number'])
    fig.add_scatter(x=dff[xpos],
                    y=dff[yneg].apply(lambda x: x * -1),
                    mode='markers',
                    marker_color='blue',
                    text=dff['Accession_Number'])
    fig.update_layout(height=500, showlegend=False)
    return fig

@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData'),
     Input('xpos-dropdown', 'value'),
     Input('ypos-dropdown', 'value'),
     Input('xneg-dropdown', 'value'),
     Input('yneg-dropdown', 'value')
     ])
def display_hover_data(hoverData, xpos, ypos, xneg, yneg):
    name = hoverData['points'][0]['text']
    path = df.loc[df['Accession_Number'] == name, 'All_Pathways'].values[0]
    xpos_val = df.loc[df['Accession_Number'] == name, xpos].values[0]
    ypos_val = df.loc[df['Accession_Number'] == name, ypos].values[0]
    xneg_val = df.loc[df['Accession_Number'] == name, xneg].values[0]
    yneg_val = df.loc[df['Accession_Number'] == name, yneg].values[0]
    blah = f'Protein:\t{name}\nPathways:\t{path}\n{xpos}:\t{xpos_val}\n{ypos}:\t{ypos_val}\n{xneg}:\t{xneg_val}\n{yneg}:\t{yneg_val}'
    return blah


if __name__ == '__main__':
    app.run_server(debug=False)

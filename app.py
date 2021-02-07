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

xpos = 'DB_CORO_MEAN'
ypos = 'HET_CORO_MEAN'
xneg = 'KOHET_CORO_MEAN'
yneg = 'KOKO_CORO_MEAN'
df = pd.read_csv('coro_data.tsv', sep='\t')
df[xpos] = df[xpos].apply(lambda x: x)
df[ypos] = df[ypos].apply(lambda x: x)

fig = go.Figure()
fig.add_scatter(x=df[xpos],
                y=df[ypos],
                mode='markers',
                marker_color='blue',
                text=df['Accession_Number'])
fig.add_scatter(x=df[xneg].apply(lambda x: x * -1),
                y=df[ypos],
                mode='markers',
                marker_color='blue',
                text=df['Accession_Number'])
fig.add_scatter(x=df[xneg].apply(lambda x: x * -1),
                y=df[yneg].apply(lambda x: x * -1),
                mode='markers',
                marker_color='blue',
                text=df['Accession_Number'])
fig.add_scatter(x=df[xpos],
                y=df[yneg].apply(lambda x: x * -1),
                mode='markers',
                marker_color='blue',
                text=df['Accession_Number'])
fig.update_layout(height=500, showlegend=False)
app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig,
        clear_on_unhover=True
    ),

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
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    name = hoverData['points'][0]['text']
    path = df.loc[df['Accession_Number'] == name, 'All_Pathways'].values[0]
    xpos_val = df.loc[df['Accession_Number'] == name, xpos].values[0]
    ypos_val = df.loc[df['Accession_Number'] == name, ypos].values[0]
    xneg_val = df.loc[df['Accession_Number'] == name, xneg].values[0]
    yneg_val = df.loc[df['Accession_Number'] == name, yneg].values[0]
    blah = f'Protein:\t{name}\nPathways:\t{path}\n{xpos}:\t{xpos_val}\n{ypos}:\t{ypos_val}\n{xneg}:\t{xneg_val}\n{yneg}:\t{yneg_val}'
    return blah


if __name__ == '__main__':
    app.run_server(debug=True)

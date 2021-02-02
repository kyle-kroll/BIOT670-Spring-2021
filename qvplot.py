'''
    BIOT670 Capstone Project - Quad Viewer
    plotting functions
'''
import math

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go


app = dash.Dash(__name__)
df = pd.read_csv('het_coro_aorta.tsv', sep='\t')
df['Mean HET_AORTA'] = df['Mean HET_AORTA'].apply(lambda x: math.log2(x+1))
df['Mean HET_CORO'] = df['Mean HET_CORO'].apply(lambda x: math.log2(x+1))
df['NEG Mean HET_AORTA'] = df['Mean HET_AORTA'].apply(lambda x: x*-1)
df['NEG Mean HET_CORO'] = df['Mean HET_CORO'].apply(lambda x: x*-1)
fig = go.Figure()
fig.add_scatter(x=df['Mean HET_AORTA'],
                y=df['Mean HET_CORO'],
                mode='markers',
                fillcolor='blue',
                text=df['Accession_Number'])
fig.add_scatter(x=df['NEG Mean HET_AORTA'],
                y=df['Mean HET_CORO'],
                mode='markers',
                fillcolor='blue',
                text=df['Accession_Number'])
fig.add_scatter(x=df['NEG Mean HET_AORTA'],
                y=df['NEG Mean HET_CORO'],
                mode='markers',
                fillcolor='blue',
                text=df['Accession_Number'])
fig.add_scatter(x=df['Mean HET_AORTA'],
                y=df['NEG Mean HET_CORO'],
                mode='markers',
                fillcolor='blue',
                text=df['Accession_Number'])
fig.update_layout(height=700)
app.layout = html.Div([
    dcc.Graph(
        id='graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)
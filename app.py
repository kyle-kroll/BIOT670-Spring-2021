'''
    BIOT670 Capstone Project - Quad Viewer
    plotting functions
'''
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import math

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Declare a global dataframe to hold the uploaded information
df = pd.DataFrame()


def serve_layout():
    layout = html.Div([
        # The following dbc.Row contains the 2 column layout where settings are on the left
        # and the plot is the column to the right

        dbc.Row([
            dbc.Col([
                html.Div(className='six columns', children=[
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=False
                    ),
                    html.Div(id='output-data-upload'),
                    html.Div(id='dropdown-items'),
                    html.Label('Plot Axis Scale'),
                    html.Div(children=[
                        dcc.RadioItems(
                            id='scale-radio',
                            options=[
                                {'label': 'Linear', 'value': 'lin'},
                                {'label': 'Log10', 'value': 'log'}
                            ],
                            value='lin',
                            labelStyle={'display': 'block'}
                        )]),
                ])
            ], width={"size": 2}

            ),
            # Figure plot
            dbc.Col(
                html.Div(className='six columns', children=[
                    dcc.Graph(
                        id='basic-interactions',
                        clear_on_unhover=True,
                        config={
                            'toImageButtonOptions': {
                                'format': 'svg',  # one of png, svg, jpeg, webp
                                'filename': 'custom_image',
                                'height': 800,
                                'width': 800,
                                'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
                            }
                        }
                    )
                ])
            )
            # Second row is for the hover data which only has a single, centered column
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Markdown("""
                                    **Hover Data**
                            
                                    Mouse over values in the graph.
                                """),
                    html.Pre(id='hover-data')
                ])
            ], width={"size": 6, "offset": 3})
        ])
    ])
    return layout


app.layout = serve_layout


# Parse uploaded data function
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    global df
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'tsv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode(('utf-8'))),
                sep='\t'
            )
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


# Callback for handling uploaded data
@app.callback(Output('dropdown-items', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        parse_contents(list_of_contents, list_of_names, list_of_dates)
    return [
        html.Label('Positive X'),
        dcc.Dropdown(
            id="xpos-dropdown",
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=False,
        ),
        html.Label('Positive Y'),
        dcc.Dropdown(
            id="ypos-dropdown",
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=False,
        ),
        html.Label('Negative X'),
        dcc.Dropdown(
            id="xneg-dropdown",
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=False,
        ),
        html.Label('Negative Y'),
        dcc.Dropdown(
            id="yneg-dropdown",
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=False,
        )
    ]


@app.callback(
    Output('basic-interactions', 'figure'),
    [Input('xpos-dropdown', 'value'),
     Input('ypos-dropdown', 'value'),
     Input('xneg-dropdown', 'value'),
     Input('yneg-dropdown', 'value'),
     Input('scale-radio', 'value'),
     State('basic-interactions', 'figure')])
def create_figure(xpos, ypos, xneg, yneg, scale, state):
    global df
    fig = go.Figure()
    if None not in [xpos, ypos]:
        fig.add_scatter(x=df[xpos] if scale == 'lin' else df[xpos].apply(lambda x: math.log10(x + 1)),
                        y=df[ypos] if scale == 'lin' else df[ypos].apply(lambda x: math.log10(x + 1)),
                        mode='markers',
                        marker_color='blue',
                        text=df['Accession_Number'],
                        name="Quadrant 1")
    if None not in [xneg, ypos]:
        fig.add_scatter(
            x=df[xneg].apply(lambda x: x * -1) if scale == 'lin' else df[xneg].apply(lambda x: math.log10(x + 1) * -1),
            y=df[ypos] if scale == 'lin' else df[ypos].apply(lambda x: math.log10(x + 1)),
            mode='markers',
            marker_color='blue',
            text=df['Accession_Number'],
            name="Quadrant 2")
    if None not in [xneg, yneg]:
        fig.add_scatter(
            x=df[xneg].apply(lambda x: x * -1) if scale == 'lin' else df[xneg].apply(lambda x: math.log10(x + 1) * -1),
            y=df[yneg].apply(lambda x: x * -1) if scale == 'lin' else df[yneg].apply(lambda x: math.log10(x + 1) * -1),
            mode='markers',
            marker_color='blue',
            text=df['Accession_Number'],
            name="Quadrant 3")
    if None not in [xpos, yneg]:
        fig.add_scatter(x=df[xpos] if scale == 'lin' else df[xpos].apply(lambda x: math.log10(x + 1)),
                        y=df[yneg].apply(lambda x: x * -1) if scale == 'lin' else df[yneg].apply(
                            lambda x: math.log10(x + 1) * -1),
                        mode='markers',
                        marker_color='blue',
                        text=df['Accession_Number'],
                        name="Quadrant 4")
    fig.update_layout(showlegend=False,
                      xaxis_title=f"\u2190{xneg}-----{xpos}\u2192",
                      yaxis_title=f"\u2190{yneg}-----{ypos}\u2192",
                      title={
                            'text': ypos,
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    return fig


@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData'),
     Input('xpos-dropdown', 'value'),
     Input('ypos-dropdown', 'value'),
     Input('xneg-dropdown', 'value'),
     Input('yneg-dropdown', 'value'),
     State('xpos-dropdown', 'value')]
)
def display_hover_data(hoverData, xpos, ypos, xneg, yneg, state):
    if hoverData is not None:
        global df
        name = hoverData['points'][0]['text']
        path = df.loc[df['Accession_Number'] == name, 'All_Pathways'].values[0]
        output_dict = {}
        if xpos is not None:
            output_dict[xpos] = df.loc[df['Accession_Number'] == name, xpos].values[0]
        if ypos is not None:
            output_dict[ypos] = df.loc[df['Accession_Number'] == name, ypos].values[0]
        if xneg is not None:
            output_dict[xneg] = df.loc[df['Accession_Number'] == name, xneg].values[0]
        if yneg is not None:
            output_dict[yneg] = df.loc[df['Accession_Number'] == name, yneg].values[0]
        blah = f'Protein:\t{name}\nPathways:\t{path}\n' + ''.join(
            f'{k}:\t{output_dict[k]}\n' for k in output_dict.keys())
        return blah


if __name__ == '__main__':
    app.run_server(debug=False)

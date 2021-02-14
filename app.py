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
import plotly
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import math
import numpy as np

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

# Color dictionary - Mary
#Dicitonary for colors of pathways
color_dict={'Integrin':'limegreen',
            'Blood_Coagulation':'firebrick',
            'Cytoskeleton':'orangered',
            'Chemokine_Cytokine_Signaling':'tomato',
            'Chemokine_Cytokine_Signaling, Cytoskeleton':'royalblue',
            'Chemokine_Cytokine_Signaling, Cytoskeleton, Integrin':'seagreen',
            'Chemokine_Cytokine_Signaling, Cytoskeleton, Huntington':'wheat',
            'Chemokine_Cytokine_Signaling, Huntington, Integrin':'yellowgreen',
            'Chemokine_Cytokine_Signaling, Cytoskeleton, Huntington, Integrin':'violet',
            'Huntington, Integrin':'crimson',
            'Parkinson':'lightseagreen',
            'Cytoskeleton, Huntington':'aqua',
            'Chemokine_Cytokine_Signaling, Integrin':'palegreen',
            'Glycolysis, Huntington':'chocolate',
            'ATP_Synthesis':'brown',
            'ATP_Synthesis, Huntington':'burlywood',
            'Glycolysis':'mediumvioletred',
            'Glycolysis, Pyruvate_Metabolism':'cadetblue',
            'Huntington':'goldenrod',
            'Pyruvate_Metabolism':'darkkhaki',
            'Pyruvate_Metabolism, TCA_Cycle':'sienna',
            'TCA_Cycle':'darkred',
            'De_Novo_Purine_Biosynthesis':'mediumpurple',
            'None':'slategray'}

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
                    html.Div(id='file-name'),
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
                                'height': 1080,
                                'width': 1920,
                                'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
                            },

                        },

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

# Create pie chart for every row in data frame
colour_column = 'All_Pathways'


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
                io.StringIO(decoded.decode('utf-8')),
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
    df = df.replace(np.nan, 'None', regex=True)


# Callback for handling uploaded data
# After data uploaded it is parsed into global df item and then populates the columns for dropdowns 
@app.callback(Output('file-name', 'children'),
              Output('dropdown-items', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        parse_contents(list_of_contents, list_of_names, list_of_dates)
    return [html.Label(f"File: {list_of_names}"),(
        html.Label('Row names'),
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=True
        ),
        html.Label('Color by:'),
        dcc.Dropdown(
            id='colour-dropdown',
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=True
        ),
        html.Label('Positive X'),
        dcc.Dropdown(
            id="xpos-dropdown",
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=True,
        ),
        html.Label('Positive Y'),
        dcc.Dropdown(
            id="ypos-dropdown",
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=True,
        ),
        html.Label('Negative X'),
        dcc.Dropdown(
            id="xneg-dropdown",
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=True,
        ),
        html.Label('Negative Y'),
        dcc.Dropdown(
            id="yneg-dropdown",
            options=[{'label': name, 'value': name} for name in df.columns],
            clearable=False,
            searchable=True,
        ))
    ]


# After selecting columns to plot, create those traces
@app.callback(
    Output('basic-interactions', 'figure'),
    [Input('xpos-dropdown', 'value'),
     Input('ypos-dropdown', 'value'),
     Input('xneg-dropdown', 'value'),
     Input('yneg-dropdown', 'value'),
     Input('scale-radio', 'value'),
     Input('name-dropdown', 'value'),
     Input('colour-dropdown', 'value'),
     State('basic-interactions', 'figure')])
def create_figure(xpos, ypos, xneg, yneg, scale, name, colour_by, state):
    global df
    data = []
    if None not in [xpos, ypos]:
        data.append(go.Scatter(x=df[xpos] if scale == 'lin' else df[xpos].apply(lambda x: math.log10(x + 1)),
                        y=df[ypos] if scale == 'lin' else df[ypos].apply(lambda x: math.log10(x + 1)),
                        mode='markers',
                        #marker_color=[color_dict[k] for k in df[colour_by].values],
                        marker_color="blue",
                        text=df[name],
                        name="Quadrant 1",
                        showlegend=False))
    if None not in [xneg, ypos]:
        data.append(go.Scatter(
            x=df[xneg].apply(lambda x: x * -1) if scale == 'lin' else df[xneg].apply(lambda x: math.log10(x + 1) * -1),
            y=df[ypos] if scale == 'lin' else df[ypos].apply(lambda x: math.log10(x + 1)),
            mode='markers',
            # marker_color=[color_dict[k] for k in df[colour_by].values],
            marker_color="blue",
            text=df[name],
            name="Quadrant 2",
            showlegend=False))
    if None not in [xneg, yneg]:
        data.append(go.Scatter(
            x=df[xneg].apply(lambda x: x * -1) if scale == 'lin' else df[xneg].apply(lambda x: math.log10(x + 1) * -1),
            y=df[yneg].apply(lambda x: x * -1) if scale == 'lin' else df[yneg].apply(lambda x: math.log10(x + 1) * -1),
            mode='markers',
            # marker_color=[color_dict[k] for k in df[colour_by].values],
            marker_color="blue",
            text=df[name],
            name="Quadrant 3",
            showlegend=False))
    if None not in [xpos, yneg]:
        data.append(go.Scatter(x=df[xpos] if scale == 'lin' else df[xpos].apply(lambda x: math.log10(x + 1)),
                        y=df[yneg].apply(lambda x: x * -1) if scale == 'lin' else df[yneg].apply(
                            lambda x: math.log10(x + 1) * -1),
                        mode='markers',
                        #marker_color=[color_dict[k] for k in df[colour_by].values],
                        marker_color="blue",
                        text=df[name],
                        name="Quadrant 4",
                        showlegend=False))

    # Add in axis labels
    if len(data) > 0:
        fig = go.Figure(data=data)
        '''for k in color_dict.keys():
        fig.add_scatter(x=[None], y=[None], mode='markers',
                            marker=dict(size=10, color=plotly.colors.qualitative.Dark24),
                            legendgroup='Markers', showlegend=True, name=colour_by)'''
        fig.add_hline(y=0)
        fig.add_vline(x=0)
        fig.update_layout(
                          showlegend=True,
                          xaxis_title=f"\u2190{xneg}-----{xpos}\u2192",
                          yaxis_title=f"\u2190{yneg}-----{ypos}\u2192",
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)')
        return fig
    else:
        return go.Figure()


# Format and display hover data in a table below the graph
@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData'),
     Input('xpos-dropdown', 'value'),
     Input('ypos-dropdown', 'value'),
     Input('xneg-dropdown', 'value'),
     Input('yneg-dropdown', 'value'),
     Input('name-dropdown', 'value'),
     Input('colour-dropdown', 'value'),
     State('xpos-dropdown', 'value')])
def display_hover_data(hoverData, xpos, ypos, xneg, yneg, row_name, pathways, state):
    if hoverData is not None:
        global df
        name = hoverData['points'][0]['text']
        if pathways is not None:
            path = df.loc[df[row_name] == name, pathways].values[0]
        else:
            path = "NA"
        output_dict = {}
        if xpos is not None:
            output_dict[xpos] = df.loc[df[row_name] == name, xpos].values[0]
        if ypos is not None:
            output_dict[ypos] = df.loc[df[row_name] == name, ypos].values[0]
        if xneg is not None:
            output_dict[xneg] = df.loc[df[row_name] == name, xneg].values[0]
        if yneg is not None:
            output_dict[yneg] = df.loc[df[row_name] == name, yneg].values[0]
        blah = f'Protein:\t{name}\nColoured by:\t{path}\n' + ''.join(
            f'{k}:\t{output_dict[k]}\n' for k in output_dict.keys())
        return blah


if __name__ == '__main__':
    app.run_server(debug=False)

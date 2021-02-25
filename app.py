'''
    BIOT670 Capstone Project - Quad Viewer
    plotting functions
'''
import json
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
import plotly.express as px

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
files = {}

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
                            html.Button('Click Here to Select File(s)')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=True
                    ),
                    html.Div(id='file-selector'),
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
                                'height': 800,
                                'width': 800,
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
    files[filename] = df.to_dict()


# Callback for handling uploaded data
# After data uploaded it is parsed into global df item and then populates the columns for dropdowns 
@app.callback(Output('file-selector', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        return (
            dcc.Dropdown(
                id='file-dropdown',
                options=[{'label': file, 'value': file} for file in list_of_names],
                clearable=False,
                searchable=True,
                placeholder='Please Select Your File'
            ))


@app.callback(Output('file-name', 'children'),
              Output('dropdown-items', 'children'),
              Input('file-dropdown', 'value'))
def drop_down_updates(file_name):
    global df
    if file_name is not None:
        df = pd.DataFrame.from_dict(files[file_name])

    return [html.Label(f"File: {file_name}"), (
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
    fig = go.Figure()
    fig.update_layout(height=600, width=600, autosize=False)
    if None not in [xpos, ypos, xneg, yneg]:
        # Create a figure for each quadrant
        fig1 = px.scatter(df, x=xpos, y=ypos, color=colour_by, custom_data=[name],
                          hover_data={
                              xpos:False,
                              ypos:False,
                              colour_by: False,
                              name: True
                            })
        fig2 = px.scatter(df, x=xneg, y=ypos, color=colour_by, custom_data=[name],
                          hover_data={
                              xpos: False,
                              ypos: False,
                              colour_by: False,
                              name: True
                          })
        fig2.update_layout(showlegend=False)
        fig3 = px.scatter(df, x=xneg, y=yneg, color=colour_by, custom_data=[name],
                          hover_data={
                              xpos: False,
                              ypos: False,
                              colour_by: False,
                              name: True
                          })
        fig3.update_layout(showlegend=False)
        fig4 = px.scatter(df, x=xpos, y=yneg, color=colour_by, custom_data=[name],
                          hover_data={
                              xpos: False,
                              ypos: False,
                              colour_by: False,
                              name: True
                          })
        fig4.update_layout(showlegend=False)

        # Set negative columns to negative values
        for sc in fig2['data']:
            sc['x'] = sc['x'] * -1
        for sc in fig3['data']:
            sc['x'] = sc['x'] * -1
            sc['y'] = sc['y'] * -1
        for sc in fig4['data']:
            sc['y'] = sc['y'] * -1
        # Find the maximum value from any column and round to neared 100
        max_val = max(np.concatenate([np.concatenate([abs(sc['x']) for sc in fig1['data']]),
                                      np.concatenate([abs(sc['y']) for sc in fig1['data']]),
                                      np.concatenate([abs(sc['x']) for sc in fig2['data']]),
                                      np.concatenate([abs(sc['y']) for sc in fig2['data']]),
                                      np.concatenate([abs(sc['x']) for sc in fig3['data']]),
                                      np.concatenate([abs(sc['y']) for sc in fig3['data']]),
                                      np.concatenate([abs(sc['x']) for sc in fig4['data']]),
                                      np.concatenate([abs(sc['y']) for sc in fig4['data']])]))
        axis_max = int(round(float(max_val) / 100) * 100)

        # Create the final figure with new axis limits
        fig = go.Figure(data=fig1.data + fig2.data + fig3.data + fig4.data,
                         layout_xaxis_range=[axis_max * -1, axis_max],
                         layout_yaxis_range=[axis_max * -1, axis_max])

        # Update the axis ticks so they don't show negative values
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=np.concatenate([list(range(axis_max * -1, 1, 100)), list(range(0, axis_max + 1, 100))]),
                ticktext=np.concatenate(
                    [[x * -1 for x in list(range(axis_max * -1, 1, 100))], list(range(0, axis_max + 1, 100))])
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=np.concatenate([list(range(axis_max * -1, 1, 100)), list(range(0, axis_max + 1, 100))]),
                ticktext=np.concatenate(
                    [[x * -1 for x in list(range(axis_max * -1, 1, 100))], list(range(0, axis_max + 1, 100))])
            ),
            width=600,
            height=600, showlegend=False
        )

    # Add in axis labels

    fig.add_hline(y=0)
    fig.add_vline(x=0)
    fig.update_layout(

                      xaxis_title=f"\u2190{xneg}-----{xpos}\u2192",
                      yaxis_title=f"\u2190{yneg}-----{ypos}\u2192",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
    return fig



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
        name = hoverData['points'][0]['customdata'][0]
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
        #return json.dumps(hoverData, indent=4)


if __name__ == '__main__':
    app.run_server(debug=False)

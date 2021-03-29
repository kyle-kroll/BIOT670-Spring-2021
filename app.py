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
from dash.dependencies import Input, Output, State
from uiutils import update_dropdowns, serve_layout
from plotutils import generate_plot, generate_plot_data
import numpy as np
import plotly.graph_objects as go

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
files = {}
fig = go.Figure()
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


# After the user selects a dataset after uploading, populate the various dropdowns
@app.callback(Output('file-name', 'children'),
              Output('dropdown-items', 'children'),
              Input('file-dropdown', 'value'))
def drop_down_updates(file_name):
    global df
    if file_name is not None:
        df = pd.DataFrame.from_dict(files[file_name])
    return update_dropdowns(file_name, df)


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
     Input('basic-interactions', 'clickData'),
     Input('legend-radio', 'value'),
     Input('size_by', 'value'),
     State('basic-interactions', 'clickData')])
def create_figure(xpos, ypos, xneg, yneg, scale, name, colour_by, clickData, showLegend, size_by, state):
    global df
    # The plot_data object should be passed to generate_plot but did not have time to modify that
    # plot_data is used for drawing the trace around clicked points
    plot_data = generate_plot_data(df, xpos, ypos, xneg, yneg, scale, name, colour_by)
    fig1 = generate_plot(df, xpos, ypos, xneg, yneg, scale, name, colour_by)
    fig1.update_layout(showlegend=showLegend)
    global fig
    fig = fig1
    if size_by is not None:
        for trace in fig.data:
            sizes = []
            # Adjusts the legends so that they wrap the text when multiple items are in the classifier
            for i in range(0, len(trace['customdata'])):

                if ', '.join([i.strip() for i in trace['customdata'][i][0].split("<br>")]) == size_by:
                    sizes.append(20)
                else:
                    sizes.append(5)
            trace['marker']['size'] = sizes
    # If the user has clicked a point, draw lines connecting each quadrant for that point
    if clickData:
        xl = plot_data.loc[plot_data[name] == clickData['points'][0]['customdata'][1 if colour_by is not None else 0]][
            'x'].values.tolist()
        xl.append(xl[0])
        yl = plot_data.loc[plot_data[name] == clickData['points'][0]['customdata'][1 if colour_by is not None else 0]][
            'y'].values.tolist()
        yl.append(yl[0])
        fig1.add_trace(go.Scatter(x=xl,
                                  y=yl,
                                  fill="none",
                                  hoverinfo="none"))

        return fig1
    else:
        return fig


# I could not figure out a better way to handle resetting the clickData trace
# so I implemented a simple method that just clears that information
@app.callback(
    Output('basic-interactions', 'clickData'),
    Input('button', 'n_clicks')
)
def reset_plot(clicks):
    if clicks > 0:
        clicks = 0
        return None


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
        try:
            name = hoverData['points'][0]['customdata'][1]
        except IndexError:
            name = hoverData['points'][0]['customdata'][0]
        if pathways is not None:
            path = df.loc[df[row_name] == name, pathways].values[0]
            path = '\n\t\t'.join(x.strip() for x in path.split(','))
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
        hover_output = f'Protein:\t{name}\nColoured by:\t{path}\n' + ''.join(
            f'{k}:\t{output_dict[k]}\n' for k in output_dict.keys())
        return hover_output


# Nearly identical to the hoverData callback except now we will be displaying
# data for the point that was clicked on
@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData'),
     Input('xpos-dropdown', 'value'),
     Input('ypos-dropdown', 'value'),
     Input('xneg-dropdown', 'value'),
     Input('yneg-dropdown', 'value'),
     Input('name-dropdown', 'value'),
     Input('colour-dropdown', 'value'),
     State('xpos-dropdown', 'value')])
def display_click_data(clickData, xpos, ypos, xneg, yneg, row_name, pathways, state):
    if clickData is not None:
        global df
        try:
            name = clickData['points'][0]['customdata'][1]
        except IndexError:
            name = clickData['points'][0]['customdata'][0]
        if pathways is not None:
            path = df.loc[df[row_name] == name, pathways].values[0]
            path = '\n\t\t'.join(x.strip() for x in path.split(','))
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
        click_output = f'Protein:\t{name}\nColoured by:\t{path}\n' + ''.join(
            f'{k}:\t{output_dict[k]}\n' for k in output_dict.keys())
        return click_output


# Populate the size_by dropdown which will increase points that match the selected classifier
@app.callback(
    Output('size_by', 'options'),
    Input('colour-dropdown', 'value')
)
def update_sizeby_dropdown(size_selection):
    return [{'label': name, 'value': name} for name in np.unique(df[size_selection])]


if __name__ == '__main__':
    app.run_server(debug=False)

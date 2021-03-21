import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def update_dropdowns(file_name, df):
    return (
        [html.Label(f"File: {file_name}"), (
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
                clearable=True,
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
            ))]
    )


def serve_layout():
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(
                    html.A(
                        "Help",
                        href="https://github.com/kyle-kroll/BIOT670-Spring-2021",
                        target="_blank",
                        className="nav-link"
                    )
                ),
            ],
            brand="QuadViewer",
            brand_href="#",
            color="primary",
            dark=True,
        ),
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
                        ),
                        html.Label(html.B('Legend Options')),
                        dcc.RadioItems(
                            id='legend-radio',
                            options=[
                                {'label': 'Show Legend', 'value': True},
                                {'label': 'Hide Legend', 'value': False}
                            ],
                            value=True,
                            labelStyle={'display': 'block'}
                        )
                    ]),
                ]),

            ], width={"size": 2}

            ),
            # Figure plot
            dbc.Col(

                html.Div(className='six columns', id='test-cont', children=[
                    dcc.Loading(
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

                        ))
                ]), width={"size": 6, }, style={"height": "800px"}
            ),
            dbc.Col([
                html.Div([
                    html.Button('Refresh Plot', id='button',
                                style={
                                    'margin': '10px'
                                }
                                ),
                    html.Br(),
                    html.Label('Size By'),
                    dcc.Dropdown(
                        id="size_by",
                        clearable=True,
                        searchable=True,
                    ),
                    dcc.Markdown("""
                                        **Hover Data**

                                        Mouse over values in the graph.
                                    """),
                    html.Pre(id='hover-data')
                ]),

                html.Div([
                    dcc.Markdown("""
                                            **Highlighted Data**

                                            Click a point to highlight data.
                                        """),
                    html.Pre(id='click-data')
                ])
            ], width={"size": 4})
            # Second row is for the hover data which only has a single, centered column
        ])
    ])

    return layout

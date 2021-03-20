import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import math
import pandas as pd


'''
    Define the color palette that will be used.
    Author: Mary Mills
    28 colors for options. 
    - Should be more than enough to plot in real world situations
'''

palette = ['limegreen', 'firebrick', 'orangered', 'tomato', 'royalblue', 'seagreen',
           'wheat', 'yellowgreen', 'violet', 'crimson', 'lightseagreen', 'aqua',
           'palegreen', 'chocolate', 'red', 'gold', 'burlywood', 'mediumvioletred',
           'cadetblue', 'goldenrod', 'saddlebrown', 'darkgreen', 'darkred', 'mediumpurple',
           'gray', 'darkmagenta', 'deeppink', 'darkblue']

def generate_plot_data(df, xpos, ypos, xneg, yneg, scale, name, colour_by):
    global plot_data
    fig = go.Figure()
    fig.update_layout(height=700, width=700)
    if None not in [xpos, ypos, xneg, yneg]:
        names = np.concatenate([df[name].values] * 4)
        colors = []
        if colour_by is not None:
            for item in df[colour_by]:
                colors.append('<br>'.join([i.strip() for i in item.split(",")]))
        else:
            colors.append(None)
        colors = np.concatenate([colors] * 4) if colour_by is not None else [None] * len(names)

        xp = df[xpos] if scale == 'lin' else df[xpos].apply(lambda x: math.log10(x + 1))
        yp = df[ypos] if scale == 'lin' else df[ypos].apply(lambda x: math.log10(x + 1))
        xn = df[xneg].apply(lambda x: x * -1) if scale == 'lin' else \
            df[xneg].apply(lambda x: math.log10(x + 1) * -1)
        yn = df[yneg].apply(lambda x: x * -1) if scale == 'lin' else \
            df[yneg].apply(lambda x: math.log10(x + 1) * -1)
        data = {name: names,
                colour_by: colors,
                'x': np.concatenate([xp, xn, xn, xp]),
                'y': np.concatenate([yp, yp, yn, yn])}
        plot_data = pd.DataFrame(data=data)
    return plot_data

def generate_plot(df, xpos, ypos, xneg, yneg, scale, name, colour_by):
    global plot_data
    fig = go.Figure()
    fig.update_layout(height=700, width=700)
    if None not in [xpos, ypos, xneg, yneg]:
        names = np.concatenate([df[name].values] * 4)
        colors = []
        if colour_by is not None:
            for item in df[colour_by]:
                colors.append('<br>'.join([i.strip() for i in item.split(",")]))
        else:
            colors.append(None)
        colors = np.concatenate([colors] * 4) if colour_by is not None else [None] * len(names)

        xp = df[xpos] if scale == 'lin' else df[xpos].apply(lambda x: math.log10(x + 1))
        yp = df[ypos] if scale == 'lin' else df[ypos].apply(lambda x: math.log10(x + 1))
        xn = df[xneg].apply(lambda x: x * -1) if scale == 'lin' else \
            df[xneg].apply(lambda x: math.log10(x + 1) * -1)
        yn = df[yneg].apply(lambda x: x * -1) if scale == 'lin' else \
            df[yneg].apply(lambda x: math.log10(x + 1) * -1)
        data = {name: names,
                colour_by: colors,
                'x': np.concatenate([xp, xn, xn, xp]),
                'y': np.concatenate([yp, yp, yn, yn])}
        plot_data = pd.DataFrame(data=data)
        fig1 = px.scatter(plot_data,
                          x='x',
                          y='y',
                          color=colour_by,
                          color_discrete_sequence=palette,
                          hover_data={
                              'x': False,
                              'y': False,
                              colour_by: False,
                              name: False
                          })

        max_x = max(abs(plot_data['x']))

        max_y = max(abs(plot_data['y']))
        max_axis = max(max_x, max_y)
        fig = go.Figure(data=fig1.data,
                        layout_xaxis_range=[max_axis * -1, max_axis],
                        layout_yaxis_range=[max_axis * -1, max_axis])
        fig.update_layout(legend=dict(orientation='v'), clickmode="event+select")
        fig.add_hline(y=0)
        fig.add_vline(x=0)
        fig.update_layout(

            xaxis_title=f"\u2190{xneg}-----{xpos}\u2192",
            yaxis_title=f"\u2190{yneg}-----{ypos}\u2192",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False)
        if colour_by is not None:
            for trace in fig.data:
                if "None" in trace['customdata'][0]:
                    trace['marker']['opacity'] = 0.2
                    trace['marker']['color'] = 'black'
    return fig



    '''if None not in [xpos, ypos]:
        fig.add_scatter(x=df[xpos] if scale == 'lin' else df[xpos].apply(lambda x: math.log10(x + 1)),
                        y=df[ypos] if scale == 'lin' else df[ypos].apply(lambda x: math.log10(x + 1)),
                        mode='markers',
                        marker_color=[color_dict[k] for k in df[colour_by].values],
                        text=df['Accession_Number'],
                        name="Quadrant 1",
                        showlegend=True,
                        legendgroup="Data")
        plot = True
    if None not in [xneg, ypos]:
        fig.add_scatter(
            x=df[xneg].apply(lambda x: x * -1) if scale == 'lin' else df[xneg].apply(lambda x: math.log10(x + 1) * -1),
            y=df[ypos] if scale == 'lin' else df[ypos].apply(lambda x: math.log10(x + 1)),
            mode='markers',
            marker_color=[color_dict[k] for k in df[colour_by].values],
            text=df['Accession_Number'],
            name="Quadrant 2",
            showlegend=False,
                        legendgroup="Data")
        plot = True
    if None not in [xneg, yneg]:
        fig.add_scatter(
            x=df[xneg].apply(lambda x: x * -1) if scale == 'lin' else df[xneg].apply(lambda x: math.log10(x + 1) * -1),
            y=df[yneg].apply(lambda x: x * -1) if scale == 'lin' else df[yneg].apply(lambda x: math.log10(x + 1) * -1),
            mode='markers',
            marker_color=[color_dict[k] for k in df[colour_by].values],
            text=df['Accession_Number'],
            name="Quadrant 3",
            showlegend=False,
            legendgroup="Data")
        plot = True
    if None not in [xpos, yneg]:
        fig.add_scatter(x=df[xpos] if scale == 'lin' else df[xpos].apply(lambda x: math.log10(x + 1)),
                        y=df[yneg].apply(lambda x: x * -1) if scale == 'lin' else df[yneg].apply(
                            lambda x: math.log10(x + 1) * -1),
                        mode='markers',
                        marker_color=[color_dict[k] for k in df[colour_by].values],
                        text=df['Accession_Number'],
                        name="Quadrant 4",
                        showlegend=False,
                        legendgroup="Data")
        plot = True

    # Add in axis labels
    if plot:
        for k in color_dict.keys():
            fig.add_scatter(x=[None], y=[None], mode='markers',
                            marker=dict(size=10, color=color_dict[k]),
                            legendgroup='Markers', showlegend=True, name=k)
        fig.add_hline(y=0)
        fig.add_vline(x=0)
        fig.update_layout(
            xaxis_title=f"\u2190{xneg}-----{xpos}\u2192",
            yaxis_title=f"\u2190{yneg}-----{ypos}\u2192",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(

                orientation="h")
            )
        return fig
    else:
        fig = go.Figure()
        fig.update_layout(height=600, width=600)
        return fig
    
    if None not in [xpos, ypos, xneg, yneg]:
        # Create a figure for each quadrant
        fig1 = px.scatter(df, x=xpos, y=ypos, color=colour_by, custom_data=[name],
                          color_discrete_sequence=palette,
                          hover_data={
                              xpos: False,
                              ypos: False,
                              colour_by: False,
                              name: True
                          })
        fig2 = px.scatter(df, x=xneg, y=ypos, color=colour_by, custom_data=[name],
                          color_discrete_sequence=palette,
                          hover_data={
                              xpos: False,
                              ypos: False,
                              colour_by: False,
                              name: True
                          })
        fig2.update_layout(showlegend=False)
        fig3 = px.scatter(df, x=xneg, y=yneg, color=colour_by, custom_data=[name],
                          color_discrete_sequence=palette,
                          hover_data={
                              xpos: False,
                              ypos: False,
                              colour_by: False,
                              name: True
                          })
        fig3.update_layout(showlegend=False)
        fig4 = px.scatter(df, x=xpos, y=yneg, color=colour_by, custom_data=[name],
                          color_discrete_sequence=palette,
                          hover_data={
                              xpos: False,
                              ypos: False,
                              colour_by: False,
                              name: True
                          })
        fig4.update_layout(showlegend=False)

        # Set negative columns to negative values
        for sc in fig1['data']:
            sc['x'] = sc['x']
            sc['y'] = sc['y']
        for sc in fig2['data']:
            sc['x'] = sc['x'] * -1
            sc['y'] = sc['y']
        for sc in fig3['data']:
            sc['x'] = sc['x'] * -1
            sc['y'] = sc['y'] * -1
        for sc in fig4['data']:
            sc['x'] = sc['x']
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
        ax_dict = dict(
                tickmode='array',
                tickvals=np.concatenate([list(range(axis_max * -1, 1, 100)), list(range(0, axis_max + 1, 100))]),
                ticktext=np.concatenate(
                    [[x * -1 for x in list(range(axis_max * -1, 1, 100))], list(range(0, axis_max + 1, 100))]))
        # Create the final figure with new axis limits
        fig = go.Figure(data=fig1.data + fig2.data + fig3.data + fig4.data,
                        layout_xaxis_range=[axis_max * -1, axis_max],
                        layout_yaxis_range=[axis_max * -1, axis_max])

        # Update the axis ticks so they don't show negative values
        fig.update_layout(
            xaxis=ax_dict,
            yaxis=ax_dict,
            width=600,
            height=600, showlegend=False
        )

        # Add in new trace for colors
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            marker_colorscale=palette,
            mode='markers'
        ))

    # Add in axis labels

    fig.add_hline(y=0)
    fig.add_vline(x=0)
    fig.update_layout(

        xaxis_title=f"\u2190{xneg}-----{xpos}\u2192",
        yaxis_title=f"\u2190{yneg}-----{ypos}\u2192",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return fig'''

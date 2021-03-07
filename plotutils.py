import plotly.graph_objects as go
import numpy as np
import plotly.express as px


'''
    Define the color palette that will be used.
    Author: Mary Mills
    28 colors for options. 
    - Should be more than enough to plot in real world situations
'''

palette=['limegreen', 'firebrick', 'orangered', 'tomato', 'royalblue', 'seagreen',
         'wheat', 'yellowgreen', 'violet', 'crimson', 'lightseagreen', 'aqua',
         'palegreen', 'chocolate', 'red', 'gold', 'burlywood', 'mediumvioletred',
         'cadetblue', 'goldenrod', 'saddlebrown', 'darkgreen', 'darkred', 'mediumpurple',
         'gray', 'darkmagenta', 'deeppink', 'darkblue']


def generate_plot(df, xpos, ypos, xneg, yneg, scale, name, colour_by):
    fig = go.Figure()
    fig.update_layout(height=600, width=600, autosize=False)
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

    # Add in axis labels

    fig.add_hline(y=0)
    fig.add_vline(x=0)
    fig.update_layout(

        xaxis_title=f"\u2190{xneg}-----{xpos}\u2192",
        yaxis_title=f"\u2190{yneg}-----{ypos}\u2192",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return fig



# Color dictionary - Mary
# Dicitonary for colors of pathways
color_dict = {'Integrin': 'limegreen',
              'Blood_Coagulation': 'firebrick',
              'Cytoskeleton': 'orangered',
              'Chemokine_Cytokine_Signaling': 'tomato',
              'Chemokine_Cytokine_Signaling, Cytoskeleton': 'royalblue',
              'Chemokine_Cytokine_Signaling, Cytoskeleton, Integrin': 'seagreen',
              'Chemokine_Cytokine_Signaling, Cytoskeleton, Huntington': 'wheat',
              'Chemokine_Cytokine_Signaling, Huntington, Integrin': 'yellowgreen',
              'Chemokine_Cytokine_Signaling, Cytoskeleton, Huntington, Integrin': 'violet',
              'Huntington, Integrin': 'crimson',
              'Parkinson': 'lightseagreen',
              'Cytoskeleton, Huntington': 'aqua',
              'Chemokine_Cytokine_Signaling, Integrin': 'palegreen',
              'Glycolysis, Huntington': 'chocolate',
              'ATP_Synthesis': 'brown',
              'ATP_Synthesis, Huntington': 'burlywood',
              'Glycolysis': 'mediumvioletred',
              'Glycolysis, Pyruvate_Metabolism': 'cadetblue',
              'Huntington': 'goldenrod',
              'Pyruvate_Metabolism': 'darkkhaki',
              'Pyruvate_Metabolism, TCA_Cycle': 'sienna',
              'TCA_Cycle': 'darkred',
              'De_Novo_Purine_Biosynthesis': 'mediumpurple',
              'None': 'slategray'}


import plotly.express as px

def chart_scatter_plotly(chart_hits):
    '''
    Accepts a ACE.chart_hits object.
    Returns a plotly line figure
    '''
    x_axis = [i.date for i in chart_hits]
    y_axis = [i.position for i in chart_hits]
    
    if chart_hits and hasattr(chart_hits[0], 'song_name') and chart_hits[0].song_name:
        color = [i.song_name for i in chart_hits]
    else:
        color = None
    fig = px.scatter(
    x=x_axis,
    y=y_axis,
    color=color,
    )
    
    fig.update_layout(yaxis=dict(autorange="reversed"))

    # Add titles to the x and y axes
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Chart Position",
        template='plotly_dark',
    )
    return fig
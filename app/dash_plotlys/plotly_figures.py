import plotly.express as px

def chart_scatter_plotly(
        dates,
        positions,
        songs_or_arts,
):
    '''
    Accepts a ACE.chart_hits object.
    Returns a plotly line figure
    '''
    fig = px.scatter(
    x=dates,
    y=positions,
    color=songs_or_arts,
    )
    
    fig.update_layout(yaxis=dict(autorange="reversed"))

    # Add titles to the x and y axes
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Chart Position",
        template='plotly_dark',
        legend_title_text='',
    )
    
    return fig

def year_month_line_chart(
        dates,
        positions,
        art_names
):
    fig = px.line(
    x=dates,
    y=positions,
    color=art_names,
    )
    #print("Creating figure with x:", dates, "y:", positions, "colors:", art_names)
    fig.update_layout(yaxis=dict(autorange="reversed"))

    # Add titles to the x and y axes
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Chart Position",
        template='plotly_dark',
        showlegend=False,
    )
    fig.update_layout(
        config=dict(
            displayModeBar=False,
        )
    )
    
    return fig
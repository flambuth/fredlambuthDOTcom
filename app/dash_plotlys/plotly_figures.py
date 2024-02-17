import plotly.express as px


###########################
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


######################
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

    
    return fig


##############################
#global dash figures

def songs_line_chart(df):
    '''
    Returns a line chart of the input df. Uses
    '''
    #df['name_truncated'] = df['name'].str.slice(0, 30)
    df['name_truncated'] = df['name'].apply(lambda x: x[:40] if '(' not in x else x.split('(')[0][:40])
    df['name_artists'] = df['name_truncated'] + ' - ' + df['artists']
    first_date = min(df.snapshot_date)
    last_date = max(df.snapshot_date)

    fig = px.line(
        x=df.snapshot_date,
        y=df.daily_rank,
        color=df.name_artists,
        template='plotly_dark',
        #title=f"The Top 10 Songs Since {first_date}"
    )

    fig.update_layout(
        yaxis_title="Chart Position",
        xaxis_title=" ",
        height=880, 
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.01,
            title_text=f"The Top 10 Songs from {first_date} - {last_date}",
            traceorder="normal",  # Stack legend title on top of legend items
            itemsizing="constant",  # Ensure constant item size across legends
            itemwidth=100  # Adjust the width of each legend item
        )
    )
    # Invert the y-axis
    fig.update_yaxes(autorange="reversed",)

    return fig


def artists_hbar_chart(df_top_artists):
    '''
    Returns a line chart of the input df. Uses
    '''

    fig = px.bar(
        y=df_top_artists.artist,
        x=df_top_artists.appearances,
        color=df_top_artists.unique_songs,
        orientation='h',
        template='plotly_dark',
        color_continuous_scale='darkmint',  # You can customize the color scale here
        range_color=[0, 10],
    )

    fig.update_layout(
        yaxis_title="",
        xaxis_title="",
        title='Most Chart Appearances',
        xaxis=dict(range=[0, max(df_top_artists['appearances']) + 1]),  # Set the range_x parameter
        
    )

    # Invert the y-axis
    fig.update_yaxes(autorange="reversed")
    fig.update(layout_coloraxis_showscale=False)

    annotation_text = "Color Represents Unique Song Count"
    annotation_x = 5  # X-coordinate of the annotation
    annotation_y = 0  # Y-coordinate of the annotation

    fig.add_annotation(
        text=annotation_text,
        x=annotation_x,
        y=annotation_y,
        #showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-30,
        font=dict(size=8)
    )

    return fig
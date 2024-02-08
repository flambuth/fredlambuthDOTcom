import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
#import plotly.express as px
#import pandas as pd
import global_stats

# Dash app
app = dash.Dash(__name__)

# Dropdown options
countries = list(global_stats.country_codes.values())

dropdown_options = [{'label': category, 'value': category} for category in countries]

# App layout
app.layout = html.Div([
    dcc.Dropdown(
        id='category-dropdown',
        options=dropdown_options,
        value=countries[4]  # Default value
    ),
    dash_table.DataTable(
        id='top10-today-table',
        columns=[{"name": col, "id": col} for col in global_stats.Chart_Data().todays_top10().columns],
        style_table={'height': '300px', 'overflowY': 'auto'}
    ),
    dash_table.DataTable(
        id='top10-songs-table',
        columns=[{"name": col, "id": col} for col in global_stats.Chart_Data().top_n_names_in_df().columns],
        style_table={'height': '300px', 'overflowY': 'auto'}
    ),

    #tuples
    html.Div(
        id='top10_artists',
        style={'height': '300px', 'overflowY': 'auto'}
    ),


    dcc.Graph(id='hbar-plot'),
    dcc.Graph(id='line-plot')
])

# Callback to update the graph based on dropdown selection
@app.callback(
    Output('top10-today-table', 'data'),
    Output('top10-songs-table', 'data'),

    Output('top10_artists','children'),

    Output('hbar-plot', 'figure'),
    Output('line-plot', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_graph(selected_category):
    #big_df = global_stats.cleaned_df()
    blob = global_stats.Country_Chart_Data(selected_category)
    top10_today_data = blob.df_today_top10.to_dict('records')
    top10_songs_data = blob.df_top_10_songs.to_dict('records')

    #tuples
    top10_artists = blob.top_10_artists
    top10_art_tuples = [html.P(str(row)) for row in top10_artists]

    fig1 = blob.fig_top10_artists
    fig2 = blob.fig_top10_song
    return top10_today_data, top10_songs_data, top10_art_tuples, fig1, fig2

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

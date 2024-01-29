from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
load_figure_template('LUX')

from app.dash_plotlys.layouts import create_navbar, my_icon, notable_tracks_html, longest_artist_streak_html
from app.dash_plotlys import data_sources, plotly_figures

def Add_Dash_art_cat(flask_app):
    dash_app = Dash(
        server=flask_app, name="art_cat", 
        url_base_pathname="/dash/art_cat/",
        external_stylesheets=[dbc.themes.LUX])
    dash_app.layout = html.Div(
        style={'backgroundColor': 'black'},
        children=[
            dcc.Location(id='url', refresh=False),
            create_navbar(),
            html.Div(id='my_output'),
            #dcc.Store(id='artist_name_store'),  # Store component to hold the artist name
            dcc.Graph(
                id="artist_history",
            ),
            my_icon
        ]
    )
    dash_app.title = 'My Listening History'

    #the component_ids are referenced in the dash_app.layout. There are dcc or html objects that have 
    #the same id as the component ids in this dash callback.
    @dash_app.callback(
        Output(component_id='artist_history', component_property='figure'),
        Output(component_id='my_output', component_property='children'),
        #Input(component_id='my_input', component_property='value'),
        Input('url', 'pathname'),  # This input captures the URL pathname
    )
    def update_graph(pathname):
        '''
        This does all the HTML work that isn't done by the Dashboard itself imported from Chartsie
        '''
        #art_cat_data = char.art_cat_entry(input_art_name)[0]
        input_art_id = pathname.split('/')[-1]

        if input_art_id is None:
            input_art_id = '41Q0HrwWBtuUkJc7C1Rp6K'

        #fig, art_cat_data, hits_data = char.total_artist_history(input_art_name)
        art_cat_data = data_sources.Artist_Catalog_Enriched(input_art_id)
        #fig_tracks = plotly_figures.chart_scatter_plotly(art_cat_data.track_hits)
        fig_arts = plotly_figures.chart_scatter_plotly(art_cat_data.arts_hits)


        
        #if hits_data.art_spots == None:
        #    fig = None
        totem_div = html.Div(children=[
                    dbc.Container(children=[
                        dbc.Row([
                                html.H1(children=art_cat_data.art_cat.art_name,
                                style={'color':'green', 'textAlign':'center'}
                                ),
                        html.Div(children=art_cat_data.art_cat.genre, style={'textAlign':'center'}),
                        ], style = {'padding-bottom':'10px'}),
                        dbc.Row([
                            dbc.Col([                        
                        html.H5(children='First Appearance', style={'textAlign':'left', 'font-weight':'bold', }),
                        html.Div(children=art_cat_data.first_and_last_appearance()[0], style={'padding-bottom':'5px'}),
                        longest_artist_streak_html(art_cat_data.longest_streak)[0],
                        longest_artist_streak_html(art_cat_data.longest_streak)[1],
                        html.H5(children='Latest Appearance', style={'textAlign':'left', 'font-weight':'bold', }),
                        art_cat_data.first_and_last_appearance()[1],
                                    ]),
                            dbc.Col([
                                notable_tracks_html(art_cat_data.notable_tracks)[0],
                                notable_tracks_html(art_cat_data.notable_tracks)[1],
                        ]),
                            dbc.Col(
                        html.Img(src=f"https://i.scdn.co/image/{art_cat_data.art_cat.img_url}", style={'width':260}))
                            ])])
                            ])
        if fig_arts is None:
            placeholder_text = "No data available"
            return dcc.Markdown(f"**{placeholder_text}**"), totem_div
        else:
            return fig_arts, totem_div
        #return fig, totem_div
    return dash_app
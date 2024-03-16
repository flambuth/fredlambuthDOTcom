from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
load_figure_template('VAPOR')

from app.dash_plotlys import data_sources, plotly_figures, layouts



navbar = layouts.create_navbar()
#navbar_style = {
#    'backgroundColor': 'white',  # Change this to your desired color
    # Add other styles as needed
#}
#navbar = dbc.Navbar(navbar, style=navbar_style)

def Add_Big_Dash(flask_app):
    dash_app = Dash(
        server=flask_app, name="big_dash", 
        url_base_pathname="/spotify/big_dash/",
        external_stylesheets=[dbc.themes.VAPOR, '/static/css/style.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'])
    
    dash_app.layout = dbc.Container([
        navbar,
        # headline row
        dbc.Row([
            dbc.Col([
                html.Label('Week(s) Ago', style={'marginRight': '10px'}),
                dcc.RadioItems(
                    options=[
                        {'label': ' One', 'value': '7'},
                        {'label': ' Two', 'value': '14'},
                        {'label': ' Three', 'value': '21'}
                    ],
                    value='7',
                    id='daterange-selection'
                ),
            ], width=2, class_name="dash-div",),
            dbc.Col([
                html.H1(
                    children='Some Spotify Stats',
                    style={'textAlign': 'center'},
                    className="dash-div",),
                html.Div(
                    id='date-range-info',
                    style={'textAlign':'center'}
                    ),
                    html.Small(
                        "Please hit refresh after resizing (or resize after refreshing).",
                        style={'display': 'block', 'textAlign': 'center', 'margin-top': '5px', 'color': 'gray'}
                    ),
            ], width=10),
        ], className="dash-div",),

        #middle row
        dbc.Row([
            dbc.Col([
                html.Div(id='top-subgenre-card', style={'padding':'10px'}),
                html.Div(id='top-master-genre-card', style={'padding':'10px'}),
                html.Div(id='top-song-card', style={'padding':'10px'}),
            ], width=2, className="dash-div"),
            dbc.Col([
                #1linegraph
                dbc.Row([
                    dbc.Col(dcc.Graph(id='hourly-line-graph', config={'displayModeBar': False}), style={'padding': '10px'}),  
                ], className="dash-div", style={'margin-bottom': '20px', 'padding': '10px'}),

                #2graphs
                dbc.Row([
                    dbc.Col(dcc.Graph(
                        id='known-pie-graph', 
                        config={'displayModeBar': False}), 
                        style={'padding': '10px'}, 
                        className="dash-div",
                        width=3),  
                    dbc.Col(dcc.Graph(
                        id='day-of-week-graph', 
                        config={'displayModeBar': False}), 
                        style={'padding': '10px'}, 
                        class_name="dash-div",
                        width=9),
                ],  style={'margin-bottom': '20px', 'padding': '10px'}),
            ], width=10),
        ]),

    
        # cards row
        dbc.Row([
            dbc.Col(html.Div(id='top-3-cards'), style={'padding': '10px'}),  
        ], className="dash-div", style={'padding': '10px'}),
        layouts.my_icon,
    ], fluid=True,)

    dash_app.title = 'Every Whizbang Plotly Can Muster'

    #the component_ids are referenced in the dash_app.layout. There are dcc or html objects that have 
    #the same id as the component ids in this dash callback.
    @dash_app.callback(
        Output('day-of-week-graph', 'figure'),
        Output('known-pie-graph', 'figure'),
        Output('top-3-cards', 'children'),
        Output('date-range-info', 'children'),
        Output('hourly-line-graph', 'figure'),
        Output('top-subgenre-card', 'children'),
        Output('top-master-genre-card', 'children'),
        Output('top-song-card', 'children'),
        Input('daterange-selection', 'value'),        
    )
    def update_graph(value):
        rp_stuff = data_sources.Fred_Big_Dash_Stuff(int(value), 5)
        top_3_imgs_div = layouts.top_3_imgs(rp_stuff.top_tuples)

        day_of_week_fig = plotly_figures.day_of_week_bars(rp_stuff.dts, rp_stuff.mean_song_per_day)
        known_pie_fig = plotly_figures.un_known_pie_chart(rp_stuff.known, rp_stuff.unknown)

        hourly_line_fig = plotly_figures.hourly_listening_line_chart(rp_stuff.avg_song_per_hour_Series())

        date_range_info = html.H5(f'{rp_stuff.first_day} thru {rp_stuff.last_day}')  # New date range info

        top_subgenre_card = layouts.side_card(
            'Top Sub-Genre',
            rp_stuff.rando_subgenre_ac.img_url_mid,
            rp_stuff.known_genre_counts()[1][0][0]
        )
        top_master_genre_card = layouts.side_card(
            'Top Genre',
            rp_stuff.rando_master_genre_ac.img_url_mid,
            rp_stuff.rando_master_genre_ac.master_genre
        )
        top_song_card = layouts.side_card(
            'Top Song',
            rp_stuff.top_rp.image[-40:],
            rp_stuff.top_rp.song_name
        )

        return day_of_week_fig, known_pie_fig, top_3_imgs_div, date_range_info, hourly_line_fig, top_subgenre_card, top_master_genre_card, top_song_card

    return dash_app.server
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
    # headline column
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
                children='My Spotify Stats',
                style={'textAlign': 'center'},
                className="dash-div",),
            html.Div(
                id='date-range-info',
                style={'textAlign':'center'}
                ),
        ], width=10),
    ], className="dash-div",),

    # graphs row
    dbc.Row([
        dbc.Col(dcc.Graph(id='known-pie-graph')),  
        dbc.Col(dcc.Graph(id='day-of-week-graph')),
    ], className="dash-div",),

    # cards row
    dbc.Row([
        dbc.Col(html.Div(id='top-3-cards')),  
    ], className="dash-div",),
    layouts.my_icon,
], fluid=True,)

    dash_app.title = 'The Big Fred Dashboard'

    #the component_ids are referenced in the dash_app.layout. There are dcc or html objects that have 
    #the same id as the component ids in this dash callback.
    @dash_app.callback(
        Output('day-of-week-graph', 'figure'),
        Output('known-pie-graph', 'figure'),
        Output('top-3-cards', 'children'),
        Output('date-range-info', 'children'),
        Input('daterange-selection', 'value')
    )
    def update_graph(value):
        rp_stuff = data_sources.Fred_Big_Dash_Stuff(int(value))
        top_3_imgs_div = layouts.top_3_imgs(rp_stuff.top_tuples)

        day_of_week_fig = plotly_figures.day_of_week_bars(rp_stuff.dts, rp_stuff.mean_song_per_day)
        known_pie_fig = plotly_figures.un_known_pie_chart(rp_stuff.known, rp_stuff.unknown)

        date_range_info = html.H5(f'{rp_stuff.first_day} thru {rp_stuff.last_day}')  # New date range info

        return day_of_week_fig, known_pie_fig, top_3_imgs_div, date_range_info

    return dash_app.server
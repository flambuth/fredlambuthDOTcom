from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output
from datetime import date

#from dash import url
from app.dash_plotlys.layouts import create_navbar, my_icon

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from app.dash_plotlys import data_sources, plotly_figures
load_figure_template('LUX')

navbar = create_navbar()

def Add_Dash_year_month(flask_app):
    dash_app = Dash(
        server=flask_app, name="art_cat", 
        url_base_pathname="/dash/months/",
        external_stylesheets=[dbc.themes.LUX])
    dash_app.layout = html.Div(
        style={'backgroundColor': 'black'},
        children=[
            dcc.Location(id='url', refresh=False),
            navbar,
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
        #Input(component_id='my_input', component_property='value'),
        Input('url', 'pathname'),  # This input captures the URL pathname
    )
    def update_graph(pathname):
        '''
        This does all the HTML work that isn't done by the Dashboard itself imported from Chartsie
        '''
        #art_cat_data = char.art_cat_entry(input_art_name)[0]
        input_month = pathname.split('/')[-1]
        input_year = pathname.split('/')[-2]

        if input_month is None:
            input_month = date.today().month - 1
            input_year = date.today().year

        month_arts = data_sources.Chart_Year_Month_Stats(input_year,input_month)
        x,y,z=month_arts.line_chart_components()
        fig = plotly_figures.year_month_line_chart(x,y,z)


        
        #if hits_data.art_spots == None:
        #    fig = None

        

    



        if fig is None:
            placeholder_text = "No data available"
            return dcc.Markdown(f"**{placeholder_text}**")
        else:
            return fig
        #return fig, totem_div
    return dash_app
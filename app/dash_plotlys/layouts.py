import dash_bootstrap_components as dbc
from dash import html, dcc

from datetime import datetime

this_year = datetime.today().year
image_url = "/static/favicon.ico"
image_alt = "Howdy!"

my_icon = html.Header([
            html.Link(
                rel='icon',
                href=image_url,  # Replace with the actual path
                type='image/x-icon'
            ),
        ])

dash_links = dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("Artist Catalog", href='https://fredlambuth.com/spotify/artists'),
                                dbc.DropdownMenuItem("Twenty Four Hours each Month", href="https://fredlambuth.com/dash/24"),
                                dbc.DropdownMenuItem("Top Artists of Each Month", href=f"https://fredlambuth.com/dash/{this_year}"),
                                dbc.DropdownMenuItem("Artist Total Listening History", href="https://fredlambuth.com/dash/art_search"),
                                dbc.DropdownMenuItem("Global Spotify Stats & Me", href="https://fredlambuth.com/dash/global"),
                                    ],
                                nav=True,
                                in_navbar=True,
                                label="Links")

def create_navbar():
    # Create the brand element with the image and text
    brand_element = dbc.NavbarBrand(
        children=[
            html.Img(src=image_url, height="30px", title=image_alt),  # Adjust the height as needed
            " Fredlambuth.com",
        ],
        href="https://fredlambuth.com/",
    )

    navbar = dbc.NavbarSimple(
        children=[
            dash_links,
        ],
        brand=brand_element,  # Use the brand element with the image and text
        color="primary",
        dark=True,
        style={'borderBottom':'5px solid #238a6b'}
    )

    return navbar

def notable_tracks_html(notable_tracks):
    '''
    TBA
    '''
    if len(notable_tracks) == 0:
        return (None, None)
    track_hits_heading = html.H5(children='Notable Tracks', style={'textAlign':'left', 'font-weight':'bold',})
    list_group = dbc.ListGroup(
    [html.Div(children=song, style={'textAlign':'left'}) for song in notable_tracks]
)
    return (track_hits_heading, list_group)

def longest_artist_streak_html(longest_streak):
    if longest_streak == None:
        return (None, None)

    html_line = html.Div(children=f'{longest_streak[1]} days beginning on {longest_streak[0]}', style={'padding-bottom':'5px'})

    heading = html.H5(children='Longest Streak', style={'textAlign':'left', 'font-weight':'bold',})

    return (heading, html_line)
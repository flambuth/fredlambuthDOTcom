import dash_bootstrap_components as dbc
from dash import html, dcc

from flask import url_for

from datetime import datetime

this_year = datetime.today().year
image_url = "/static/favicon.ico"
image_alt = "Howdy!"

colors = {
    'background': '#111111',
    'text': '#238a6b'
}

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
    #root_url = url_for('homepage')

    brand_element = dbc.NavbarBrand(
        children=[
            html.Img(src=image_url, height="30px", title=image_alt),  # Adjust the height as needed
            " Fredlambuth.com",
        ],
        #href='url_for('homepage')',
        href='#',
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

########################
#Monthly view
def artist_card(art_cat):
    '''
    Returns a DBC.card object. Accepts the art_cat models as input
    '''
    this_card = dbc.Card([
        dbc.CardImg(
            src=f"https://i.scdn.co/image/{art_cat.img_url_mid}",
            top=True,
            style={'opacity': 0.3, 'width': '100%', 'heighth':'80%',},  # Set width to 100%
        ),
        dbc.CardImgOverlay(
            dbc.CardBody(
                [
                    html.H4(art_cat.art_name, className="card-title"),
                    html.P(
                        art_cat.genre,
                        className="card-text",
                    ),
                    dbc.Button(
                        art_cat.master_genre,
                        color='primary',
                        href='https://fredlambuth.com/spotify/artists/genre/'+art_cat.master_genre),
                ]
            ),
        ),
    ])
    return this_card


def artist_card_row(art_cats):
    ''''
    List comprehension of the input art_cats. Creates a row with the layout.artist_card, for each
    art_cat from the parameter.
    '''
    colors = ['blue', 'red', 'green', 'gold', 'cyan']

    totem_div = html.Div(children=[
        dbc.Row([
            dbc.Col([
                artist_card(artist),
            ], style={
                    'border': f'2px solid {colors[i % len(colors)]}',  # Border style with color
                    'border-radius': '10px',  # Optional: Add rounded corners
                    'padding': '10px',
                    'height': '60%',
                })  
            for i, artist in enumerate(art_cats)
        ])
    ])
    return totem_div



#############################
#Artist History
def notable_tracks_html(notable_tracks):
    '''
    TBA
    '''
    if len(notable_tracks) == 0:
        return (None, None)
    track_hits_heading = html.H5(children='Notable Tracks', style={'textAlign':'left', 'font-weight':'bold','color':colors['text']})
    list_group = dbc.ListGroup(
    [html.Div(children=song, style={'textAlign':'left'}) for song in notable_tracks]
)
    return (track_hits_heading, list_group)

def longest_artist_streak_html(longest_streak):
    if longest_streak == None:
        return (None, None)

    html_line = html.Div(children=f'{longest_streak[1]} days beginning on {longest_streak[0]}', style={'padding-bottom':'5px'})

    heading = html.H5(children='Longest Streak', style={'textAlign':'left', 'font-weight':'bold','color':colors['text']})

    return (heading, html_line)

def artist_history_stats_html(art_cat_data):
    #will display all genres if available, or jsut 1 or 2
    genres = [art_cat_data.art_cat.genre, art_cat_data.art_cat.genre2, art_cat_data.art_cat.genre3]
    genre_divs = []
    #iterates the genre attributes to make a list of up to 3
    for genre in genres:
        if genre:
            genre_divs.append(html.Div(children=genre, style={'margin-right': '20px'}))

    totem_div = html.Div(children=[
        dbc.Container(
            fluid=True,
            style={'maxWidth':'800px'},
            children=[
            dbc.Row([
                html.H1(children=art_cat_data.art_cat.art_name,
                        style={'color':'green', 'textAlign':'center'}),
                html.Div(children=genre_divs, style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-top':'10px', 'margin-bottom':'10px'}),
            ]),
            dbc.Row([
                dbc.Col([                        
                    html.H5(children='First Appearance', style={'textAlign':'left', 'font-weight':'bold', 'color':colors['text']}),
                    html.Div(children=art_cat_data.first_and_last_appearance()[0], style={'padding-bottom':'5px'}),
                    longest_artist_streak_html(art_cat_data.longest_streak)[0],
                    longest_artist_streak_html(art_cat_data.longest_streak)[1],
                    html.H5(children='Latest Appearance', style={'textAlign':'left', 'font-weight':'bold', 'color':colors['text']}),
                    art_cat_data.first_and_last_appearance()[1],
                ]),
                dbc.Col(
                    html.Img(src=f"https://i.scdn.co/image/{art_cat_data.art_cat.img_url}", style={'width':260,'border': f'2px solid {colors["text"]}', 'border-radius': '10px'})
                )
            ])
        ])
    ])
    return totem_div


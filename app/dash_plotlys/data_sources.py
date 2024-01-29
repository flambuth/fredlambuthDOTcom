from app.models.catalogs import artist_catalog
from app.models.charts import daily_artists, daily_tracks
from app import utils

#from sqlalchemy import func



class Artist_Catalog_Enriched:
    '''
    Holds together the data that will fill out the 'artist_history' plotly-dash.
    '''
    def __init__(self, art_id):
        self.art_id = art_id

        #daily Charts data:tracks
        self.track_hits = daily_tracks.artist_days_on_chart(art_id)
        self.track_streaks = utils.find_streaks_in_dates([i.date for i in self.track_hits])
        self.track_days = len(self.track_hits)
        #returns a list of song_names if this art_id has appearances in the daily_tracks charts
        self.notable_tracks = list(set(
            [i.song_name for i in self.track_hits]
        ))
        
        #daily_artists
        self.arts_hits = daily_artists.artist_days_on_chart(art_id)
        self.arts_streaks = utils.find_streaks_in_dates([i.date for i in self.arts_hits])
        self.arts_days = len(self.arts_hits)

        #returns a tuple that is ('date','int')
        self.longest_streak = utils.evaluate_longest_streak(
            self.track_streaks,
            self.arts_streaks
        )
        #art_cat data
        self.art_cat = artist_catalog.art_id_to_art_cat(art_id)

    def first_and_last_appearance(self):
        both_charts = self.track_hits + self.arts_hits
        all_dates = sorted([i.date for i in both_charts])
        first_date = all_dates[0]
        last_date = all_dates[-1]
        return first_date, last_date

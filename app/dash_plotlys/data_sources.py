from app.models.catalogs import artist_catalog
from app.models.charts import daily_artists, daily_tracks
from app import utils
from sqlalchemy import func

#from sqlalchemy import func
class Chart_Year_Month_Stats:

    def __init__(self, year, month):
        #self.top_5_in_tracks = daily_tracks.hits_in_year_month(year, month)
        #self.top_5_names_in_tracks = [i[0] for i in self.top_5_in_tracks]

        #find the top5 artists names of the year-month set by the parameters
        self.top_5_in_arts = daily_artists.hits_in_year_month(year, month)
        #lsit of 5 strings
        self.top_5_names_in_arts = [i[0] for i in self.top_5_in_arts]

        self.top_5_artcats = artist_catalog.get_current_records().filter(artist_catalog.art_name.in_(self.top_5_names_in_arts)).order_by(artist_catalog.art_name).all()

        #filter down to the daily_arts charts that is just the top5
        self.arts_of_top5 = daily_artists.filter_by_year_month(year,month).filter(daily_artists.art_name.in_(self.top_5_names_in_arts)).order_by(daily_artists.art_name).all()

    def line_chart_components(self):
        dates = [i.date for i in self.arts_of_top5]
        positions = [i.position for i in self.arts_of_top5]
        art_names = [i.art_name for i in self.arts_of_top5]
        return dates, positions, art_names


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

    def scatter_plot_components(self):
        arts_triples = [
            (i.date, i.position, self.art_cat.art_name)
            for i in self.arts_hits]
        track_triples = [
            (i.date, i.position, i.song_name)
            for i in self.track_hits]
        both = arts_triples + track_triples
        x = [i[0] for i in both]
        y = [i[1] for i in both]
        z = [i[2] for i in both]
        return x,y,z
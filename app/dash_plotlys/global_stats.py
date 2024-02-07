from collections import Counter
import pandas as pd
import plotly.express as px

def cleaned_df(csv_name='universal_top_spotify_songs.csv'):
    '''
    csv_name = 'universal_top_spotify_songs.csv'
    '''
    country_codes = {
        'ZA': 'South Africa',
        'VN': 'Vietnam',
        'VE': 'Venezuela',
        'UY': 'Uruguay',
        'US': 'United States',
        'UA': 'Ukraine',
        'TW': 'Taiwan',
        'TR': 'Turkey',
        'TH': 'Thailand',
        'SV': 'El Salvador',
        'SK': 'Slovakia',
        'SG': 'Singapore',
        'SE': 'Sweden',
        'SA': 'Saudi Arabia',
        'RO': 'Romania',
        'PY': 'Paraguay',
        'PT': 'Portugal',
        'PL': 'Poland',
        'PK': 'Pakistan',
        'PH': 'Philippines',
        'PE': 'Peru',
        'PA': 'Panama',
        'NZ': 'New Zealand',
        'NO': 'Norway',
        'NL': 'Netherlands',
        'NI': 'Nicaragua',
        'NG': 'Nigeria',
        'MY': 'Malaysia',
        'MX': 'Mexico',
        'MA': 'Morocco',
        'LV': 'Latvia',
        'LU': 'Luxembourg',
        'LT': 'Lithuania',
        'KZ': 'Kazakhstan',
        'KR': 'South Korea',
        'JP': 'Japan',
        'IT': 'Italy',
        'IS': 'Iceland',
        'IN': 'India',
        'IL': 'Israel',
        'IE': 'Ireland',
        'ID': 'Indonesia',
        'HU': 'Hungary',
        'HN': 'Honduras',
        'HK': 'Hong Kong',
        'GT': 'Guatemala',
        'GR': 'Greece',
        'GB': 'United Kingdom',
        'FR': 'France',
        'FI': 'Finland',
        'ES': 'Spain',
        'EG': 'Egypt',
        'EE': 'Estonia',
        'EC': 'Ecuador',
        'DO': 'Dominican Republic',
        'DK': 'Denmark',
        'DE': 'Germany',
        'CZ': 'Czech Republic',
        'CR': 'Costa Rica',
        'CO': 'Colombia',
        'CL': 'Chile',
        'CH': 'Switzerland',
        'CA': 'Canada',
        'BY': 'Belarus',
        'BR': 'Brazil',
        'BO': 'Bolivia',
        'BG': 'Bulgaria',
        'BE': 'Belgium',
        'AU': 'Australia',
        'AT': 'Austria',
        'AR': 'Argentina',
        'AE': 'United Arab Emirates'
    }
    big_df = pd.read_csv(csv_name).dropna()
    big_df['country_string'] = big_df.country.map(country_codes)
    return big_df

class Chart_Data:
    def __init__(self, df):
        self.df = df

    def filter_country(self, country_string, df):
        '''
        Filters the dataframe down to a single country code
        '''
        return df[df.country_string == country_string]
    
    def filter_spotify_ids(self, spotify_ids, df):
        filtered_df = df[df.spotify_id.isin(spotify_ids)]
        return filtered_df

    def line_chart(self, df):
        '''
        Returns a line chart of the input df. Uses
        '''
        df['name_artists'] = df['name'] + ' - ' + df['artists']

        fig = px.line(
            x=df.snapshot_date,
            y=df.daily_rank,
            color=df.name_artists,
            template='plotly_dark',

        )

        fig.update_layout(
            yaxis_title="Chart Position",
        )
        # Invert the y-axis
        fig.update_yaxes(autorange="reversed")

        return fig

    def top_n_names_in_df(self,n=10):
        
        '''
        Groups all the names and sums the popularity for that name.
        Returns a three column dataframe:
        name: song_name,
        artists: single artist string or CSV of artists
        popularity: sum values of popularity across all days in data
        '''
        top_names = self.df.groupby(['spotify_id','name', 'artists']).sum('popularity').sort_values(by='popularity', ascending=False)
        df_top_names = top_names.reset_index()
        return df_top_names[['spotify_id','name', 'artists', 'popularity']].head(n)

    def todays_top10(self):
        '''
        Returns the top 10 songs for today of the dataframe. 
        If you give it a dataframe for one region, it will return a 10
        row dataframe
        Returns a dataframe with 10 rows for each value in the 'country' column
        '''
        latest_date = max(self.df.snapshot_date)
        today = self.df[self.df.snapshot_date == latest_date]
        today_top10 = today[today.daily_rank < 11]
        return today_top10[['daily_rank', 'name', 'artists', 'popularity']]

    def slice_artists_names(self):
        '''
        Returns a tuple
        0 is the art_names in the primary position
        1 is the art_names that came after the primary position in one song
        '''
        primaries = []
        secondaries = []

        for entry in self.df.artists:
            if ',' in entry:
                names = [name.strip() for name in entry.split(',')]
                primaries.append(names[0])
                secondaries.extend(names[1:])
            else:
                primaries.append(entry)

        return primaries, secondaries

    def get_sorted_artists(self):
        return sorted(list(set(self.slice_artists_names()[0])))

    def get_sorted_featured_artists(self):
        return sorted(list(set(self.slice_artists_names()[1])))

    def get_top_n_artists(self, n=10):
        prims, secs = self.slice_artists_names()
        name_counter = Counter(prims)
        sec_name_counter = Counter(secs)
        doubler = {i[0]: i[1] for i in name_counter.items()}
        name_counter.update(doubler)

        secs_dict = {i[0]: i[1] for i in sec_name_counter.items()}
        name_counter.update(secs_dict)

        return name_counter.most_common(n)

class Country_Chart_Data(Chart_Data):
    '''
    Depends on that Country_String. The csv only has the country codes
    '''

    def __init__(self, country_string, big_df):
        super().__init__(big_df)  # Call the constructor of the parent class

        # Filter the data for the specific country
        self.country = country_string
        self.df = self.filter_country(country_string, self.df)

        # Compute top 10 songs for the country
        self.df_top_10_songs = self.top_n_names_in_df()
        self.df_top_10_data = self.filter_spotify_ids(
            self.df_top_10_songs.spotify_id, self.df)[[
                'daily_rank',
                'name', 'artists',
                'snapshot_date',
            ]]
        
        # Generate line chart for top 10 songs in the country
        self.fig_top10_song = self.line_chart(self.df_top_10_data)

        # Compute today's top 10 songs for the country
        self.df_today_top10 = self.todays_top10()

        # Get sorted lists of artists and featured artists
        self.artists = self.get_sorted_artists()
        self.featured_artists = self.get_sorted_featured_artists()

        # Get top 10 artists for the country
        self.top_10_artists = self.get_top_n_artists()

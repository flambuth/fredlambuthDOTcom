import json
import os
import nltk

master_genre_grams = {
    'electronic' : ['electronic','house','techno','dub','chill','bass','beat','beats', 'breakbeat', 'electro-industrial','moog','rave','electronica','trance'
    ,'electro', 'clubbing', 'edm', 'club', 'ethnotronica','dnb','dubstep', 'downtempo','vaporwave'
    ,'aussietronica','jungle', 'uk_garage', 'breaks', 'lo-fi', 'idm','bassline','breakcore','indietronica','hi-nrg'],
    
    'pop' : ['pop','dance', 'future', 'idol', 'wave', 'synth', 'glithcore','synthpop', 'anime score','electropop','chiptune', 'post-bop', 'darksynth','disco','post-disco','neo-synthpop','hard bop',
    'bmore','romantic','nederpop','grimewave','glitch','nerdcore','sovietwave'],
    
    'country' : ['country','bakersfield','tejano', 'rockabilly', 'stomp and holler', 'grass'],
    
    'funk' : ['hip','hop','hip hop', 'hip-hop','r&b','rap', 'funk', 'afrofuturism', 'bounce', 'afrobeat', 'brostep','footwork','souldies',
    'bboy','turntabilism','reggae','soul', 'groove','crunk','trap','motown'],
    
    'punk' : ['punk', 'crack', 'riot', 'psychobilly', 'ska', 'post-punk', 'anti-folk','hardcore','post-hardcore','thrash','dance-punk'],
    
    'indie' : ['indie','emo', 'bubblegrunge','psychedelic','ectofolk','alternative','gaze','spacegrunge'] ,
    
    'rock' : ['rock','metal', 'garage', 'invasion', 'surf', 'grunge', 'aggrotech','grindcore','industrial','gothabilly','americana','rock-and-roll','mod', 'rocksteady','proto-metal'],
    
    'old' : ['adult','bossa', 'classical', 'jazz', 'salsa', 'folk', 'vintage', 'early', 'chicha', 'standards', 'doo-wop','composition','norteno','operetta','nortena'
    'exotica', 'blues','bebop', 'organ', 'bolero', 'tradicional', 'listening','mambo','swing','orchestra', 'era','2-step'
    'grupera','chanson', 'boogaloo','bachata','ballroom', 'cubano','mexicano','cumbia','amazonica']
    }


#########
#using migrated data
def new_art_cat():
    with open('new_stuff.json', 'r') as file:
        genre_dict = json.load(file)
    return genre_dict

def new_genres():
    new_stuff = new_art_cat()
    genres_from_new_stuff = [i[3:6] for i in new_stuff]
    flattened_list = [item for sublist in genres_from_new_stuff for item in sublist]
    unique_genres_in_new_stuff = list(set(flattened_list))
    sorted_genres = sorted(unique_genres_in_new_stuff, key=lambda x: (x is None, x))[:-1]
    new_genres_from_new_stuff = [i for i in sorted_genres if i not in My_Genre_Catalog().genre_flat_list]
    return new_genres_from_new_stuff
########################

def my_spotify_genres():
    with open('genres.json', 'r') as file:
        genre_dict = json.load(file)
    return genre_dict

def my_flat_genre_list():
    my_book  = my_spotify_genres()
    flat_list = [i for sublist in my_book.values() for i in sublist]
    return flat_list

class My_Genre_Catalog:
    def __init__(self):
        self.genre_book = my_spotify_genres()
        self.genre_flat_list = my_flat_genre_list()


def find_word_in_dicts(word):
    '''
    Function to see if the input word ISIN the lists that are the values in the genre_dicts()
    Returns a true or false
    '''
    genre_simple = genre_book()

    matches = [i for i in genre_simple if word in genre_simple[i]]
    if len(matches) > 0:
        return matches[0]
    else:
        return 'No Match'

############################

def genre_book():
    '''
    Return the dictionary of the master_genre:genre assignments from the JSON
    '''
    if os.path.exists('genres.json'):
        with open('genres.json', 'r') as myfile:
            data=myfile.read()
        genre_book = json.loads(data)
    
    else:
        genre_book = self.genre_assignment()
        self.write_genres_to_json(genre_book)
    
    return genre_book

def look_in_book(new_genre):
    '''
    Function used when evaluating a new entry to the artist table
    First looks for an explicit string match. Then it tries a function for encountering new genres
    '''
    book = genre_book()

    #returns
    listcomp = [i for i in book if new_genre in book[i]]

    if len(listcomp) > 0:
        return listcomp[0]
    
def new_genre_encounter(self, new_genre):
    '''
    Used when an explicit match for evaluating a genre could not be found
    Breaks the input word into grams. If one of them is in the monograms used in the master_dicts,
    it gets the master_genre that uses that monogram
    '''
    grams = new_genre.split(' ')
    blob = [self.find_word_in_dicts(i) for i in grams if self.find_word_in_dicts(i) != 'No Match']
    if blob:
        #turn this one when we can confirm it works - 20july2022
        #self.add_genre_to_json(new_genre, blob[0])
        return blob[0]
    else:
        return 'Other'
    

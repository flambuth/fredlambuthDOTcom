from app.models.artist_catalog import artist_catalog
from sqlalchemy import func

#latest_art_cats = artist_catalog.query.order_by(artist_catalog.app_record_date.desc()).limit(5).all()

genres = ['electronic', 'pop', 'country', 'hip hop', 'punk', 'indie', 'rock', 'old', 'Other']
alphas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
non_alphas =  non_alphas = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '@', '#', '$', '%', '&', '*', '!', '?', '+', '-', '[']

def latest_art_cats(num=5):
    latest_acs = artist_catalog.query.order_by(artist_catalog.app_record_date.desc()).limit(num).all()
    return latest_acs

def possible_alphas(art_cats_model):
    '''
    Given a flask-sqlAlchemy of artist_catalog, returns a set of all possible charcters for the starting character of each art_name in the art_cat table 
    '''
    art_cats = art_cats_model.query.all()
    all_letters = [i.art_name[0].upper() for i in art_cats]
    unique_chars = list(set(all_letters))
    return sorted(unique_chars, key=lambda x: (not x.isalpha(), x))

def all_art_cats_starting_with(letter):
    
    start_with_letter = artist_catalog.query.filter(artist_catalog.art_name.startswith(letter)).order_by('art_name').all()

    thes = artist_catalog.query.filter(
        func.substring(artist_catalog.art_name,0,5)=='The '
        ).filter(func.substring(artist_catalog.art_name,6,-1).startswith(letter)
                ).order_by('art_name').all()
    
    art_cat_results = start_with_letter + thes
    return art_cat_results

def all_art_cats_in_master_genre(master_genre):
    arts_in_the_genre = artist_catalog.query.filter(artist_catalog.master_genre==master_genre).order_by('art_name').all()
    return arts_in_the_genre
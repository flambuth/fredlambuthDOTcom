import nltk
import json
from collections import Counter

def all_spotify_genres():
    with open('GenreList.txt', 'r') as file:
        lines = file.readlines()
        words = [line.strip() for line in lines]
    return sorted(words)

def my_spotify_genres():
    with open('genres.json', 'r') as file:
        genre_dict = json.load(file)
    return genre_dict

def my_flat_genre_list():
    my_book  = my_spotify_genres()
    flat_list = [i for sublist in my_book.values() for i in sublist]
    return flat_list

def list_of_genre_monograms(genre_list):
    return [nltk.tokenize.word_tokenize(genre) for genre in genre_list]

def bigrams_in_grams(gram_list):
    all_bigrams = [list(nltk.bigrams(i)) for i in gram_list]
    all_bigrams = [i for i in all_bigrams if len(i)>0]
    return all_bigrams

genre_list = all_spotify_genres()
gram_list = list_of_genre_monograms(genre_list)
bigram_list = bigrams_in_grams(gram_list)
flat_bigram_list = [item for sublist in bigram_list for item in sublist]
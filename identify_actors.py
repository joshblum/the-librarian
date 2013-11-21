"""
    Given a list of name tokens perform fuzzy matching
    on the names and find movies for actors that are identified.
    returns a movie title if found.
"""
from constants import TMDB_API_KEY
from utils import ActorDB

from fuzzywuzzy import process
from tmdb import tmdb

MIN_INTERSECTION = 2
MIN_FUZZ_SCORE = 85

tmdb.configure(TMDB_API_KEY)
db = ActorDB()

def identify_actors(clean_text):
    films = set([])
    for name_token in clean_text:
        print 'name:', name_token
        matches = _normalize_text(name_token) #[(actor names, score)]
        print 'matches:', matches
        potential_actors = map(find_films, matches)#[[film_set1, filmset_2, ...], [...]]
        print 'potential_actors:', potential_actors
        if not len(potential_actors):
            continue
        print 'films:', films
        
        films = reduce(merge_sets, potential_actors)#[film_interset1, film_interset2...]
        if len(min(films)) <= MIN_INTERSECTION:
            break

    return min(films)

def _normalize_text(name_token):
    """
        Perform fuzzing matching to try and match name tokens
    """
    print "normalize_text: name_token:", name_token
    choices = map(lambda x: " ".join(x), db.query_name(name_token))
    print 'normalize_text: choices:', len(choices)
    matches = process.extractOne(name_token, choices)
    print 'normalize_text: matches', matches
    if not isinstance(matches, list):
        matches = [matches]
    
    filtered_matches = filter(
        lambda x: x is not None and x[1] > MIN_FUZZ_SCORE, matches)
    print "normalize_text:filtered_matches:", filtered_matches
    return map(lambda x: x[0], filtered_matches)

def find_films(actor_name):
    people = tmdb.People(actor_name)
    return [set([movie.get_original_title() for movie in person.cast()])
            for person in people]

def merge_sets(sets1, sets2):
    """
        merge sets of sets by computing the intersection of each pair
    """
    return filter(lambda x: len(x), [
            s1.intersection(s2) for s2 in sets2
            for s1 in sets1
        ])


if __name__ == "__main__":
    clean_text = ['craig van hook', 'olga merediz', 'eva mendes', 'rev john facci', 'ryan gosling',]
    identify_actors(clean_text)

import requests_with_caching
import json

def get_movies_from_tastedive(s):
    base_url="https://tastedive.com/api/similar"
    params_dict={}
    params_dict["q"]=s
    params_dict["type"]="movies"
    params_dict["limit"]=5
    resp=requests_with_caching.get(base_url, params=params_dict)
    #print(resp.url)
    return resp.json()
 
#result=get_movies_from_tastedive("Tony Bennett")
#print(result)
#result=get_movies_from_tastedive("Black Panther")
def extract_movie_titles(dict):
    movie_title=[]
    for i in range(len(dict['Similar']['Results'])):
        result=dict['Similar']['Results'][i]
        movie_title.append(result['Name'])
    return movie_title
#course 3 final project
def get_related_titles(list):
    related_titles=[]
    for item in list:
        title=extract_movie_titles(get_movies_from_tastedive(item))
        for val in title:
            if val not in related_titles:
                related_titles.append(val)
                
    return related_titles            
    

def get_movie_data(movie_name):
    base_url="http://www.omdbapi.com/"
    params_dict={}
    params_dict["t"]=movie_name
    params_dict["r"]="json"
    res= requests_with_caching.get(base_url, params=params_dict)
    return json.loads(res.text)

def get_movie_rating(d):
    if len(d['Ratings'])>=2 and d['Ratings'][1]['Source']=="Rotten Tomatoes":
        ratings=d['Ratings'][1]['Value']
        if '%' in ratings:
            num=round(float(ratings.strip('%')))
            return num
    else:
        return 0

    
def get_sorted_recommendations(movie_list):
    title_dict={}
    for title in get_related_titles(movie_list):
        title_dict[title]=get_movie_rating(get_movie_data(title))
    return [i[0] for i in sorted(title_dict.items(), key=lambda item: (item[1], item[0]), reverse=True)]
    

result=get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
print(result)

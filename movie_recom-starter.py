import pandas as pd
import numpy as np
from flask import Flask, render_template, request, url_for, redirect
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import urllib.request
import pickle
import requests


def read_file_and_make_similarity_matrix():
    df = pd.read_csv('main_data.csv')
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df['comb'])
    cosine_similarities=cosine_similarity(count_matrix)
    print("Loaded Data Successfully")
    return df, cosine_similarities

def get_recommended_movies(movie_name,numb_of_recom):
    numb_of_recom=int(numb_of_recom)+1
    movie_name=movie_name.lower()
    # print(movie_name)
    df, cosine_simi=read_file_and_make_similarity_matrix()
    if df is None or cosine_simi is None:
        return False, ["Error Fetching Data.Please Try Again Later..."]
    try:
        movie_ind = df.loc[df['movie_title'] == movie_name].index[0]
    except IndexError:
        return False, ["Sorry!!! Cant find the Movie you Requested.Try Later"]
    except Exception:
        return False, ["Error Fetching Data.Please Try Again Later..."]

    lst=list(enumerate(cosine_simi[movie_ind]))
    sorted_lst=sorted(lst, key=lambda x : x[1], reverse=True)
    if numb_of_recom>len(sorted_lst)-1:
        numb_of_recom=len(sorted_lst)-1
    sorted_lst=sorted_lst[1:numb_of_recom]
    recommendations=[]
    for i in range(len(sorted_lst)):
        ind=sorted_lst[i][0]
        recommendations.append(df['movie_title'][ind])
        print(recommendations)
    return True, recommendations


def get_suggestions():
    data = pd.read_csv('main_data.csv')
    return list(data['movie_title'].str.capitalize())


app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('home.html')

@app.route('/')
@app.route('/home')
def suggestions_to_home_page():
    suggestions = get_suggestions()
    # print(suggestions)
    return render_template('home.html', suggestions=suggestions)


@app.route('/similarity', methods=['POST'])
def get_similarities():
    arr=[]
    arr_new=[]
    movie = request.form['name']
    num = request.form['nums']
    print("num is  : "+num)
    type(num)
    nums = num
    stat, rc = get_recommended_movies(movie, nums)
    arr = rc
    # print(rc)
    print('array is : ', arr)
    for i in range(len(arr)):
        arr_new.append(str(i + 1)+ ". "+ arr[i])

    return render_template('recommend.html', title=movie, arr=arr_new) #redirect(url_for('recommend', title=movie, arr=arr))
    # if type(rc)==type('string'):
    #     return rc
    # else:
    #     new_rc = "---".join(rc)
    #     return new_rc


if __name__ == '__main__':
    app.run(debug=True)
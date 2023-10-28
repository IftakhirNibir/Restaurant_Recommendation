from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Restaurant_DB

# Create your views here.

def homepage(request):
    return render(request,"homepage.html")

def recommendation_page(request):
    try:
        if request.method == "POST":
            value = request.POST.get('input')
            value = value.strip()  #To remove extra space 
            restaurant_names = []
            filtered_rows = []
            res = pd.read_csv("res.csv",encoding='cp1252')
            # sentiment_counts_df = pd.read_csv("sentiment_counts.csv")
            sentiment_counts_df = pd.read_csv("try_address.csv")
            cv = CountVectorizer(max_features=5000,stop_words='english')
            vectors = cv.fit_transform(res['tags']).toarray()
            similarity = cosine_similarity(vectors)
            index = res[res['main_cuisine'].str.lower() == value.lower()].index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            recommended_restaurants = set()
            for i in distances:
                restaurant_index = i[0]
                main_cuisine = res.iloc[restaurant_index].main_cuisine
                recommended_restaurants.add(res.iloc[restaurant_index]['name'])
                if len(recommended_restaurants) >= 10:
                    break
            for restaurant_name in recommended_restaurants:
                restaurant_names.append(restaurant_name)
            restaurant_namess = restaurant_names
            for restaurant_name in restaurant_namess:
                filtered_row = sentiment_counts_df[sentiment_counts_df['Restaurant Name'] == restaurant_name]
                filtered_rows.append(filtered_row)
            filtered_df = pd.concat(filtered_rows)
        else:
            filtered_df = pd.DataFrame()
        filtered_df = filtered_df.values.tolist()
        return render(request,'recommendationpage.html',{'rows': filtered_df})

    except Exception as e:
        error_text = "There is an error, please check the input value again"
        return render(request,'recommendationpage.html',{'error_message': error_text})

def trending(request):
    search_restaurent = request.GET.get('restaurant', '')
    search_address = request.GET.get('address','')

    restaurant_db = Restaurant_DB.objects.all()

    if search_restaurent:
        restaurant_db = restaurant_db.filter(name__icontains=search_restaurent)

    if search_address:
        restaurant_db = restaurant_db.filter(address__icontains=search_address)
    
    if request.method == "POST":
        selected_value = request.POST.get('one')
        s = int(selected_value)
        df = pd.read_csv('popularity.csv')
        a = df.values.tolist()
        a = a[:s]
    else:
        df = pd.read_csv('popularity.csv')
        a = df.values.tolist()
        a = a[:5]  # Provide an empty list as a fallback when no form submission occurs
    return render(request, 'trending.html', {'rows': a,
            'restaurant_db': restaurant_db,
            'search_restaurent': search_restaurent, 
            'search_address': search_address,})


def recommendation2_page(request, restu):
    try: 
        value = restu
        value = value.strip()  #To remove extra space 
        restaurant_names = []
        filtered_rows = []
        res = pd.read_csv("res.csv",encoding='cp1252')
        # sentiment_counts_df = pd.read_csv("sentiment_counts.csv")
        sentiment_counts_df = pd.read_csv("try_address.csv")
        cv = CountVectorizer(max_features=5000,stop_words='english')
        vectors = cv.fit_transform(res['tags']).toarray()
        similarity = cosine_similarity(vectors)
        index = res[res['name'] == value].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_restaurants = set()
        for i in distances:
            restaurant_index = i[0]
            main_cuisine = res.iloc[restaurant_index].main_cuisine
            recommended_restaurants.add(res.iloc[restaurant_index]['name'])
            if len(recommended_restaurants) >= 10:
                break
        for restaurant_name in recommended_restaurants:
            restaurant_names.append(restaurant_name)
        restaurant_namess = restaurant_names
        for restaurant_name in restaurant_namess:
            filtered_row = sentiment_counts_df[sentiment_counts_df['Restaurant Name'] == restaurant_name]
            filtered_rows.append(filtered_row)
        filtered_df = pd.concat(filtered_rows)
        filtered_df = filtered_df.values.tolist()
        return render(request,'recommendationpage2.html',{'restu':value,'rows': filtered_df})

    except Exception as e:
        error_text = "Not found any"
        return render(request,'recommendationpage2.html',{'error_message': error_text})
    
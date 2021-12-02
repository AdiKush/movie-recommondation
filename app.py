import numpy as np 
import pandas as pd
from flask import Flask,request,jsonify,render_template
import joblib
app=Flask(__name__)
# model=joblib.load("bmi.pkl")
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    columns_names = ["user_id", "item_id", "rating","timestamp"] 
    df= mydata=pd.read_csv(r"u.data",sep='\t', names=columns_names)
    # pd.read_csv(r"D:\dataset\ml-100k\u.item",sep='\|', header= None)
    movies_titles = pd.read_csv(r"u.item",sep='\|', header= None)
    movies_titles = movies_titles[[0,1]]
    movies_titles.columns=['item_id','title']
    #now we need to merge two data frames(df, movies_titles) so we use merge function
    df = pd.merge(df, movies_titles, on="item_id")
    df.groupby('title').mean()
    #we need rating then
    df.groupby('title').mean()['rating']
    #to get highest rating
    df.groupby('title').mean()['rating'].sort_values(ascending=False).head()
    #which movie watched maximum number of time
    df.groupby('title').count()['rating'].sort_values(ascending=False)
    ratings = pd.DataFrame(df.groupby('title').mean()['rating'])
    ratings['number of ratings'] = pd.DataFrame(df.groupby('title').count()['rating'])
    ratings.sort_values(by='rating', ascending =False)
    moviemat=df.pivot_table(index="user_id",columns="title", values="rating")
    ratings.sort_values('number of ratings', ascending=False)

    movie_name=request.form['movie']

    movie_user_ratings= moviemat[movie_name]
    similar_to_movie = moviemat.corrwith(movie_user_ratings)
    corr_movie=pd.DataFrame(similar_to_movie, columns=['Correlation'])
    corr_movie.dropna(inplace=True)
    corr_movie =corr_movie.join(ratings['number of ratings'])
    predictions = corr_movie[corr_movie['number of ratings']>100].sort_values('Correlation',ascending=False)

    predictions.drop('Correlation',axis=1)
    r=predictions.drop("number of ratings",axis=1)
    r1=r.drop("Correlation",axis=1)
    r2=r1.head().index.tolist()

   

    
    

    return render_template("index.html", prediction_text="Recomended movies are \n   {}".format(r2))








    # int_features = [int(x) for x in request.form.values()]
    # final_features = [np.array(int_features)]
    # prediction = model.predict(final_features)

    # output = round(prediction[0], 2)
    # #print(output)
    # index_target=pd.Series(["Extremely Weak","Weak" ,"Normal" ,"Overweight","Obesity" ,"Extreme Obesity"])
    # result=index_target[output]
    #result=list(result.values)
    #result=str(result)
    # return render_template('index.html', prediction_text='Predicted BMI  {}'.format(result))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    movie = request.get_json(force=True)
    prediction = predict()
    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
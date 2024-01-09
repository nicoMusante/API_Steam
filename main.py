from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

app=FastAPI()

games_and_reviews=pd.read_csv("ETL/games_and_reviews.csv")
games_and_reviews=games_and_reviews.iloc[:, 1:]


""" def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013} """
@app.get('/añomaxgenero/{genero}')
def PlayTimeGenre( genero : str ):
    #primero validamos que el genero que se introdujo está efectivamente en el dataframe 
    #lo tomamos como valido si todas las letras coinciden sin importar las mayúsculas y minúsculas
    if (genero.lower() not in map(str.lower, games_and_reviews.columns)):
        return "El genero proporcionado no se encuentra en el servidor" #respuesta en caso de que se haya introducido un genero que no se encuentra en el dataframe
        #esta Api no se va a utilizar en una aplicación luego, pero si así ocurriese 
        # podríamos retornar una respuesta más genérica como: return -1 
    
    #obtenemos el nombre de la columna original correspondiente a genero-lower()
    columna_original = next(column for column in games_and_reviews.columns if column.lower() == genero.lower())
    
    #filtramos el DataFrame por el género específico
    df_genero = games_and_reviews[games_and_reviews[columna_original] == 1]

    #encontramos el año de lanzamiento con más horas jugadas
    año_max_horas = df_genero.groupby('posted_year')["playtime_forever"].sum().idxmax()

    return f"El año de lanzamiento con más horas jugadas para el género '{genero}' es: {año_max_horas}"
    #tambien podríamos retornar algo mas genérico como: return año_max_horas

#con estos 2 endpoints validamos que se haya ingresado un género a travez de la url
@app.get('/añomaxgenero/')
def falta_de_parametros():
    return "Debe proporcionarse un género desarrolladora para recibir una respuesta del servidor"
        

@app.get('/añomaxgenero')
def falta_de_parametros2():
    return "Debe proporcionarse una género desarrolladora para recibir una respuesta del servidor"




""" def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}"""
@app.get('/usermaxgenero/{genero}')
def UserForGenre( genero : str ):
    #primero validamos que el genero que se introdujo está efectivamente en el dataframe 
    #lo tomamos como valido si todas las letras coinciden sin importar las mayúsculas y minúsculas
    if (genero.lower() not in map(str.lower, games_and_reviews.columns)):
        return "El genero proporcionado no se encuentra en el servidor" #respuesta en caso de que se haya introducido un genero que no se encuentra en el dataframe
        #esta Api no se va a utilizar en una aplicación luego, pero si así ocurriese 
        # podríamos retornar una respuesta más genérica como: return -1 
        
    #obtenemos el nombre de la columna original correspondiente a genero-lower()
    columna_original = next(column for column in games_and_reviews.columns if column.lower() == genero.lower())    
        
    #filtramos el dataframe por el genero que se introdujo
    df_genero=games_and_reviews[games_and_reviews[columna_original]==1]

    #agrupamos por usuario y sumar las horas jugadas para cada usuario
    user_playtime = df_genero.groupby('user_id')['playtime_forever'].sum()

    #encontramos el usuario con más horas jugadas
    max_user = user_playtime.idxmax()

    #agrupamos por año y sumar las horas jugadas para cada año
    year_playtime = df_genero.groupby('posted_year')['playtime_forever'].sum()

    return max_user, year_playtime.tolist()

#con estos 2 endpoints validamos que se haya ingresado un género a travez de la url
@app.get('/usermaxgenero/')
def falta_de_parametros3():
    return "Debe proporcionarse un género para recibir una respuesta del servidor"
        

@app.get('/usermaxgenero')
def falta_de_parametros4():
    return "Debe proporcionarse una género para recibir una respuesta del servidor"



""" def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}] """
@app.get('/masjugadosaño/{anio}')
def UsersRecommend( anio : int ):
    #primero validamos que el año que se introdujo está efectivamente en el dataframe 
    if anio not in games_and_reviews['posted_year'].unique():
        return "El año proporcionado no se encuentra en el servidor" #respuesta en caso de que se haya introducido un año que no se encuentra en el dataframe
        #esta Api no se va a utilizar en una aplicación luego, pero si así ocurriese 
        # podríamos retornar una respuesta más genérica como: return -1 
    
    #filtramos el DataFrame para obtener solo las filas del año especificado y con recomendaciones positivas/neutrales
    year_df = games_and_reviews[(games_and_reviews['posted_year'] == anio) & (games_and_reviews['recommend'] == True)]

    #agrupamos por juego y contar el número de recomendaciones
    game_recommendations = year_df.groupby('title')['recommend'].sum()

    #ordenamos en orden descendente y obtener el top 3
    top_3_games = game_recommendations.sort_values(ascending=False).head(3)

    return top_3_games.index.tolist()

#con estos 2 endpoints validamos que se haya ingresado un año a travez de la url
@app.get('/masjugadosaño/')
def falta_de_parametros5():
    return "Debe proporcionarse un año para recibir una respuesta del servidor"
        

@app.get('/masjugadosaño')
def falta_de_parametros6():
    return "Debe proporcionarse un año para recibir una respuesta del servidor"



""" def UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}] """
@app.get('/empresasminaño/{anio}')
def UsersWorstDeveloper( anio : int ):
    #primero validamos que el año que se introdujo está efectivamente en el dataframe 
    if anio not in games_and_reviews['posted_year'].unique():
        return "El año proporcionado no se encuentra en el servidor" #respuesta en caso de que se haya introducido un año que no se encuentra en el dataframe
        #esta Api no se va a utilizar en una aplicación luego, pero si así ocurriese 
        # podríamos retornar una respuesta más genérica como: return -1 

    #filtramos el DataFrame para obtener solo las filas del año especificado y con recomendaciones negativas
    year_df = games_and_reviews[(games_and_reviews['posted_year'] == anio) & (games_and_reviews['recommend'] == False)]

    #agrupamos por desarrolladora y contar el número de recomendaciones negativas
    developer_malas_recomendaciones = year_df.groupby('developer')['recommend'].sum()

    #ordenamos en orden ascendente y obtener el top 3
    top_3_developers = developer_malas_recomendaciones.sort_values(ascending=True).head(3)

    #finalmente ajustamos la respuesta de la función para que quede en el formato pedido
    result_list = [{"Puesto " + str(i+1): developer} for i, developer in enumerate(top_3_developers.index)]

    return result_list

#con estos 2 endpoints validamos que se haya ingresado un año a travez de la url
@app.get('/empresasminaño/')
def falta_de_parametros7():
    return "Debe proporcionarse un año para recibir una respuesta del servidor"
        

@app.get('/empresasminaño')
def falta_de_parametros8():
    return "Debe proporcionarse un año para recibir una respuesta del servidor"



""" def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]} """
@app.get('/opinionesempresa/{empresa_desarrolladora}')
def sentiment_analysis_by_developer(empresa_desarrolladora: str):

    #validamos que la empresa desarrolladora que se introdujo está efectivamente en el dataframe 
    if empresa_desarrolladora.lower() not in games_and_reviews['developer'].str.lower().unique():
        return "La empresa desarrolladora proporcionada no se encuentra en el servidor" #respuesta en caso de que se haya introducido una empresa desarrolladora que no se encuentra en el dataframe
        #esta Api no se va a utilizar en una aplicación luego, pero si así ocurriese 
        # podríamos retornar una respuesta más genérica como: return -1 
    
    #filtramos el DataFrame por la empresa desarrolladora proporcionada
    dev_df = games_and_reviews[games_and_reviews['developer'].str.lower() == empresa_desarrolladora.lower()]

    #calculamos la cantidad total de registros para cada valor de 'sentiment_score'
    sentiment_counts = dev_df['sentiment_score'].value_counts().to_dict()

    #nos aseguramos de que todos los valores posibles estén presentes en el diccionario
    for score in range(3):
        sentiment_counts.setdefault(score, 0)

    #creamos el diccionario final en el formato solicitado
    result_dict = {
        empresa_desarrolladora: {
            "Negative": sentiment_counts[0],
            "Neutral": sentiment_counts[1],
            "Positive": sentiment_counts[2]
        }
    }

    return result_dict

#con estos 2 endpoints validamos que se haya ingresado una empresa desarrolladora a travez de la url
@app.get('/opinionesempresa/')
def falta_de_parametros9():
    return "Debe proporcionarse una empresa desarrolladora para recibir una respuesta del servidor"
        

@app.get('/opinionesempresa')
def falta_de_parametros10():
    return "Debe proporcionarse una empresa desarrolladora para recibir una respuesta del servidor"



# preparamos los datos para entrenar el modelo de machine learning
games_and_reviews.fillna(0, inplace=True)  # Asegurarse de que no hay valores nulos

#esleccionamos columnas de género
genre_columns = ["Action",	"Casual", "Indie",	"Simulation", "Strategy", "Free to Play", "RPG", "Sports", "Adventure", "Racing","Early Access", "Massively Multiplayer", "Animation &amp; Modeling", "Video Production", "Utilities", "Web Publishing", "Education", "Software Training", "Design &amp; Illustration", "Audio Production", "Photo Editing", "Accounting"] 
game_features = games_and_reviews.set_index('item_id')[genre_columns]

#noremalizamos las características
scaler = StandardScaler()
game_features_scaled = scaler.fit_transform(game_features)

#calculamos similitud coseno
cosine_sim = cosine_similarity(game_features_scaled)

#mapeamos índices y títulos
indices = pd.Series(games_and_reviews.index, index=games_and_reviews['item_id']).drop_duplicates()

""" def recomendacion_juego( id de producto ): Ingresando el id de producto, deberíamos recibir una lista 
con 5 juegos recomendados similares al ingresado. """
@app.get("/recomendacionjuego/{idJuego}")
def recomendacion_juego(idJuego: int):
    # verificamos si el ID del juego existe en el dataset
    if idJuego not in indices:
        return "El ID del juego no existe en el dataset."

    idx = indices[idJuego]
    sim_scores = list(enumerate(cosine_sim[idx].flatten()))  # Aplanar el array
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    game_indices = [i[0] for i in sim_scores]
    return games_and_reviews['title'].iloc[game_indices].tolist()


#con estos 2 endpoints validamos que se haya ingresado un id de un juego a travez de la url
@app.get('/recomendacionjuego')
def falta_de_parametros11():
    return "Debe proporcionarse un id de un juego para recibir una respuesta del servidor"
        

@app.get('/recomendacionjuego/')
def falta_de_parametros12():
    return "Debe proporcionarse un id de un juego para recibir una respuesta del servidor"
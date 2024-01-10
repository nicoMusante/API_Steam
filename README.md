
# Proyecto Individual Machine Learning Operations: Plataforma de juegos

## Descripción
Este proyecto de ciencia de datos se centra en el análisis de un conjunto de datos de una plataforma de juegos en línea, similar a Steam. El objetivo es realizar un ETL (Extracción, Transformación y Carga), un EDA (Análisis Exploratorio de Datos), desarrollar una API para interactuar con los datos limpios, y entrenar un modelo de machine learning. A través de este proyecto, se buscan insights sobre las preferencias de los jugadores, tendencias en géneros de juegos, y la dinámica de las reseñas. El modelo de machine learning tiene como finalidad aprovechar estos datos para predecir tendencias o comportamientos futuros, proporcionando una herramienta valiosa para análisis más profundos y toma de decisiones basada en datos.

## Tecnologías Utilizadas
- Python
- Pandas para manipulación de datos
- Matplotlib y Seaborn para graficación de datos
- Scikit Learn para entrenar un modelo de Machine Learning
- Fast Api y Uvicorn para levantar la api

## Instalación y Configuración

1.Abrir una Terminal o Línea de Comandos: Necesitarás una ventana de terminal (en Linux o macOS) o línea de comandos (en Windows) para ejecutar los comandos de instalación.

2.Navegar al Directorio del Archivo requirements.txt. Por ejemplo, si tu archivo está en el escritorio, el comando podría ser algo como:
```bash
cd "ruta/de/proyecto"
``` 

3.Ejecutar el Comando de Instalación: Una vez en el directorio correcto, utiliza el siguiente comando para instalar todas las librerías listadas en tu requirements.txt:
```bash
pip install -r requirements.txt 
```

## Uso del proyecto

Para poder consumir la API simplemente hay que levantarla de forma local con el siguiente comando: 
```bash
uvicorn main:app --reload
```

## Estructura del Proyecto

ETL_Notebooks: Noteebooks que se utilizaron para poder realizar el ETL.
EDA/: Archivos con los cuales se hace el analisis exploratorio de datos con el dataset mergeado completo y el dataset acotado con el cual se realizan las consultas de la API.
main.py: Código fuente para la API con los endpoints y todas las funciones que se necesitan para responder las consultas de la misma.
games_and_reviews_sample.csv: dataset que se utiliza para responder a las consultas de la API.
repo_consigna/: este es el repositorio clonado que contiene la consigna que se desarrolla en este proyecto. 
README.md: Este es el archivo que estás leyendo que explica lo básico del proyecto.

## Dataset en Google Drive  

Estas carpetas están disponibles en el siguiente Google Drive: 
"https://drive.google.com/drive/folders/19aK4zBYt-Da0zdX_-ZYz9YpiOIZ52C9W?usp=drive_link"
Dataset_Completo/: todos los archivos con datos originales de los que se disponían para hacer el proyecto
Dataset_ETL/: archivos limpios producto de los notebooks de la carpeta "ETL_Notebooks"

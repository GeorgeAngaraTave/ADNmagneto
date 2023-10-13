



# Descripción
Este sistema, describe el uso y puesta a punto de una **Api rest** usando [**Python**](https://www.python.org/downloads/) y [**Flask**](https://palletsprojects.com/p/flask/)



# Requisitos
- [**Python**](https://www.python.org/downloads/) 3.7.x
- [**virtualenv**](https://virtualenv.pypa.io/en/stable/) (Recomendado)


## Instalación de este repositorio
Clonar este repositorio y alojarlo en una carpeta conveniente.

    git clone git@gitlab.geovisor.com.co:Servinformacion/BackEndBase.git

Se recomienda usar [**virtualenv**](https://virtualenv.pypa.io/en/stable/) para desarrollo y pruebas.


## Activar virtualenv en entornos Gnu/Linux, Mac OS

```sh
$ virtualenv --python python3 env ó python -m virtualenv env
$ source env/bin/activate
```


## Instalar las dependencias
Una vez dentro del entorno, instalar las dependencias:

```sh
(env) $ pip install -r requirements.txt
```


# Iniciando el servidor web
A continuación se describen algunas configuraciones para iniciar el servidor web.


## Usando Flask run (Recomendado)

```sh
(env) $ flask run
```

## Usando python

```sh
(env) $ python main.py
```

## Usando gunicorn

```sh
(env) $ pip install gunicorn
```

```sh
(env) $ gunicorn --bind 0.0.0.0:6969 --reload --log-level debug main:app
```


## Desplegar en Google App Engine

### Usando gcloud deploy

```sh
(env) $ gcloud app deploy --project PROJECT_ID --version VERSION_ID --no-promote
```

### Usando gcloud build
```sh
(env) $ gcloud builds submit .
```

ó especificando un archivo de construcción personalizado.

```sh
(env) $ gcloud builds submit --config cloudbuild.yaml .
```

>La direccion y el puerto por defecto es: [**http://localhost:6969**](http://localhost:6969)

# Descripción de la solución

- Se utilizo para el desarrollo la versión de Python 3 con el fireware Flask
- Base de datos utilizada una Cloud SQL de google cloud platform 
- Proyecto desplegado en la nuebe Google app engine
- Copia da la base de datos en la ruta (**asset/dbBuild/proyectos.sql**)



# ** Servicios solución Magneto **

**Appengine URL** : https://magneto-dot-invertible-eye-316323.uc.r.appspot.com

## **Verificar ADN:**

Validar ADN, si es mutante ó humano

**URL** : `/api/mutant`

**Method** : `POST`

**Data constraints**

```json
{

    "adn": ["ATGCGA","CAGTGC","TTATTT","AGACGG","GCGTCA","TCACTG"]

}
``` 
*   *"adn"*: **Array con cadenas de ADN**

### Success Response

**Condition** : Si la acción se completó satisfactoriamente.

**Code** : `200 OK`

**Content example**

```json
{
  "data": "Is  mutant",
  "message": "success!",
  "status": 200
}
```

### Fail Response

**Condition** : Si la acción falló.

**Code** : `403 Forbidden`

**Content example**

```json
{
  "data": "Is not mutant",
  "message": "you don't have permission to access the requested resource.",
  "status": 403
}
```
## **Estadísticas:**

Devuelve un Json con las estadísticas de las verificaciones de ADN

**URL** : `/api/stats`

**Method** : `GET`


### Success Response

**Condition** : Si la acción se completó satisfactoriamente.

**Code** : `200 OK`

**Content example**

```json
{
  "data": {
    "count_human_dna": 2,
    "count_mutant_dna": 3,
    "ratio": 0.7
  },
  "message": "success!",
  "status": 200
}
```










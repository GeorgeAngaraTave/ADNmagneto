# firebase-export

## Requisitos
Para la ejecución correcta de estos scripts, se requiere que esté activado el entorno (**env**), y las dependencias del **BackEndBase** instaladas.

Sí se desea utilizar este script fuera del entorno del **BackEndBase**, las dependencias utilizadas son:

- [Click](https://github.com/pallets/click)
- [firebase-admin](https://github.com/firebase/firebase-admin-python)
- [google-cloud-firestore](https://github.com/googleapis/python-firestore)
- [cuenta de servicio de Google Cloud](https://cloud.google.com/docs/authentication/getting-started).

> Recuerda definir una variable de entorno en el S.O., que tenga la ruta de una [cuenta de servicio](https://cloud.google.com/docs/authentication/getting-started).


**Ejemplo:**

```sh
$ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```


## Uso
Permite exportar datos de Firestore a un archivo json.

**Parámetros:**

```sh
Usage: firebase-export.py [OPTIONS]

  allow export data from Firestore.

Options:
  -f, --file PATH             file to export.  [required]
  -c, --collection-list TEXT  Collections list to export  [required]
  -e, --exclude-list TEXT     Collection list to exclude (default: None)
  -v, --version               show current version and exit.
  -h, --help                  Show this message and exit.
```

**Ejemplos:**

- Exportando todo por defecto (permite exportar toda la base de datos)
```sh
(env) $ python ./tools/firebase-export.py -f final2.json -c all
```

- Excluyendo Colecciones (las colecciones definidas no se exportarán)
```sh
(env) $ python ./tools/firebase-export.py -f final2.json -c all -e Groups Roles
```

- Definiendo Colecciones a exportar (solo se exportarán las colecciones definidas)
```sh
(env) $ python ./tools/firebase-export.py -f final2.json -c Users Cities Companies
```

**Salida:**

```sh
python ./tools/firebase-export.py -f export.json -c all
file name: export.json
collections list: ['all']
exclude collections list: []

export all collections
export_method all
obteniendo listado de colecciones...

Se iniciara el export de las colecciones...
> ['Cities', 'Companies', 'Countries', 'Departments', 'Groups', 'Locales', 'OauthClients', 'Roles', 'Sessions', 'Status', 'Uploads', 'Users', 'Versions']

Continue? [Yy/Nn]
checking...
downloading collection Cities...
downloading collection Companies...
downloading collection Countries...
downloading collection Departments...
downloading collection Groups...
downloading collection Locales...
downloading collection OauthClients...
downloading collection Roles...
downloading collection Sessions...
downloading collection Status...
downloading collection Uploads...
downloading collection Users...
downloading collection Versions...

Downloaded 13 collections, 9522 documents...

now writing 2080600 json records to export.json...
please wait...

the process has been successfully completed!.
Press any key to continue ...
```


**Estructura del archivo de salida (ejemplo)**

```json
{
    "Locales": {
        "15UMU057Jcjnv5GghXod": {
            "code": "es",
            "created_at": "20190704175309",
            "name": "spanish",
            "status": "Active"
        },
        "eymTKRkGpgU0P2XGEO2u": {
            "code": "en",
            "created_at": "20190704175315",
            "name": "english",
            "status": "Active"
        },
        "x5YXbekZAMlZOz34sMQt": {
            "code": "fr",
            "created_at": "20190704175303",
            "name": "french",
            "status": "Active"
        }
    },
    "Status": {
        "NKYuYBQlFQV0sBCJCMwN": {
            "created_at": "20190704174146",
            "name": "ACTIVE"
        },
        "QD3EYS6q9KnAIFHp7z6n": {
            "created_at": "20190704174150",
            "name": "INACTIVE"
        },
        "xpm1WS8ZioJcyZKIvSs0": {
            "created_at": "20191117162327",
            "name": "DELETED"
        }
    }
}
```

La salida del script, es un archivo con estructura json, que contiene cada colección y sus documentos, siguiendo la estructura descrita a continuación:

```json
{
    "nombre de la coleccion":{
        "ID del documento":{
            "campos": "valores"
        }
    }
}
```


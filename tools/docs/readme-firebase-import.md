# firebase-import

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
Permite importar datos a traves de archivos csv, a Firestore.

Utiliza la estructura del archivo csv (cabeceras), para generar un json array e importarlo de forma masiva a Firestore.


**Parámetros:**

```sh
Usage: firebase-import.py [OPTIONS]

  allow import data to Firestore.

Options:
  -f, --file PATH        file to import.  [required]
  -c, --collection TEXT  Collection name  [required]
  -a, --auto TEXT        Specifying auto generated Document ID. (default: yes)
  -p, --prefix TEXT      Collection prefix (default: None)
  -d, --delimiter TEXT   default file delimiter (default: ;)
  --help                 Show this message and exit.
```

**Ejemplo:**

```sh
(env) $ python ./tools/firebase-import.py -f countries.csv -c Countries -d ','
```

**Salida:**

```sh
firebase-import: import data to Firestore
file path: countries.csv
Collection name: Countries
prefix: None
Document ID: True
default delimiter for the file: ,

Continue? [Yy/Nn] Y
checking...
Loading 492 records...
Loading data...  [####################################]  100%

the process has been successfully completed!.
Press any key to continue ...
```

**Estructura del archivo de muestra**

| name          | lang  | iso    | iso3  | phone_code|
| ------------- |:-----:|:-----: |:-----:|:---------:|
| Afganistán    | es    | AF     | AFG   | +93       |
| Albania       | es    | AL     | ALB   | +355      |
| Alemania      | es    | DE     | DEU   | +49       |

**Estructura generada:**

```json
[
  {
    "name": "Afganistán",
    "lang": "es",
    "iso": "AF",
    "iso3": "AFG",
    "phone_code": "+93"
  },
  {
    "name": "Albania",
    "lang": "es",
    "iso": "AL",
    "iso3": "ALB",
    "phone_code": "+355"
  },
  {
    "name": "Alemania",
    "lang": "es",
    "iso": "DE",
    "iso3": "DEU",
    "phone_code": "+49"
  }
]
```


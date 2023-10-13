
Sistema base para el desarrollo de Back-End's usando Python

codename: **Lilith**


# BackenBase

## 3.0.0 release (2020-06-09T17:01:25)

### New
- upgrade modules
    - Click 7.1
    - Flask 1.1.2
    - Werkzeug 1.0.0
    - SQLAlchemy 1.3.17
    - Flask-RESTful 0.3.8
    - Jinja2 2.11.1
    - psycopg2-binary 2.8.5
    - six 1.14.0
    - python-dateutil 2.8.1
    - python-dotenv 0.10.5
    - Flask-Caching 1.8.0
    - sendgrid 6.1.1
    - firebase-admin 3.2.1
    - google-cloud-firestore 1.6.2
    - google-cloud-tasks 1.2.1
    - google-cloud-storage 1.25.0
    - google-cloud-bigquery 1.23.1
    - jsonschema 3.2.0
- new modules
    - **flask_caching**
    - **jsonschema**
- upgrade to **Flask 1.1.2**
- method `get_all_collections` (**firestore_model module**)
- method `multi_save` (**firestore_model module**)
- method `delete_collection` (**firestore_model module**)
- view `ViewSchema` (using **firestore_model module**)
- method `get_schema` (**generic_model module**)
- method `delete_table` (**generic_model module**)
- method `where_` (**generic_model module**)
- method `multi_save` (**generic_model module**)
- function `create_task` for handle Google Cloud Task Queues
- decorator `validate_schema` to validate schema using **jsonschema**
- `save` method (**firestore_model module**) return **firestore id**
- `create_job` and `get_job` functions (**cartodb module**)
- new profile `ADMINISTRATOR` (**security/auth_profiles**)
- change keys, `SECRET_KEY`, `CSRF_SESSION_KEY`, `hash_key` (**crypto module**)
- `get_list_users` method (**firestore_auth module**)
- decorators `require_json_content_type` and `get_header_content_type` (**security/auth module**)

### Fix
- change database driver to `pymysql` (**databases/google_cloud**)
- change logo, now using from (https://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png)
- now use `string` instead `int` (**app/departments/urls**)
- fix support python 3.x (**cartodb module**)
- `SESSION_EXPIRE_TIME` (**local_settings**) it's 6 hours now
- a new endpoint **/api/upload/legacy** is created, for file uploads directly to the App engine, `view_uploads` now only stores the information of a previously loaded file
- `clean_string` (**utils/commons**)
- `sanity_check` (**utils/commons**) function has new parameters
- `save_file` (**google_storage module**) function has new parameters
- fix `get_file` function (**google_storage module**) is a static method
- fix support python 3.x (**servinf module**)
- `check_current_session` (**security/sessions**) function has new parameters
- many bug fixeds on **firebase/realtime** module
- update **geo_hash** lib (**firebase/geo_hash module**) from https://github.com/vinsci/geohash
- `select_from_view` (**generic_model**) function has new parameters
- rename module ~~APICom~~ as IPCOM (**ext/sms module**)
- now the http status 403 (forbidden) is used in some cases
- many fixes and improvements

### Removed
- **werkzeug.contrib.cache** in favor of using **flask_caching**
- remove `get_header_api_key` in favor of `get_header_content_type` (**security/auth module**)
- remove `obtain_key_token`(**security/auth module**)

### Experimental
- proposal added simple dict to save on `multi_save` method (**firestore_model module**)
- the `task_queue` function (**task_queue module**), can receive the data from Pub/Sub or from a service

### Deprecated
- The DataStore module (**NDBModel**) is now deprecated, it is recommended to switch to [Firestore](https://cloud.google.com/datastore/docs/upgrade-to-firestore) (**FirestoreModel**) or to a relational database (**GenericModel**). *Will be removed from future versions.*
- The google_mail module (**sendEmail**) is now deprecated, it is [recommended to use a third party email provider](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrating-services#mail) such as [**SendGrid**](https://sendgrid.com/docs/API_Reference/index.html), Mailgun or Mailjet. All these services offer API's to send emails from applications. *Will be removed from future versions.*

### Thanks To
- **Jeisson.romero**
- **gabriel.jimenez**
- **gabriel.rodriguez**


## 3.c release (2020-03-16T21:28:52)

### New
- upgrade modules
    - Flask 1.0.4
    - Werkzeug 0.16.0
    - Flask-Cors 3.0.8
    - Jinja2 2.10.3
    - MarkupSafe 1.1.1
    - psycopg2-binary 2.8.4
    - SQLAlchemy 1.2.19
    - Flask-SQLAlchemy 2.4.1
    - python-dotenv 0.10.3
    - firebase-admin 2.18.0
    - google-cloud-firestore 1.6.0
    - google-cloud-tasks 1.2.0
    - google-cloud-storage 1.23.0
    - google-cloud-bigquery 1.23.0
    - xlrd 1.2.0
- new method `big_response` (**bigquery module**)
- new request function `after_request` (**main function**)
- new env var `DATABASE_PREFIX`
- `MIN_PASSWORD_LENGTH` set to 6
- new method `deleteFields` (**firestore_model module**)
- now check `GOOGLE_APPLICATION_CREDENTIALS` env var before run
- new tool **firebase-import** to import data to firestore
- new tool **firebase-export** to export data from firestore
- change keys, `SECRET_KEY`, `CSRF_SESSION_KEY`, `hash_key` (**crypto module**)


### Fix
- prints and Exceptions (**generic_model module**)
- fix methods `to_json` `sanity_check` (**commons module**)
- validate key and select_fields (**firestore_model module**)
- fix methods `response`, `send_query` (**bigquery module**)
- roles is defined as plural (**urls roles**)
- now using uuid param, and validate this (**view_users views**)
- many bug fixeds


## 3.b release (2019-10-04T12:17:30)

### New
new modules:
- `auth`
- `cities`
- `companies`
- `countries`
- `departments`
- `locales`
- `oauth_clients`
- `roles`
- `status`
- `users`
- new construction system using [Google Cloud Build](https://cloud.google.com/cloud-build)
- experimental support for continuous integration, using [GitLab CI](https://about.gitlab.com/product/continuous-integration)
- fast execution in development environments using [Flask Run](https://flask.palletsprojects.com/en/1.0.x/server) (**strongly recommended for development**)
- new module for the use of Firestore Auth, Database and RealTime
- Support for sending SMS using Aldeamo and ~~APICom~~ IPCOM
- support for version 2 of the CartoDB Api
- now the `.flaskenv` file is used for configuration and development in local environments

### Fix
- `uploads` module
- `sessions` module
- BigQuery Client
- Storage Client
- SendGrid module
- GKE support using Dockerfile
- MemCached module using GAE and custom servers
- configuration of database engines in GCP

### Removed
- Google Api Client (Discovery)
- Google Mail Api
- Python 2.x support
- logs and messages used to debug on the command line.


## 3.a release (2019-06-22T12:23:03)

### New
- Since the last version (2.1), we have added numerous functionalities, and corrected many errors.
The most important change is the step to Python 3.x (3.7.x), use Firestore as the main Database engine, use of the BigQuery and Cloud Storage client, and use SenGrid as the mail sending engine (deprecating to Google Mail Api).
- New preloaded modules, reorganization of the Sessions, registration and user login.


## 2.1 release (2018-10-24T03:12:34)

### New
- implements **PyMySQL** and deprecated **MySQL-python**
- SMS module
- SendGridMail module
- use **google-api-python-client** for discovery apis (**BigQuery**)
- force ssl in some external request
- now using secure always [from all endpoints](https://cloud.google.com/appengine/docs/standard/python/sockets/ssl_support)
- method `to_geo_point` to **GeoPoint property**
- now is possible, generate and download `csv files` and response using Rest
- now get info of store files, from GAE (**uploads module**)

### Fix
- pep warnings
- change secret key (**settings**)
- response from **FCM**
- method `get_key`, `get_by_key` and `get_by_name`
- `delete` now are a method class (**datastore_model**),
- metadata is default public (**google_storage**),
- filename an ext `filename_timestamp.ext` or `timestamp_filename`,
- use `save_log` param for save on **DataStore** bug fixeds
- remove code block on `nt OS`, see issue **#4**
- connection for 2nd gen Cloud SQL DB
- added option for XML send and response
- validate some parameters  using `encode("utf-8")`
- **Consumer** function now return original response instead None, if result request not allowed, now it returns the original answer, instead of "**None**", in the answers of services not allowed.
- `get_by` now using `result_fetch` param for one or many values (**datastore_model**)

### Removed
- **MySQL-python**
- `unicode` function (**Commons**)
- unused logs


## 2.0 release (2018-04-12T15:40:33)

### New
- module to send messages to topic and  subscribe clients to topic using fireBase Rest Client
- added 413 response(**main**)
- FireBase settings
- **cartodb now is own module**
- config now set **CARTODB_URI**
- added `config` to path
- now use config folder, added first router
- new configuration folder, for each app or module
- `customEncoder` class now support time `to_json` method have new params (`sort=False`) and `sort_keys` are False
- added **sendEmail**
- added suport for XML response ('application/xml', 'text/xml')
- new method `response_xml` for **XML**
- consumer class, using `"Content-Type: application/json"` by default
- mail Class from **app.ext.mail**
- new method `get_next_month`
- added missing suport for email, using **flask_mail** use `DEFAULT_MAIL_MSG` and `DEFAULT_MAIL_SENDER`
- added `role_id` to `auth_grants` response
- now filter using `companies_id`, queries now cleaned
- **more clean readme, the doc are now on website**
- use **declared_attr** for class name
- new method **send_to_receiver**
- **set default encoding**
- View Upload more clean and easy!
- now using **StorageFile** class from **app.ext.storage**
- now using `send_from_directory` from downloads (custom server only)
- using **secure_filename** to create **store_file_path**
- using `Uploads` entity for save info file in **DataStore**
- `create_file` method class now using **PUBLIC_URI**
- storage class for **custom server**
- storage class for **GCS**
- uncomment the upload module
- added **UPLOAD_FOLDER** and **MAX_CONTENT_LENGTH**

### Fix
- profiles is now `Users`
- readme, change name to uppercase
- connection to **SQLAlchemy** when not connection exists
- `current_current_config`
- security bugs
- ident, and calendar
- `companies` query and response
- `Clients` query and response
- `today` method now using **type_format** param 
- `get_current_time` method using **try/except**
- method get_from_session
- new module name, fix ident
- query over users (view **userinfo**)
- now using config from **app.config.google.bigquery**
- **errorhandler** on wsgi
- now using **GCS** or custom for storage files
- path for modules
- queries, now using filter by `companies`

### Removed
- GOTU
- **old doc, use website doc instead, more updated!**
- ident, remove unused libs, logging as log
- several bug fixeds from `Scheduler api`


## 0.2.b release (2017-12-27T17:28:16)

### New
- method `add_days`
- method `fix_time` to check hours
- new View for **recovery password**
- new doc for security module :)

### Fix
- fix `compare_times` now using `fix_time`
- `to_date` now using `'%Y-%m-%d'` in new_format
- password to view, change where now is using `status_id`
- `application_id` now in companies
- some params `session`, and `uri` fix `content-type`, **added timeout to 60 seconds default**
- using method lambda for `put` and `delete`, `change 'u' to response`
- var now use `StoreCookie` class for save cookies, using `Set-Cookie` header default status is **200** or **201** remove status **400** and **404**
- now use **urllib2.HTTPError** for status error remove `urllib` module
- cartodb sql api V2 client functions
- now check session before create a new session
- field type to Boolean, fix fields types and length
- **rename get_auth_session to get_from_session**
- some methods, change `now` for `utcnow`
- change `hash_key`, **APP_VERSION**, **SECRET_KEY**
- now trying to convert to **JSON**, if `content_type` it's something else
- now use **early_date** and end_date running after 3 moths
- merge from BackendBase 0.2.a-0430ab8

### Removed
- comments
- query using model
- new route for repograms


## 0.2.a release (2017-11-30T15:07:26)

### New
- **CartoDB** cartodb sql api V2 client functions
- data, roles, permissions, role_permissions
- define custom profile for each app
- update initial data, now create companies, auth_grants, auth_clients
- log on error 500, fix else on __name__
- **upgrade Flask to 0.12.2, Flask-SQLAlchemy to 2.3.2, SQLAlchemy to 1.1.15**
- flask logo :)
- now using `http_status_code` and `status_code`
- **georeversed** module
- `ViewStats`, now using **Auth** to access the requested resource
- 'get_by' method, ow print ImportError
- more extension allowed
- doc for custom server
- **gunicorn V. 19.7.1**
- view `ViewStats` for stats info
- create class **customEncoder** for `json decoder`, create new function **to_json**
- **Haversine function from Grafeno api**
- update config to use **flask mail**
- use `TOKEN_TYPE` from **local_settings**

### Fix
- error on click package see **pallets/click** issues **#594** and **#617**
- using with wsgi
- wsgi main app
- length some fields
- password, generate new `client_id`, `client_secret`, `auth_code` using `gen_salt` function
- DEFAULT CHARACTER, COLLATE, AUTO_INCREMENT, added ROW_FORMAT, reduce length fields for `auth_grants`, `auth_clients` and `auth_tokens`
- database names
- to try use **unicode**, some buf fixeds
- **GenericModel** inheriting from **db.Model**
- using session_validate, unipassword are `username + password`
- import in `check_password`, `generate_salt`
- mysql password
- now use `status_http` and `status_code` for differents cases, added **response_custom**
- added info for `settings`
- added changelog uri

### Removed
- MISSING_ARRAY_FIELDS, see `AuthStatus`
- `view_` prefix from `select_from_view`, remove comments
- `generate_password` return password without salt, `check_password` not generate salt
- unused imports, `check_password` and `generate_salt` now in **from app.ext.security** added `client_secret`
- old functions fro crypt keys, now use crypto only

### Deprecated
- `dbsession`
- route for repograms


## 0.1.14 release (2017-06-16T17:22:32Z)

### New
- **Google Big Query** api client functions


## 0.1.12 release (2017-06-15T17:57:19Z)

### New
- **Flask-Cors V. 3.0.2** for **gae-requeriments.txt**
- new module and model for loading files (/uploads)
- new methods `get_file_size` and `allowed_files` (commons)

### Fix
- fix cors issues
- `to_json` now use **unicode** (generic_model)
- check a valid extension and rename file when is stored (uploads)


## 0.1.11  (2017-06-15T01:23:02Z)

### New
- now global config is located in `settings` file
- new file for `database_config`

### Fix
- more clean, see `local_settings`
- fix clear session, now using `terminate_session`
- now using `app.local_settings` and `app.settings`

### Removed
- `constants` and `config` files


## 0.1.10 release (2017-06-14T22:04:23Z)

### New
- new module **Servinf** for georref on **Sitidata**
- new `status_geo`, `geocoder`, `geoassisted`, `geoassisted` functions
- added **cloudstorage**, Client Library for **Google Cloud Storage**
- added **cors** support using **Flask-Cors V. 3.0.2**
- new class **DateUtils**, using init as module

### Fix
- fix token on Sitidata settings for georref
- added and validate `custom_headers` (external_uri)
- rename folders for issue using google libraries
- imports from `app.ext.utils`


## 0.1.9.2 Maintenance Version (2017-06-05T16:04:06Z)

### New
- new file for config databases
- new `raw_query` functions (generic_model)
- config `nosql` (A.K.A. **Google Datastore**)
- new functions `json`, `get_key`, `get_by_key`, `get_by_name` (datastore_model)
- now using **ndb** from **google.appengine.ext**
- `nosql` example for use with **Google Datastore**
- added `nosql` example doc
- new view `ViewAuthLogout`, now create **auth_session** with token and validate time of session
- functions for generate cryp keys, `generate_password`, `check_password` (make_hash)
- create constant for users roles
- new functions `sanity_check`, `remove_accents` (commons)
- endpoint for logs
- `select_from_view` as getting result_fetch for return result, as **one** and **all**
- new functions `get_current_time`, `get_expire_time` (auth)
- added `@dound/gae-sessions` **V. 1.0.7** and using **SessionMiddleware** for **GAE**
- added user logout view `ViewUserLogout`
- mail module using **GAE**
- new functions `get_current_session`, `terminate_session` (serversessions)
- added initial data for `status`, `applications`, `persons` and `role_permissions`
- module for consumer external uri (A.K.A. **consumer**)

### Fix
- check `SQLALCHEMY_DATABASE_URI` for engine session
- using `DATABASE_CONNECTION`, instead raw connection
- change key secret for **AES**
- default patch now return `UNAUTHORIZED`
- added **/v1**, fix path for `Auth`
- `validate_token_header`, now check token type
- new function `session_validate` as function decorator
- `raw_query`, now uses `raw_json` to return result
- `SECONDS_EXPIRE` is in seconds
- now validate each session type
- rename `generate_uuid`
- validate `key_secret` from App
- validate creation `AuthClient`
- MAIL_ADMIN use `os.environ.get`
- `get_current_time` using `timedelta` (**hours=5**)
- update database schema and initial db script

### Removed
- rename folder for bug in libraries with **ndb**
- obsolete `t_userinfo`, `get_by_username`, `get_userinfo`
- remove deprecated `require_auth` function
- unused imports

### Deprecated
- `constants` and `config` files, are removed from future versions


## 0.1.9.1  (2017-05-16T19:30:42Z)

### Fix
- change version number

### Removed
- accidentally added files


## 0.1.9  (2017-05-16T19:23:53Z)

### New
- **hello world** module example
- readme for `example` folder
- created database schema
- creating initial data for `database`
- database configuration

### Fix
- now using **DATABASE_CONNECTION**
- force to used `CLOUD` if **GAE**

### Removed
- unused imports
- log


## 0.1.8  (2017-05-15T18:38:31Z)

### New
- users views
- log views
- added `psycopg2` **V. 2.7.1**
- support connect to **postgreSQL**
- new Model base to use with **Google Datastore**
- using `pycrypto` **V. 2.6**
- implement `get_by` (generic_model)
- new module `Cypher`, using **AES** secure algorithm
- new module for store files in **Google Storage**
- added `build_systems` for python (Sublime Text)
- `create_name_from_email`, `is_iterable` functions
- app engine docs
- implements **app.ext.security.Auth**, on class and methods
- new `HttpStatus` class for funny messages :)
- requeriments for **Google App Engine**

### Fix
- more complete readme
- now using `CORS_HEADERS`, invoke api.representation method
- send custom headers
- override CRUD's methods for **generic_model.py**
- fixed `get_by_name`
- new method `to_json` for serialize class objects
- fix ident using `pep8`
- rename to `SQLALCHEMY_DATABASE_URI`
- fix paths for readme's
- now using **HttpStatus**
- Dictionary headers into response pass method (**app.ext.rest.cors**)

### Experimental
- new `feature/experimental` branch
- fix models using **sqlacodegen**
- view for crud `AuthClients`
- using for debugging
- new method `dict_to_obj`, `select_from_view`, `get_userinfo`
- using session for query, now validated both client credentials

### Removed
- remove creation array in 'data'
- remove `abort` method


## 0.1.7  (2017-05-05T16:56:14Z)

### New
- added **SQLAlchemy V. 1.1.9**
- added **MySQL-python V. 1.2.5**
- added **sqlacodegen V. 1.1.6**
- added models for `Auth, Permission, Persons, Role, RolePermission, Status, Users`
- enabled endpoint for RegUsers
- GenericModel mapping for SQlAlchemy DB
- new class method `get_by_name`
- create engine for connections
- new module Applications
- new module for `google` use
- new module Permission
- update models for AuthClient, AuthGrant, AuthToken
- added **SQLALCHEMY_DATABASE_URI**
- added **404**, **500** error handler

### Experimental
- experimental use of mysql Views

### Fix
- change path and magic port :)
- move Commons to **ext.utils**
- reorganized home endpoints, models and views

### Removed
- unused vars, obsolete queries
- remove and move modules, functions and more, cleaning the house!


## 0.1.6  (2017-05-03T11:37:27Z)

### New
- init version for app engine
- new setting **INSTALLED_MODULES**
- check if running on **GAE**
- check vars on email, **EXCLUDE_EXT** and other to exclude
- added **home** module
- added **Commons** class
- awesome rest, validate data
- new module **ext**
- Security, verify auth token, json body ext...
- move to ext, now using **CORS_HEADERS**

### Fix
- run main app using `app.ext.register`
- using `ResourceHandler`, `Commons`, `Rest`
- fix path
- more expresive class for register
- fix name for main.app on **GAE**
- Merge branch `feature/crazybranch` into `develop` branch

### Removed
- olds and unused scripts
- change APP_PATH, remove unused functions
- unused logs
- unused modules


## 0.1.5  (2017-04-17T11:36:59Z)

### New
-  added vars from config for run server, **USE_STDERR**,

### Fix
-  modify **APP_PATH**
-  fix path for env, set message
-  reorder apps, fix path, added vars to `application.run`


## 0.1.4  (2017-04-16T20:55:19Z)

### New
-  added ingnore files, os specific files, more info on ***gitignore.io***
-  awesome editor config

### Fix
-  update name, url


## 0.1.3  (2017-04-16T20:33:46Z)

### New
- added **AUTH_ERROR_MSG**, **CSRF_SESSION_KEY**, **CSRF_ENABLED**, fix APP_PATH
- import AUTH_ERROR_MSG
- using `Rest.response` for 401 instead **abort(401)**
- new decorator 'require_token_header' for single request header

### Fix
- now return a object array from register metod

### Removed
- remove unused comments


## 0.1.2  (2016-09-03T20:41:23Z)

### New
- dynamic routing loaded,
- define staticmethod routes, for url routes
- add **HEADER_API_KEY**, **ROUTES_PATH**, **EXCLUDE_EXT** constants
- new register function
- added **USE_VERSION_API** for `url_prefix`
- added **Flask-Mail V. 0.9.1**
- added config for email sender

### Fix
- `dynamic_importer` is renamed a __module_loader, function to load return tuple with routes and class
- fixed bugs and style guide
- rename class, now as **ResourceApi**
- fix register function, for add `url_prefix` to the api

### Removed
- api and `add_resource`, in favor of `register` with url_prefix


## 0.1.1  (2016-09-01T00:05:33Z)

### New
- `dynamic_importer` for loading dynamic routes
- decorate require_auth function for check header, using in a example
- new and awesome decorated methods :)
- new class Rest and Utils
- main handler
- added **LGPL V. 2.1**

### Fix
- Users, now using pulse

### Removed
- now using __init from utils folder


## 0.1.0 (2016-08-27T17:49:23Z)

### New
- initial packages
- some utils, response
- wsgi config for apache
- `get_timestamp`, `today`, `to_date` (utils)
- decorated function for validate json request
- `validate_email` function

### Fix
- `not_found` function

## Initial app (2016-08-24T22:21:33Z)

### New
- added **Flask 0.11.1**
- added **Flask-RESTful 0.3.5**

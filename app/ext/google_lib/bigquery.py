# -*- coding: utf-8 -*-

"""Python module for Google Cloud BigQuery."""

from google.cloud import bigquery
from app.ext.utils import DateUtils
from app.config.storage import DEFAULT_BUCKET
from app.config.google.bigquery import BQ_PROJECT_ID

try:
    client = bigquery.Client()
except Exception as e:
    print("BigQuery Client Exception:", e)
    raise e


class Jobs:
    @staticmethod
    def create_job(query, prefix=None, location=None, destination_table=None, labels=None, maximum_bytes_billed=None):
        new_prefix = None
        new_location = None

        if query is None:
            print("Jobs create_jobs Exception: missing query")
            return None

        if prefix is None:
            print("Jobs create_jobs: missing prefix")
            print("The client libraries automatically generate a job ID...")
            new_prefix = "data_rutas_export_job_{0}".format(DateUtils.get_timestamp())
            print ("Jobs create_jobs new prefix:", new_prefix)
        else:
            new_prefix = prefix

        if location is None:
            print("Jobs create_jobs Exception: missing location")
            new_location = "US"
        else:
            new_location = location

        if labels is None:
            print("Jobs create_jobs Exception: missing labels")
            labels = {"data_rutas_export_job": new_prefix}

        if maximum_bytes_billed is None:
            print("Jobs create_jobs Exception: missing maximum_bytes_billed")
            # maximum_bytes_billed = 1000000
            maximum_bytes_billed = 99554432

        job_config = bigquery.QueryJobConfig(
            labels=labels, maximum_bytes_billed=maximum_bytes_billed
        )

        if destination_table is not None:
            print("adding destination table:", destination_table)
            job_config = bigquery.QueryJobConfig(
                labels=labels,
                maximum_bytes_billed=maximum_bytes_billed,
                destination=destination_table
            )

            print("Jobs create_jobs: Query results loaded to the table {0}".format(destination_table))

        query_job = client.query(
            query,
            location=new_location,
            job_config=job_config,
            job_id_prefix=new_prefix
        )  # Make an API request.

        print("=================================")
        print("job prefix:", new_prefix)
        print("job location:", new_location)
        print("job labels:", labels)
        print("job maximum_bytes_billed:", maximum_bytes_billed)
        print("Started job:", query_job.job_id)
        print("=================================")

        result = query_job.result()  # Wait for the job to complete.
        print("query_job.result:", result)

        return {
            "job_id": query_job.job_id,
            "prefix": new_prefix,
            "location": new_location,
            "labels": labels,
            "maximum_bytes_billed": maximum_bytes_billed,
            "job_result": result
        }

    @staticmethod
    def get_status_job(job_id, location=None):
        new_location = "US"

        if job_id is None:
            print("Jobs get_status_job Exception: missing job_id")
            return None

        if location is None:
            print("Jobs get_status_job Exception: missing location")
            new_location = "US"
        else:
            new_location = location

        job = client.get_job(job_id, location=new_location)  # API request

        # Print selected job properties
        print("Details for job {0} running in {1}:".format(job_id, location))
        print("Type:", job.job_type)
        print("State:", job.state)
        print("tCreated:", job.created)

    @staticmethod
    def cancel_job(job_id, location=None):
        new_location = "US"

        if job_id is None:
            print("Jobs cancel_job Exception: missing job_id")
            return None

        if location is None:
            print("Jobs cancel_job Exception: missing location")
            new_location = "US"
        else:
            new_location = location

        job = client.cancel_job(job_id, location=new_location)

        # Print selected job properties
        print("Details for job {0} running in {1}:".format(job_id, new_location))
        print("Type:", job.job_type)
        print("State:", job.state)
        print("tCreated:", job.created)


class BigQuery:
    @staticmethod
    def init(dataset, table):
        table_ref = client.dataset(dataset).table(table)
        client.get_table(table_ref)

    @staticmethod
    def send_query(query, location="US", result_fields=None):
        query_job = client.query(query, location=location)
        return BigQuery.big_response(query_job, result_fields)

    @staticmethod
    def response(query_job, raw_mode=False):
        if raw_mode == False:
            result_list = []
            for row in query_job:
                # assert row[0] == row.name == row["name"]
                # print("row:", row)
                result_list.append(list(row))
            return result_list
        else:
            return query_job

    @staticmethod
    def big_response(query_job=None, array_keys=None):
        if query_job is None:
            return None

        if array_keys is None:
            return None

        if len(array_keys) > 0:
            key = array_keys
            array_list = []
            obj = {}
            cont = 0

            for item in query_job:
                for value in item:
                    obj[key[cont]] = value
                    cont += 1
                array_list.append(obj)
                obj = {}
                cont = 0

            return array_list
        else:
            return None

    @staticmethod
    def create_table(schema=None, dataset=None, table=None):
        """estructura de schema: [('colum_name','type','mode'),('colum_name','type','mode')],
        type y mode no son requeridos, los valores predeterminados son STRING y NULLABLE respetivamente"""
        #https://cloud.google.com/bigquery/docs/tables
        if schema is None or dataset is None or table is None:
            return None

        schema_bq = []
        for sch in schema:
            if len(sch) == 1:
                schema_bq.append(bigquery.SchemaField(sch[0], "STRING", mode="NULLABLE"))
            if len(sch) == 2:
                schema_bq.append(bigquery.SchemaField(sch[0], sch[1], mode="NULLABLE"))
            if len(sch) == 3:
                schema_bq.append(bigquery.SchemaField(sch[0], sch[1], mode=sch[2]))

        table_id = '{0}.{1}.{2}'.format(BQ_PROJECT_ID, dataset, table)
        new_table = bigquery.Table(table_id, schema=schema_bq)
        new_table = client.create_table(new_table)

        try:
            print('Created table {0}.{1}.{2}'.format(new_table.project, new_table.dataset_id, new_table.table_id))
        except Exception as e:
            print(new_table)
            print('create_table Errors: {0}'.format(e))
            return e
        return None

    @staticmethod
    def insert_json(dataset, table, rows_to_insert):
        if rows_to_insert is None:
            return None
        # dataset_id = dataset_name  # replace with your dataset ID
        # table_id = table_name  # replace with your table ID
        table_ref = client.dataset(dataset).table(table)
        data_table = client.get_table(table_ref)

        print("rows_to_insert:", rows_to_insert)
        errors = client.insert_rows_json(data_table, rows_to_insert)

        if not errors:
            print('rows_to_insert Success:')
            print('Loaded {0} row(s) into {1}:{2}'.format(len(rows_to_insert), dataset, table))
        else:
            print('rows_to_insert Errors:')
            for error in errors:
                print(error)
        return None

    @staticmethod
    def export_data(dataset, table_id, location=None, default_folder=None):
        new_location = "US"

        if dataset is None:
            return None

        if table_id is None:
            return None

        if location is None:
            print("BigQuery export_data Exception: missing location")
            new_location = "US"
        else:
            new_location = location

        try:
            dataset_ref = bigquery.DatasetReference(BQ_PROJECT_ID, dataset)
            table_ref = dataset_ref.table(table_id)
            print("BigQuery export_data BQ_PROJECT_ID:", BQ_PROJECT_ID)
            print("BigQuery export_data dataset:", dataset)
            print("BigQuery export_data table_id:", table_id)
        except Exception as e:
            print("BigQuery export_data DatasetReference Exception:", e)
            return e

        try:
            if default_folder is None:
                default_folder = "exports"

            # with comodin (*)
            # export_file_name = "data_rutas_export_job_{0}-*.json".format(DateUtils.get_timestamp())
            export_file_name = "data_rutas_export_job_{0}.zip".format(DateUtils.get_timestamp())

            destination_uri = "gs://{0}/{1}/{2}".format(DEFAULT_BUCKET, default_folder, export_file_name)

            print("BigQuery export_data default_folder:", default_folder)
            print("BigQuery export_data export_file_name:", export_file_name)
            print("BigQuery export_data destination_uri:", destination_uri)
            print("BigQuery export_data location:", new_location)
        except Exception as e:
            print("BigQuery export_data default_folder Exception:", e)
            return e

        try:
            job_config = bigquery.ExtractJobConfig(
                compression=bigquery.job.Compression.GZIP,
                sourceFormat=bigquery.job.SourceFormat.CSV,
                destination_format=bigquery.job.DestinationFormat.CSV
            )

            extract_job = client.extract_table(
                table_ref,
                destination_uri,
                location=new_location,
                job_config=job_config
            )  # API request

        except Exception as e:
            print("BigQuery export_data extract_table Exception:", e)
            return e

        try:
            result = extract_job.result()  # Waits for job to complete.
            print("BigQuery export_data extract_job.result:", result)
            print("BigQuery export_data Exported {0}:{1}.{2} to {3}".format(BQ_PROJECT_ID, dataset, table_id, destination_uri))
            return {
                "result": result,
                "dataset": dataset,
                "table_id": table_id,
                "destination_uri": destination_uri
            }
        except Exception as e:
            print("BigQuery export_data extract_job result Exception:", e)
            return e

        return None

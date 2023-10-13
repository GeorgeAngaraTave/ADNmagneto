# -*- coding: utf-8 -*-

"""Python module for Google Cloud Task Queues"""

from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import datetime
import json

AVAILABLE_METHODS = ['GET', 'POST']
PROJECT_NAME = 'magneto-dot-invertible-eye-316323'
TASK_LOCATION = 'us-central1'


def create_task(queue_name, endpoint_uri, method, payload=None, gae_service_name='default', gae_version='backend'):
    """Allows you to create tasks and assign them to a queue, using Google Cloud Task Queues"""

    if queue_name is None:
        print('failed to create task: task queue name is required')
        return None

    if endpoint_uri is None:
        print('failed to create task: endpoint_uri is required')
        return None

    if method is None:
        print('failed to create task: method is required')
        return None

    if method not in AVAILABLE_METHODS:
        print('failed to create task: method is not allowed')
        return None

    in_seconds = None

    try:
        client = tasks_v2.CloudTasksClient()
        parent = client.queue_path(PROJECT_NAME, TASK_LOCATION, queue_name)

        task = {
            'app_engine_http_request': {
                'relative_uri': endpoint_uri,
                'http_method': method,
                'app_engine_routing': {
                    'service': gae_service_name,
                    'version': gae_version
                }
            }
        }

        if method is 'POST':
            if payload is not None:
                # converted payload to bytes

                try:
                    # receive from service
                    converted_payload = json.dumps(payload).encode('utf-8')
                    task['app_engine_http_request']['body'] = converted_payload
                except Exception as e:
                    # receive from pub/sub
                    task['app_engine_http_request']['body'] = payload

        if in_seconds is not None:
            d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)
            task['schedule_time'] = timestamp

        response = client.create_task(parent, task)

        print('Finish and Created task: {0}'.format(response.name))

        return response.name
    except Exception as e:
        reason = "create_task Exception, An error occurred while creating the Task: {0}".format(e)
        print(reason)
        return None

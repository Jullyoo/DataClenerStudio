from celery import Celery

celery = Celery(

    'tasks',

    broker='redis://localhost:6379/0',

    backend='redis://localhost:6379/0'
)


@celery.task
def process_large_file(file_path):

    print(f'Processing: {file_path}')

    return {

        'status': 'completed',

        'file': file_path
    }
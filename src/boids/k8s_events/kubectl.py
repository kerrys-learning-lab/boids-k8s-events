import json
import subprocess

def get_resource(resource_type):
    results = subprocess.check_output(['kubectl',
                                       'get',
                                       '-n', 'boids',
                                       '-o', 'json',
                                       resource_type])

    results = json.loads(results)
    return results['items']

def apply(filepath):
    subprocess.check_output(['kubectl',
                             'apply',
                             '-f', filepath])

def delete(filepath):
    subprocess.check_output(['kubectl',
                             'delete',
                             '-f', filepath])

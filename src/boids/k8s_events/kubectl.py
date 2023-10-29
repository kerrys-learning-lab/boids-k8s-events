''' Python "interface" to kubectl tool '''
import json
import subprocess

def get_resources_by_type(resource_type):
    ''' Returns a python dict describing all entities of the given resource type '''
    results = subprocess.check_output(['kubectl',
                                       'get',
                                       '-n', 'boids',
                                       '-o', 'json',
                                       resource_type])

    results = json.loads(results)
    return results['items']

def apply(filepath):
    ''' Performs a "kubectl apply -f" using the given filepath '''
    subprocess.check_output(['kubectl',
                             'apply',
                             '-f', filepath])

def delete(filepath):
    ''' Performs a "kubectl delete -f" using the given filepath '''
    subprocess.check_output(['kubectl',
                             'delete',
                             '-f', filepath])

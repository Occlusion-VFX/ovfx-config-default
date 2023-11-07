from datetime import datetime
from pprint import pprint
import os
def getProjects():
    filters = []
    fields = ['name']
    order = []
    results = shotgun.find('Project', filters, fields, order)
    return results
    
def getShots(project,code):
    filters = [
        ['project', 'is', project],
        ['code', 'is', code],
        ]
    fields = ['code', 'description', 'project']
    order = []
    results = shotgun.find('Shot', filters, fields, order)
    return results
    
    
if __name__ == '__main__':
    projects = getProjects()
    for project in projects:
        if project['name'] == 'test_remote':
            p = project
    
    code = 'test_001'
    shots = getShots(p,code)
    if len(shots) == 1:
        print('description: ' + shot['description'])
    else:
        print('found too many shots')
        
        


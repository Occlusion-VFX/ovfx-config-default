from datetime import datetime
from pprint import pprint
start = datetime.now()
verbose = True
print('Starting: {}'.format(start))
print('')

'''
already loaded into proect context
just retrieving Project ID
'''

projectFilters = [['archived', 'is', False],
                  ['name', 'is', str(context).split(' ')[-1]],
                    ]
projectFields = ['name']
project = shotgun.find_one('Project', projectFilters, projectFields)

shotFilters = [['project', 'is', project],
               # ['sg_status_list', 'is', 'ip'], # limit search to just In Progress Shots
                ]
shotFields = ['code', 'sg_status_list']
shots = shotgun.find('Shot',shotFilters,shotFields, order=[{'field_name':'code','direction':'asc'}])
for shot in shots:
    if verbose:
        print(shot['code'], shot['sg_status_list'])
    if shot['sg_status_list'] == 'ip':
        taskFilters = [['project', 'is', project],
                      ['step', 'in', [{'type':'Step','id':8},{'type':'Step','id':9}]],
                      ['entity', 'is', shot],
                        ]
        taskFields = ['sg_status_list', 'step'] # task_assignees, entity
        tasks = shotgun.find('Task', taskFilters, taskFields)
        for task in tasks:
            if verbose:
                for t in task:
                    print('  {}: {}'.format(t, task[t]))
            if task['sg_status_list'] == 'rev':
                verFilters = [['project', 'is', project],
                              ['entity', 'is', shot],
                               ]
                verFields = ['code', 'sg_path_to_frames', 'sg_status_list', 'updated_at'] # user, entity, sg_task (extra fields)
                verAddFilter = [{"preset_name": "LATEST",
                                 "latest_by":   "ENTITIES_CREATED_AT"
                                    }]

                versions = shotgun.find('Version', verFilters, verFields, order=[{'field_name':'updated_at','direction':'desc'}]) # additional_filter_presets=verAddFilter)
                for version in versions:
                    if verbose:
                        print('')
                        for v in version:
                            print('    {}: {}'.format(v, version[v]))

elapsed = datetime.now() - start
print('')
print('Time Elapsed: {}'.format(elapsed))
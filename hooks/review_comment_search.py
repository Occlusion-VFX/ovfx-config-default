from datetime import datetime
from pprint import pprint
import os
start = datetime.now()
verbose = True
print('Starting: {}'.format(start))
print('')

'''
already loaded into proect context
just retrieving Project ID
'''
comment = None
#path = 'Z;/Projects/Project_Data/test_002/sequences/seq_001/transcode_test/comp/publish/nuke/transcode_test_comp.v008.nk'
path = r'Z:\Projects\Project_Data\test_002\sequences\seq_001\transcode_test\comp\publish\elements\transcode_test_comp_v008\4096x2304\jpg\transcode_test_comp_v008.%06d.jpg'
print comment

filters = [
    ['entity.Shot.code', 'is', 'transcode_test'],
    #['project', 'is', project],
    ['task.Task.content', 'is', 'Compositing'],
    ]
fields = ['description', 'code']
order = [{'field_name': 'version_number', 'direction':'desc'}]
found = shotgun.find('PublishedFile', filters, fields, order)
print len(found)

for f in found: 
    fn = os.path.basename(path)    
    base = fn.split('.')[0]
    code = base.split('_')[:-1]
    version = base.split('_')[-1]
    print code, version
    nk = '{code}.{version}.nk'.format(
        code='_'.join(code),
        version=version,
        )

    if f['code'] == nk:
        if f['description'] is not None:
            comment = f['description'] 
        else:
            comment = ''

print comment

print('Finished! [{}]'.format(datetime.now()-start))
#!python2

import os
import sys
import argparse

file = os.path.realpath(sys.argv[0])
config = '\\'.join(str(file).split('\\')[0:4])
sgtk_loc = os.path.join(config, 'install', 'core', 'python')
print(sgtk_loc)
sys.path.insert(0, sgtk_loc)
import sgtk
print('=> Shotgun Toolkit Bootstrap Successful!')


def upload(file):
    global ShotgunAuthenticator, shotgun_api3
    from tank_vendor import shotgun_api3
    from tank_vendor.shotgun_authentication import ShotgunAuthenticator # Import the ShotgunAuthenticator from the tank_vendor.shotgun_authentication module

    ''' Authentication '''
    global sg
    sg = shotgun_api3.Shotgun('https://occlusionvfx.shotgunstudio.com', 
                              'BB_pub',
                              'xzdqlwlzwjhf)Mbcry2fcundq')

    script_auth() 

    context = findTask()
    versionID = createVersion( context, file )

    # Upload
    uploadThumb(versionID['id'],
        "Z:/Projects/Project_Data/test_002/sequences/seq_001/transcode_test/comp/review/transcodes/transcode_test_comp_v001/transcode_test_comp_v001_thumbnail.jpg"
            )
    uploadFilmstrip(versionID['id'],
        "Z:/Projects/Project_Data/test_002/sequences/seq_001/transcode_test/comp/review/transcodes/transcode_test_comp_v001/transcode_test_comp_v001_filmstrip.jpg"
            )
    uploadMP4(versionID['id'],
        "Z:/Projects/Project_Data/test_002/sequences/seq_001/transcode_test/comp/review/transcodes/transcode_test_comp_v001/transcode_test_comp_v001.mp4"
            )
    uploadWebM(versionID['id'],
        "Z:/Projects/Project_Data/test_002/sequences/seq_001/transcode_test/comp/review/transcodes/transcode_test_comp_v001/transcode_test_comp_v001.webm"
            )
    print('==> Upload complete!')


def script_auth():
    # Instantiate the CoreDefaultsManager. This allows the ShotgunAuthenticator to
    # retrieve the site, proxy and optional script_user credentials from shotgun.yml
    cdm = sgtk.util.CoreDefaultsManager()

    # Instantiate the authenticator object, passing in the defaults manager.
    authenticator = ShotgunAuthenticator(cdm)

    # Create a user programmatically using the script's key.
    user = authenticator.create_script_user(
     api_script="BB_pub",
     api_key="xzdqlwlzwjhf)Mbcry2fcundq"
    )

    # print ("User is '%s'" % user)

    # Tells Toolkit which user to use for connecting to Shotgun.
    sgtk.set_authenticated_user(user)


def findTask():
     # Bookstrap Toolkit
    tk = sgtk.sgtk_from_path(file)
    # Required to ensure the local path cache is up to date when creating a context from a path on disk
    tk.synchronize_filesystem_structure()
    
    ctx = tk.context_from_path(file)
    project = ctx.project
    step    = ctx.step
    entity  = ctx.entity
    shot_code = file.split('/')[6]
    filename = os.path.splitext(os.path.basename(file))[0].split('.')[0]

    # filters = [ ['project', 'is', project],
        # ['code', 'is', shot_code] ]
    # shot = sg.find('Shot', filters)
    
    filters = [ ['project', 'is', project],
        ['entity','is', entity],
        ['content', 'is', 'Compositing']]
    task = sg.find_one('Task', filters)
    
    context = {
        'project': project,
        'step': step,
        'entity': entity,
        'shot_code': shot_code,
        'filename': filename,
        'task': task,
             }

    return context


def createVersion(context, path):
    print('=> Creating Version')
    data = { 'project': context['project'],
         'code': context['filename'], # '100_010_anim_v1',
         'description': 'adjusted mp4 transcode crf 15 film', # 'first pass at opening shot with bunnies',
         'sg_path_to_frames': path, #'/v1/gun/s100/010/frames/anim/100_010_animv1_jack.#.jpg',
         'sg_status_list': 'rev',
         'entity': context['entity'], # {'type': 'Shot', 'id': shot['id']},
         'sg_task': context['task'], # {'type': 'Task', 'id': task['id']},
         # 'user': user, # {'type': 'HumanUser', 'id': 165} }
            }
    version = sg.create('Version', data)
    
    return version


def uploadThumb(versionID, file):
    print('=> Uploading Thumbnail')
    sg.upload_thumbnail('Version', versionID, file)
    return


def uploadFilmstrip(versionID, file):
    print('=> Uploading Filmstrip')
    sg.upload_filmstrip_thumbnail('Version', versionID, file)
    return


def uploadMP4(versionID, file):
    print('=> Uploading MP4')
    sg.upload(
        'Version',
        versionID,
        file,
        field_name='sg_uploaded_movie_mp4',
        )


def uploadWebM(versionID, file):
    print('=> Uploading WebM')
    sg.upload(
        'Version',
        versionID,
        file,
        field_name='sg_uploaded_movie_webm',
        )


def sortTranscodes(input):

    name = os.path.splitext(os.path.basename(input))[0]

    transcodes = os.path.join(os.path.dirname(input), 'transcodes', name)
    print(transcodes)
    transcode_files = os.listdir(transcodes)
    transcode_dict = []
    for file in transcode_files:
        path = os.path.join(transcodes,file)
        ext = os.path.splitext(path)[1].replace('.','')
        transcode_dict.append(
            {
            'path': path,
            'ext': ext,
                }
                    )

    for x in transcode_dict:
        if x['ext'] == 'jpg':
            f = os.path.splitext(os.path.basename(x['path']))[0]
            type = f.split('_')[-1]
            if type == 'filmstrip':
                print('==> Uploading Filmstrip!')
            else:
                print('==> Uploading Thumbnail!')
        elif x['ext'] == 'mp4':
            print('==> Uploading MP4!')
        else:
            print('==> Uploading WebM!')


if __name__ == '__main__':
    # file = "Z:/Projects/Project_Data/test_002/sequences/seq_001/transcode_test/comp/work/images/transcode_test_comp_v001/4096x2304/exr/transcode_test_comp_v001.%06d.exr"
    file = "Z:/Projects/Project_Data/test_002/sequences/seq_001/transcode_test/comp/review/transcode_test_comp_v001.mov"
    sortTranscodes(file)
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--files', nargs='+', help='file to submit')
    # opt = parser.parse_args()

    # upload(file)
import os, sys
import time

'''
writeProfile Options:
Mono Exr, Zip
Stereo Exr, Zip
Mono Exr, DWAA
Stereo Exr, DWAA
Mono jpg
Stereo Jpg
ProRes 422 HQ
ProRes 4444
'''

''' Sets Default Write Node Preset in Nuke '''
writeProfile = 'Mono Exr, Zip'

def override_nuke_shortcuts():
    """
    Override various shortcut keys in Nuke to run our own commands
    instead

    :param engine: The current engine
    """

    import nuke
    import scripts

    m = toolbar = nuke.toolbar("Nodes")
    sg_menu = nuke.menu("Nuke").findItem("Shotgun")

    ##  Currently restarting engine in tk-nuke/init to make sure hot keys stick after loading script from File Manager

    if not nuke.env.get("gui"):
        # not running in interactive mode so don't have menus or shortcuts!
        return

    # remove default hotkey for write/read node - relocated to menu.py
    # read_node_item = nuke.menu('Nodes').findItem("Image/Read")
    # read_node_item.setShortcut("Shift+R")

    #Set hotkey to shotgun File Open and Publish
    sg_publish = sg_menu.findItem('Publish...')
    sg_open = sg_menu.findItem('File Open...')
    if sg_menu:
        if sg_menu:
            sg_open.setShortcut("F1")
        if sg_publish:
            sg_publish.setShortcut("F2")


    # add new hot key for Shotgun Mono Exr write Node
    sg_write_node_item = nuke.menu('Nodes').findItem("Shotgun/{} [Shotgun]".format( writeProfile ) )
    if sg_write_node_item:
        write_node_item = nuke.menu('Nodes').findItem("Image/Write")
        write_node_item.setShortcut("Shift+w")
        sg_write_node_item.setShortcut("w")


    #add new hot key for WritetoRead Node - relocated to menu.py
    # toolbar.addMenu('Image').addCommand( 'Read from Write', scripts.readFromWrite, 'r')

    # add new hot key for Shotgun > Shotgun Save As...
    if sg_menu:
        sg_save_as_item = sg_menu.findItem("File Save...")
        if sg_save_as_item:
            # remove default hotkey from File > Save As...
            # NOTE: Nuke 9 renamed this menu to "Save Comp As..." :/
            file_menu = nuke.menu('Nuke').findItem("File")
            save_as_item = file_menu.findItem("Save Comp As...")
            save_as_item.setShortcut("")

            sg_save_as_item.setShortcut("Ctrl+Shift+S")


        # add new hotkey for Shotgun/Load
        sg_load = sg_menu.findItem('Load...')
        if sg_load:
            sg_load.setShortcut('F3')

        '''
        Panel seems like buggy mess
        sometimes it crashes, sometimes it doesn't
        '''
        # # add hotkey for Shotgun/Shotgun Panel...
        # sg_panel = sg_menu.findItem('Shotgun Panel...')
        # if sg_panel:
            # sg_panel.setShortcut('f4')
    ''' end of override_nuke_shortcuts() '''


def syncRange():
    ''' Invoke Sync Frame Range with Shotgun '''
    import nuke

    sg_menu = nuke.menu("Nuke").findItem("Shotgun")
    if sg_menu:
        sg_setFrameRange = sg_menu.findItem('Sync Shot Info with Shotgun')
        if sg_setFrameRange:
            sg_setFrameRange.invoke()


def invokePanel():
    '''
    Invoke Shotgun Panel to load

    without sleep, causes nuke to crash
    nevermind, still crashes apparently
    panel may just be a buggy mess...
    '''
    import nuke
    # time.sleep(1)

    sg_menu = nuke.menu("Nuke").findItem("Shotgun")
    if sg_menu:
        ShotgunPanel = sg_menu.findItem('Shotgun Panel...')
        if ShotgunPanel:
            try:
                ShotgunPanel.invoke()
            except:
                pass
    ''' end of invokePanel() '''


def setFrameRate():
    import nuke
    current = nuke.root()['fps'].value()

    nuke.root()['fps'].setValue(fps)


def setRelPaths(deep=4, verbose=False):
    '''
    Parses a Root Directory from current script
    path and sets all valid Read/Write Nodes to
    relative paths

    args:
        verbose: Sets Verbosity of Script
                 use for debugging
        deep   : number of folders to use for Root
                 starting at and including the Drive
    '''
    import nuke

    scriptDir = nuke.script_directory()

    projDir = nuke.Root()['project_directory'].value()
    projDirNew = '/'.join(scriptDir.split('/')[:deep])
    if verbose:
        print(projDirCurr)
        print(projDirNew)

    if projDir != projDirNew:
        nuke.Root()['project_directory'].setValue(projDirNew)

    for node in nuke.allNodes('Read')+nuke.allNodes('Write'):
        currFile = node['file'].value()
        fileDir  = '/'.join(currFile.split('/')[:5])
        if verbose:
            print(node['name'].value())
            print('  '+currFile)

        if currFile[0] == '.':
            if os.path.isdir(os.path.dirname(projDirNew + currFile[1:])):
                continue
            else:
                absFile = projDir + currFile[1:]
                fileRoot = '/'.join(absFile.split('/')[:deep])
                if verbose:
                    print('  '+absFile)
                    print('  '+fileRoot)
                if fileRoot == projDirNew:
                    newFile = absFile.replace(projDirNew, '.')
                    node['file'].setValue(newFile)
                    if verbose:
                        print('  '+newFile)

        else:
            fileRoot = '/'.join(currFile.split('/')[:deep])
            if fileRoot == projDirNew:
                newFile = currFile.replace(projDirNew, '.')
                node['file'].setValue(newFile)
                if verbose:
                    print('  '+newFile)


def setAbsPaths(verbose=False):
    '''
    Sets paths of all valid Read/Write Nodes
    to absolute paths

    args:
        verbose: Sets Verbosity of Script
                 use for debugging
    '''
    import nuke

    projDir = nuke.Root()['project_directory'].value()
    if projDir == '':
        print('Project Directory not set!\nAlready using Absolute Paths')
        return
    else:
        for node in nuke.allNodes('Read')+nuke.allNodes('Write'):
            file = node['file'].value()
            absFile = projDir+file[1:]
            if os.path.isdir(
                os.path.dirname(absFile)
                    ):
                node['file'].setValue(absFile)


def endOfFile():
    return

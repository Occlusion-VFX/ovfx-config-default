#!python

import cv2
import os
from datetime import datetime

ffmpeg_path = "Z:/Scripts/FFMPEG/FFMPEG_Current/bin/ffmpeg.exe"


def VideoData(input):
    cap = cv2.VideoCapture(input)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(frames/50)
    num_frames = int(frames/interval)
    thumb = int(frames/2)

    data = {
        'frames': frames,
        'fps': fps,
        'interval': interval,
        'num_frames': num_frames,
        'thumb': thumb,
            }

    return data


def createMP4(fps, input, version):
    start = datetime.now()
    vcodec = "libx264 -pix_fmt yuv422p10le \
              -g 30 -b:v 2000k -preset veryslow -bf 0 -movflags +faststart -crf 15 -tune film"
    newfile = os.path.basename(input).replace('.mov', '.mp4')
    output =  os.path.join(version, newfile)
    
    args = " \
        -r {fps} \
        -i {input} \
        -vcodec {vcodec} \
        -acodec acc \
        {output}".format(
            fps=fps,
            input=input,
            vcodec=vcodec,
            output=output,
                )

    os.system('cmd /c "{exe} -y -loglevel warning -stats {args}"'.format(
        exe=ffmpeg_path,
        args=args,
            )
        )
    elapsed = datetime.now() - start
    print('==> MP4 created! [{}]'.format(elapsed))
    return output


def createWebM(fps, input, version):
    start = datetime.now()
    vcodec = "libvpx-vp9 -pix_fmt yuv420p -b:v 0 -crf 15 -threads 2 -speed 2"
    newfile = os.path.basename(input).replace('.mov', '.webm')
    output = os.path.join(version, newfile)
    
    args = " \
        -r {fps} \
        -i {input} \
        -vcodec {vcodec} \
        -acodec acc \
        {output}".format(
            fps=fps,
            input=input,
            vcodec=vcodec,
            output=output,
                )

    os.system('cmd /c "{exe} -y -loglevel warning -stats {args}"'.format(
        exe=ffmpeg_path,
        args=args,
            )
        )
    elapsed = datetime.now() - start
    print('==> WebM created! [{}]'.format(elapsed))
    return output


def createThumbnail(fps, file, thumb, version):
    start = datetime.now()
    output=os.path.join(version, os.path.basename(file).replace('.mov', '_thumbnail.jpg'))

    args = " \
        -r {fps} \
        -i {input} \
        -frames 1 \
        -vf \"scale=640:-1,select=gte(n\,{thumb})\" \
        {output} \
            ".format(
                fps=fps,
                input=file,
                thumb=thumb,
                output=output,
                )

    os.system('cmd /c "{executable} -y -loglevel warning {args}"'.format(
        executable=ffmpeg_path,
        args=args,
            )
        )
    print('==> Thumbnail created! [{}]'.format(datetime.now()-start))
    return output


def createFilmstrip(fps, file, interval, num_frames, version):
    start = datetime.now()
    output=os.path.join(version, os.path.basename(file).replace('.mov', '_filmstrip.jpg'))

    args = " \
        -r {fps} \
        -i {input} \
        -frames 1 \
        -vf \"scale=240:-1,select=not(mod(n\\,{interval})),tile={num_frames}x1\" \
        {output} \
            ".format(
                fps=fps,
                input=file,
                interval=interval,
                num_frames=num_frames,
                output=output,
                )

    os.system('cmd /c "{executable} -y -loglevel warning -stats {args}"'.format(
        executable=ffmpeg_path,
        args=args,
            )
        )
    print('==> Filmstrip created! [{}]'.format(datetime.now()-start))
    return output


def TranscodeFile(input):
    data = VideoData(input)
    dir = os.path.dirname(input)
    transcodes = os.path.join(dir,'transcodes')
    if not os.path.isdir(transcodes):
        os.mkdir(transcodes)

    version = os.path.join(transcodes, os.path.splitext( os.path.basename(input) )[0])
    if not os.path.isdir(version):
        os.mkdir(version)

    mp4 = createMP4(data['fps'], input, version)
    webm = createWebM(data['fps'], input, version)
    thumbnail = createThumbnail(data['fps'], input, data['thumb'], version)
    filmstrip = createFilmstrip(data['fps'], input, data['interval'], data['num_frames'], version)
    print('====> Finished! [{}]'.format(datetime.now()-start))
    return [mp4, webm, thumbnail, filmstrip]



if __name__ == '__main__':
    print('Running...')
    start = datetime.now()
    file = "Z:/Projects/Project_Data/test_002/sequences/seq_001/transcode_test/comp/review/transcode_test_comp_v001.mov"

    files = TranscodeFile(file)


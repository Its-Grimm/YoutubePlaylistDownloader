import os
import pytube
import subprocess
import pytube.exceptions
from pytube import Playlist

def downloadAudioFile(audioFile, outputPath, fileName):
    audioFile.download(output_path=outputPath, filename=fileName)


def mergeAudioFiles(fullAudioFile, addOnAudio, outputPath):
    mergedFile = os.path.join(outputPath, 'newFile.mp3') 
    try:
        # Does not print ffmpeg output
        subprocess.run(['ffmpeg', '-i', fullAudioFile, '-i', addOnAudio, '-filter_complex', '[0:0][1:0]concat=n=2:v=0:a=1[out]', '-map', '[out]', mergedFile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # Prints ffmpeg output
        # subprocess.run(['ffmpeg', '-i', fullAudioFile, '-i', addOnAudio, '-filter_complex', '[0:0][1:0]concat=n=2:v=0:a=1[out]', '-map', '[out]', mergedFile], check=True)
        print('Audio file merged successfully.\n')
        return mergedFile
    except subprocess.CalledProcessError as e:
        print('Error merging audio files:', e)
        return fullAudioFile


def getUserInput(prompt, valid_responses=None):
    while True:
        response = input(prompt).strip()
        if valid_responses is None or response.lower() in valid_responses:
            return response
        
        print('Invalid response, please try again.')


def main(): 
    link = getUserInput('Enter the Youtube playlist you wish to download: ')
    if 'playlist?' not in link:
        print('Only enter Youtube playlists, not regular videos or non-Youtube links! Try again!')
        return
    
    p = Playlist(link)
    outputPath = 'DownloadedMusic'
    os.makedirs(outputPath, exist_ok=True)
    
    downloadOrMerge = getUserInput(prompt='Do you want to download or download and merge? [d/DM] ', valid_responses=['d', 'dm']).lower()
    playlistTitle = str(p.title).replace(' ', '').replace('\'', '').replace('/', '')
    if downloadOrMerge == 'dm':
        playlistTitle += '.mp3'

    print('Downloading all files!' if downloadOrMerge == 'd' else 'Downloading and merging all files!')
    print('\n', playlistTitle, '\n')
    
    count = 1
    for video in p.videos:
        # print(count, '/', len(p), ': Downloading', video.title)
        print(f'{count}/{len(p)}: Downloading {video.title}')
        
        try:
            audioFile = video.streams.filter(only_audio=True).first()
            if downloadOrMerge.lower() == 'd':
                songOutputFolder = os.path.join(outputPath, playlistTitle)
                songName = f'{video.title}.mp3'
                os.makedirs(songOutputFolder, exist_ok=True)
                # Will simply overwrite song file if already exists/downloaded
                downloadAudioFile(audioFile, songOutputFolder, songName)
                    
            else:
                # Creates the master file only when downloading first track
                if count == 1:
                    downloadAudioFile(audioFile, outputPath, playlistTitle)
                    print("Master audio file created successfully.\n")
                
                # Adds each song to the master file
                else:
                    addonFileName = 'addon.mp3'
                    addonFilePath = os.path.join(outputPath, addonFileName)
                    masterAudioFilePath = os.path.join(outputPath, playlistTitle)
                    
                    downloadAudioFile(audioFile, outputPath, addonFileName)
                    mergedFile = mergeAudioFiles(masterAudioFilePath, addonFilePath, outputPath)   
                                
                    # Replaces the outdated master file with the new master file, and deletes the no-longer-needed addon file
                    os.replace(mergedFile, masterAudioFilePath)
                    os.remove(addonFilePath)
                
                    
        except pytube.exceptions.AgeRestrictedError as e:
            print(f'Skipping {video.title} due to age restriction: "{e}"\n')
        
        count += 1
        
    # print('\nDownloading all files!' if downloadOrMerge == 'd' else 'Downloading and merging all files!')
    print('\nAll files successfully downloaded!\n' if downloadOrMerge == 'd' else '\nAll files successfully downloaded and merged!\n')

if __name__ == '__main__': 
    main()  
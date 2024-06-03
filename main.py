import os
import time
import pytube
import subprocess
from pytube import Playlist
import pytube.exceptions

def downloadAudioFile(audioFile, outputPath, fileName):
    audioFile.download(output_path=outputPath, filename=fileName)


def mergeAudioFiles(fullAudioFile, addOnAudio, outputPath):
    mergedFile = os.path.join(outputPath, 'newFile.mp3')
    try:
        subprocess.run(['ffmpeg', '-i', fullAudioFile, '-i', addOnAudio, '-filter_complex', '[0:0][1:0]concat=n=2:v=0:a=1[out]', '-map', '[out]', mergedFile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # subprocess.run(['ffmpeg', '-i', fullAudioFile, '-i', addOnAudio, '-filter_complex', '[0:0][1:0]concat=n=2:v=0:a=1[out]', '-map', '[out]', mergedFile], check=True)
        print('Audio file merged successfully.\n')
        return mergedFile
    except subprocess.CalledProcessError as e:
        print('Error merging audio files:', e)
        return fullAudioFile


def main():    
    link = input('Enter the Youtube playlist you wish to download: ')
    if 'playlist' not in link:
        print('Only enter Youtube playlists, not regular videos or non-Youtube links! Try again!')
    else:
        p = Playlist(link)
        playlistTitle = str(p.title).replace(' ', '').replace('\'', '').replace('/', '') + '.mp3'
        outputPath = 'DownloadedMusic'
        os.makedirs(outputPath, exist_ok=True)
                
        print('\n', playlistTitle, '\n')
        
        count = 1
        for video in p.videos:
            masterAudioFilePath = os.path.join(outputPath, playlistTitle)
            print(count, '/', len(p), ': Downloading', video.title)
            
            try:
                audioFile = video.streams.filter(only_audio=True).first()
                
                # Creates the master file 
                if count == 1:
                    downloadAudioFile(audioFile, outputPath, playlistTitle)
                    print("Master audio file created successfully.\n")
                    
                # Adds to the master file
                else:
                    addonFileName = 'addon.mp3'
                    addonFilePath = os.path.join(outputPath, addonFileName)
                    downloadAudioFile(audioFile, outputPath, addonFileName)
                    
                    mergedFile = mergeAudioFiles(masterAudioFilePath, addonFilePath, outputPath)   
                                
                    # Replaces the outdated master file with the new master file, and deletes the no-longer-needed addon file
                    os.replace(mergedFile, masterAudioFilePath)
                    os.remove(addonFilePath)
                    
                    
            except pytube.exceptions.AgeRestrictedError as e:
                print('Skipping', video.title, 'due to error: \"', e, '\" \n')
            
            count += 1
                
            
        print('All files successfully downloaded and merged!\n')

if __name__ == '__main__': 
    main()  
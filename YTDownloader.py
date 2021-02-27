#!/usr/bin/env python


from pytube import YouTube, Playlist
from pytube.helpers import safe_filename
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
import re
import pathlib
import os, os.path
import moviepy.editor as mp


CodePath = pathlib.Path().absolute() #where the code is located

IconPath = str(CodePath) + "\YTDownloaderIcon.png"

def DownloadVideo():
    link = FileLinkInput.get()
    yt = YouTube(link)
    ys = yt.streams.get_highest_resolution() 
    
    location = FileLocationInput.get()
    ys.download(location)

def SoundDownload():

    link = FileLinkInput.get()
    yt = YouTube(link)
    location = FileLocationInput.get()
    
    ys = yt.streams.get_highest_resolution() 
    ys.download(location, filename="TemporaryFile")
                
    fileName = str(yt.title)
    newFileName = safe_filename(yt.title) + "_Audio"
    Ext = "mp3"
    clip = mp.AudioFileClip(location+"\TemporaryFile.mp4")
    clip.write_audiofile(os.path.join(location, f"{newFileName}.{Ext}"))
    clip.close()
    os.remove(location+"\TemporaryFile.mp4")

    
def PlaylistDownload():
        
    link = FileLinkInput.get()
    playlist = Playlist(link)
    location = FileLocationInput.get()   
    print(playlist.title)
    
    NumberOfFiles = 0
    NameExists = False
    FolderName = playlist.title
    FolderLocation = location
    Path = os.path.join(FolderLocation, FolderName) 
    FileLenght = len(location)
    
    if not os.path.exists(Path):
        NumberOfFiles = 0
        os.mkdir(Path)
        print(Path)
    else:
        while os.path.exists(Path):
            Path = Path+str(FileLenght)
    
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    #print('Number of videos in playlist: %s' % len(playlist.video_urls))
    for url in playlist.video_urls:
        yt = YouTube(url)
        ys = yt.streams.get_highest_resolution()
        ys.download(Path)
        
import tkinter as tk
from tkinter.ttk import *
from tkinter import PhotoImage

window = tk.Tk()
window.title("YTDownloader")

AppIcon = PhotoImage(file=IconPath)

Icon = tk.PhotoImage(file = IconPath)
IconResized = Icon.subsample(5, 5)

BackgroundPath = tk.PhotoImage(file = str(CodePath) + "\YTDownloaderBackground.png")

window.iconphoto(False,AppIcon)

window.configure(bg = "darkred")


Icon = tk.Label(window,text = "YTDownloader" ,image = IconResized,compound = tk.TOP,bg="darkred",fg="white").pack()

FileLinkInput = tk.Entry(window,width = 70,bg="red",fg="white")
FileLinkInput.insert(tk.INSERT, "Please Enter The Link Of The File/Playlist You Want To Download")
FileLinkInput.pack()

FileLocationInput = tk.Entry(window, width = 70,bg="red",fg="white")
FileLocationInput.insert(tk.INSERT, "Please Enter The Location You Want The File To Be Downloaded")
FileLocationInput.pack()

VideoDownloadButton = tk.Button(window, text="Click To Download Video",command = DownloadVideo ,width = 70, bg = "red",fg="white").pack()
SoundDownloadButton = tk.Button(window, text="Click To Download MP3 File",command = SoundDownload ,width = 70, bg = "red",fg="white").pack()
PlaylistDownloadButton = tk.Button(window, text="Click To Download Playlist",command = PlaylistDownload,width = 70, bg = "red",fg="white").pack()

label = tk.Label(window, text = "Thanks For Using YTDownloader",bg="darkred",fg="white").pack()

window.mainloop()

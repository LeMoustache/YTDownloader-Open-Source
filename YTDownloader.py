from pytube import YouTube, Playlist
from pytube.helpers import safe_filename
from time import sleep
import re
import pathlib
import os, os.path
from moviepy.audio.io.AudioFileClip import AudioFileClip


CodePath = pathlib.Path().absolute() #where the code is located

IconPath = str(CodePath)+"\Icons\YTDownloaderIcon.png"

def DownloadVideo():
    link = FileLinkInput.get()
    yt = YouTube(link)
    ys = yt.streams.get_highest_resolution() 
    
    location = ChosenDirectory
    print("Downloading..."+ys.title)
    ys.download(location)
    
    print(ys.title+" Downloaded!")
    print("In "+location)

def SoundDownload():

    link = FileLinkInput.get()
    yt = YouTube(link)
    location = ChosenDirectory
    
    ys = yt.streams.get_highest_resolution() 
    ys.download(location, filename="TemporaryFile")
                
    fileName = str(yt.title)
    newFileName = safe_filename(yt.title) + "_Audio"
    Ext = "mp3"
    clip = AudioFileClip(location+"\TemporaryFile.mp4")
    clip.write_audiofile(os.path.join(location, f"{newFileName}.{Ext}"))
    clip.close()
    os.remove(location+"\TemporaryFile.mp4")

    
def PlaylistDownload():
        
    link = FileLinkInput.get()
    playlist = Playlist(link)
    location = ChosenDirectory
    
    NumberOfFiles = 0
    NameExists = False
    FolderName = playlist.title
    FolderLocation = ChosenDirectory
    Path = os.path.join(FolderLocation, FolderName) 
    FileLenght = len(location)
    
    if not os.path.exists(Path):
        NumberOfFiles = 0
        os.mkdir(Path)
        print(Path)
    else:
        while os.path.exists(Path):
            Path = Path+str(FileLenght)
            
    print("Downloading..."+playlist.title)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    #print('Number of videos in playlist: %s' % len(playlist.video_urls))
    for url in playlist.video_urls:
        yt = YouTube(url)
        ys = yt.streams.get_highest_resolution()
        
        print("Downloading..."+ys.title)
        ys.download(Path)
        print(ys.title+" Downloaded!")
        
    print(playlist.title+" Downloaded!")
    print("In "+location)

        
import tkinter as tk
from tkinter.ttk import *
from tkinter import PhotoImage
from tkinter import filedialog as FileDialog

def browseFiles():
    global ChosenDirectory
    ChosenDirectory = FileDialog.askdirectory()
    FileLocationInput.delete("0","end")
    FileLocationInput.insert(tk.INSERT,ChosenDirectory)
    
def MP3Maker():
    MP4Video = FileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("MP4","*.MP4"),("all files","*.*")))
    print(MP4Video)
    
    VideoName = MP4Video.split("/")
    VideoName = VideoName[-1]
    MP3Name = VideoName.split(".")
    MP3Name = MP3Name[0]+".mp3"
    
    clip = AudioFileClip(MP4Video)
    clip.write_audiofile(os.path.join(ChosenDirectory,MP3Name))
    clip.close()
    
def PlaylistToMp3():
    
    link = FileLinkInput.get()
    playlist = Playlist(link)
    location = ChosenDirectory
    
    NumberOfFiles = 0
    NameExists = False
    FolderName = playlist.title
    FolderLocation = ChosenDirectory
    Path = os.path.join(FolderLocation, FolderName) 
    FileLenght = len(location)
    
    if not os.path.exists(Path):
        NumberOfFiles = 0
        os.mkdir(Path)
        print(Path)
    else:
        while os.path.exists(Path):
            Path = Path+str(FileLenght)
            
    print("Downloading..."+playlist.title)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    #print('Number of videos in playlist: %s' % len(playlist.video_urls))
    for url in playlist.video_urls:
        yt = YouTube(url)
        ys = yt.streams.get_highest_resolution()
        ys.download(Path, filename="TemporaryFile")
        print(playlist.title+" Downloaded!")
        print("In "+Path)
    
        fileName = str(yt.title)
        newFileName = safe_filename(yt.title) + "_Audio"
        Ext = "mp3"
        clip = AudioFileClip(Path+"\TemporaryFile.mp4")
        clip.write_audiofile(os.path.join(Path, f"{newFileName}.{Ext}"))
        clip.close()
        os.remove(Path+"\TemporaryFile.mp4")
        
def FolderToMp3():
    
    location = ChosenDirectory
    locationName = ChosenDirectory.split("\\")[-1]
    
    NumberOfFiles = 0
    NameExists = False
    Path = os.path.join(ChosenDirectory, locationName) 
    FileLenght = len(ChosenDirectory)
            
    VideoFolder = os.listdir(ChosenDirectory)
    print(VideoFolder)
    
    for videos in VideoFolder:
        print(videos)
        VideoFileName = videos
        fileName = str(videos)
        newFileName = safe_filename(VideoFileName) + "_Audio"
        Ext = "mp3"
        clip = AudioFileClip(Path+"/"+VideoFileName)
        clip.write_audiofile(os.path.join(Path, f"{newFileName}.{Ext}"))
        clip.close()
    
window = tk.Tk()
window.title("YTDownloader")

AppIcon = PhotoImage(file=IconPath)

Icon = tk.PhotoImage(file = IconPath)
IconResized = Icon.subsample(5, 5)

BackgroundPath = tk.PhotoImage(file = str(CodePath) + "\Icons\YTDownloaderBackground.png")

window.iconphoto(False,AppIcon)

window.configure(bg = "darkred")

TopFrame= tk.Frame(window).pack()

Icon = tk.Label(window,text = "YTDownloader" ,image = IconResized,compound = tk.TOP,bg="darkred",fg="white").pack()

FileLinkInput = tk.Entry(window,width = 70,bg="red2",fg="white")
FileLinkInput.insert(tk.INSERT, "Please Enter The Link Of The File/Playlist You Want To Download")
FileLinkInput.pack()

FileLocationInput = tk.Entry(window, width = 70,bg="red2",fg="white")
FileLocationInput.insert(tk.INSERT, "Please Enter The Location You Want The File To Be Downloaded")
FileLocationInput.pack()

button_explore = tk.Button(window, text = "Browse Files",command = browseFiles,width = 60, bg = "red2",fg="white")
button_explore.pack()

VideoDownloadButton = tk.Button(window, text="Click To Download Video",command = DownloadVideo ,width = 70, bg = "red3",fg="white").pack()
SoundDownloadButton = tk.Button(window, text="Click To Download MP3 File",command = SoundDownload ,width = 70, bg = "red3",fg="white").pack()
PlaylistDownloadButton = tk.Button(window, text="Click To Download Playlist",command = PlaylistDownload,width = 70, bg = "red3",fg="white").pack()
PlaylistMP3Button = tk.Button(window, text="Click To Convert A Playlist Into MP3",command = PlaylistToMp3,width = 70, bg = "red3",fg="white").pack()
MP3Maker = tk.Button(window, text="Click To Convert A File Into MP3",command = MP3Maker,width = 70, bg = "red3",fg="white").pack()
FolderMP3Maker = tk.Button(window, text="Click To Convert Folder Files Into MP3",command = FolderToMp3,width = 70, bg = "red3",fg="white").pack()


label = tk.Label(window, text = "Thanks For Using YTDownloader",bg="darkred",fg="white").pack()

window.mainloop()

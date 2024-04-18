# Importing all the important modules
import speedtest
from pytube import *
import speedtest
import requests
import time
import os
import re

cwd = os.getcwd()

# Greeting the user and telling hi/she that what this program does

print("\nDear user, thank you for choosing our program")
print("Before you starting using our program we want to first describe that what does our program do. Our program can do the following :\n")
# Defining the fuctions

# Defining a function to convert the time

def time_taken(timeTaken):
        TimeExtension = ""  # Initialize TimeExtension
        if (timeTaken < 60):
            timeTaken = int(timeTaken)
            TimeExtension = "Second(s)"
        if (timeTaken >= 60): # Converts to minutes
            timeTaken = timeTaken / 60
            TimeExtension = "Minute(s)"
        if (timeTaken >= 3600): # Converts to hours
            timeTaken = timeTaken / 3600
            TimeExtension = "Hour(s)"
        if (timeTaken >= 86400): # Converts to days
            timeTaken = timeTaken / 86400
            TimeExtension = "Days(s)"
    
        # Printing that how much time is taken to download the file
        print(f"\n\nTime taken to download the file is: {timeTaken} {TimeExtension}\n\n")

# defining a function to remove all the characters not accepted in filename
def remove_illegal_characters(text):
    # Define a regular expression pattern to match emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", flags=re.UNICODE)
    
    # Define a regular expression pattern to match illegal characters
    illegal_pattern = re.compile(r"[#%&{}\\<>*?/$!'\":@+`|=\s]+")

    # Remove emojis and illegal characters from the text
    cleaned_text = emoji_pattern.sub('', text)
    cleaned_text = illegal_pattern.sub(' ', cleaned_text)
    
    return cleaned_text

# Defining a function to show that how much percentage of the youtube video has been downloaded

def on_progress_pytube(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_complete = (bytes_downloaded / total_size) * 100

    # Print progress to the console (replace with your preferred output method)
    print(f"\nDownload Progress: {percentage_complete:.2f}%")

# Defining a function which will use the requests module to download data from normal websites
    
def file_downloader(url, filename=None, directory=None):
    try:

        starttime = time.time()
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Get total file size (if available in headers)
        total_size = int(response.headers.get('Content-Length', 0))

        if not filename:
            filename = "Downloaded File"  # Default filename if no name in URL

        # Construct the full output path
        if directory:
            output_path = os.path.join(directory, filename)

        else:
            output_path = os.path.join(os.getcwd(), filename)  # Use current directory if no output_dir provided

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Create directory structure if needed

        # Open the output file in binary write mode
        with open(output_path, "wb") as f:
            downloaded_bytes = 0
        for chunk in response.iter_content(1024):
            # Write the downloaded chunk to the file
            f.write(chunk)
            downloaded_bytes += len(chunk)

            # Calculate and display download progress
            percentage_complete = (downloaded_bytes / total_size) * 100
            print(f"Download Progress: {percentage_complete:.2f}%", end='\r')  # Print progress on same line

            print(f"\nFile Location :{output_path}")

        endtime = time.time()
        timeTotal = endtime - starttime
        time_taken(timeTotal)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading: {e}")



# Defining a function which will use the pytube module to download video from video streaming websites
def youtube_video_downloader(url, output_path, filename = None, resolution=None):

    # varaibles which helps to calculate time
    startTime = time.time()

    # Create a YouTube object using pytube
    yt = YouTube(url)

    # Register the progress callback function
    yt.register_on_progress_callback(on_progress_pytube)

    if resolution:
        video = yt.streams.filter(res=resolution).first()  # Or choose a different stream
    else:
        # Select the desired video stream (e.g., highest resolution)
        video = yt.streams.get_highest_resolution()  # Or choose a different stream

    # Set the output filename if provided
    if filename:
        print("\nPlease wait till the video is being dowloaded.\n")
        video.download(output_path, filename)
    else:
        print("\nPlease wait till the video is being dowloaded.\n")
        video.download(output_path)

    # Alerting the user that the video has been downloaded
    print(f"\nDownload complete: {video.title}")
    
    # Calculating the time taken to download the video
    endtime = time.time()
    timeTotal = endtime - startTime
    time_taken(timeTotal)

    # printing the location of the video
    location = output_path + "/" + filename
    print(f"\nVideo Location : {location}")

# Defining a function which will use the pytube module to download all the videos from a playlist from video streaming websites

def youtube_playlist_downloader(playlist_url, playlist_folder=None, resolution=None):
    try:
        # variable help will help to calculate the time taken

        startTime = time.time()

        # variable help will help to calculate that how many videos are downloaded from the playlist
        videos_downloaded = 1

        playlist = Playlist(playlist_url)

        # Asking the user to wait till his/her desired playlist is downloaded
        print("\n\nPlease, wait while we download your desired playlist.\n\n")

        # defining the playlist's title
        playlist_title = remove_illegal_characters(playlist.title)

        if (playlist_folder == None):
            playlist_folder = remove_illegal_characters(playlist_title)
        else:
            playlist_folder = playlist_folder
        
        # variable which will help to calculate that how many videos are downloaded
        totalVideos = len(playlist.video_urls)

        if not os.path.exists(playlist_folder):
            os.makedirs(playlist_folder)

        for index, video in enumerate(playlist.videos, start=1):
            video.register_on_progress_callback(on_progress_pytube)
            videoTitle = remove_illegal_characters(video.title)
            video_title = f"{index:02d}. {videoTitle}.mp4"
            video_path = os.path.join(playlist_folder, video_title)
            # Printing that which video is being downloaded
            print(f"\n\n Currently Downloading '{video_title}'... \n\n")

            # defining that in which resolution should we download the video
            if resolution:
                stream = video.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
            else:
                stream = video.streams.filter(progressive=True, file_extension='mp4').first()
            stream.download(output_path=playlist_folder, filename=video_title)

            # Alerting the user that a particular video has been downloaded
            print(f"\n\"{video_title}\" has been downloaded successfully !!")

            # Giving the user the location of the video
            print("\nThe video location of the video is :", video_path)


            # Giving the user that how many videos have been downloaded
            print("\n\nVideos downloaded :", videos_downloaded, "\n")

            # Calculating that how many videos are left to be downloaded
            playlist_download_progress = total_videos - videos_downloaded

            # Alerting the user that how many videos are left to be downloaded
            print("\n\nVideos left to be downloaded :", playlist_download_progress, "\n\n")

            # Incremeting the value fo videos_downloaded
            videos_downloaded = videos_downloaded + 1
            
        # Alerting the user that the wholke playlist has been successfully downlaoded
        print(f"\n\nThe playlist named \"{playlist_title}\" has been downloaded successfully !!")

        # Calculating the location of the playlist
        location = cwd + '/' + playlist_folder
        
        # Giving the user that where the playlist is saved
        print("\n\nThe location of the playlist is :", location)
        
        # Calculating the time taken to download the playlist
        endtime = time.time()
        timeTotal = endtime - startTime
        time_taken(timeTotal)
            
    
    # Handling errors
    except Exception as e:
        print("Error was found.")
        print("The exception was :", e)
    except KeyboardInterrupt:
        print("KeyBoard Interrupt Found. Exiting ...")


# Defining a function which will use the pytube module to download music by extracting it from a video from a video streaming websites

def youtube_music_downloader(url, directory, filename):
    
    # variable which will help to calculate the time taken to download the music from the video
    startTime = time.time()

    # Determing the filename
    if (filename == ""):
        filename = "downloaded_music.mp3"
    else:
        filename = filename  + '.mp3'

    yt = YouTube(url)

    # Register the progress callback function
    yt.register_on_progress_callback(on_progress_pytube)

    video = yt.streams.get_audio_only()

    video.download(directory, filename)

    # Calculating the time taken to download the music from the video
    endtime = time.time()
    timeTotal = endtime - startTime
    time_taken(timeTotal)

    # Determing the location of the file
    location = cwd + '/' + filename

    # Alerting the user with th location of the file/music
    print("The music file location is :", location)



# Defining a function which will use the speedtest module to show the internet upload and download speeds
def speed_test():
    startTime = time.time()
    # Create a Speedtest object
    st = speedtest.Speedtest()
    
    # Printing that the speed test is being done
    print("Running speed test...")
    
    # Telling the user that the download speed is being calculated
    print("Calculating the download speed ...")

    # Perform download speed test
    download_speed = st.download() / 1024 / 1024  # Convert to Mbps
    
    # Telling the user that the upload speed is being calculated
    print("Calculating the upload speed ...")

    # Perform upload speed test
    upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
    
    # Display the results
    print("\nDownload Speed: {:.2f} Mbps".format(download_speed))
    print("Upload Speed: {:.2f} Mbps".format(upload_speed))
    
    # Calculating the time taken to do the speed test
    endtime = time.time()
    timeTotal = endtime - startTime
    time_taken(timeTotal)


if __name__ == "__main__" :
# We have used try for error handiling
    try:
        # Giving all the options to the user
        print("\nChoose from the following: ")
        print("Press 1 for downloading Youtube Videos")
        print("Press 2 for downloading music from Youtube Videos")
        print("Press 3 for downloading files from normal websites.")
        print("Press 4 for dowloading the whole playlist from Youtube.")
        print("Press 5 for Interent speed test.")
        print("Press 6 for Exit.\n\n")

        # Asking the user for the ption he/she selected
        user_option = int(input("Enter the number beside your choosed option: "))

        # Asking for the url
        url = input("\nEnter the URL: ")

        # Asking for the file path
        filePath = input("\nEnter the file path (enter nothing for current file path): ")

        if not filePath:
            filePath = cwd
            filePath = os.path.join(filePath, "Downloaded Files")

        if user_option == 1:

            # Asking for fileName

            fileName = input("Enter the file name (noting for video title): ")

            # Asking for resolution

            resolution = input("Enter the resolution of the video (noting for 720p resolution): ")

            # Altering the user that the video is going to be downloaded

            video = YouTube(url)
            video = video.title
            print(f"Please wait ...\nWere are trying to download the video named : \"{video}\"")

            # Calling the function youtube_video_downloader to downlaod the video

            youtube_video_downloader(url, filePath, fileName, resolution)
        
        elif user_option == 2:

            # Asking for fileName

            fileName = input("Enter the file name (noting for video title): ")

            # Altering the user that the video is going to be downloaded

            video = YouTube(url)
            video = video.title
            print(f"Please wait ...\nWere are trying to download the music from the video named : \"{video}\"")

            # Calling the function youtube_video_downloader to downlaod the video

            youtube_music_downloader(url, filePath, fileName)

        elif user_option == 3:

            # Asking for fileName

            fileName = input("Enter the file name (noting for default filename): ")

            # Altering the user that the video is going to be downloaded

            video = YouTube(url)
            video = video.title
            print(f"Please wait ...\nWere are trying to download the music from the video named : \"{video}\"")

            print(f"Please wait ...\nWere are trying to download the music from the video named : \"{video}\"")

            # Calling the function file_downloader to downlaod the video

            file_downloader(url, fileName, filePath)

        elif user_option == 4:

            # Altering the user that the video is going to be downloaded

            playlist = Playlist(url)
            playlistTitle = playlist.title

            video_count = len(playlist.video_urls)

            # Printing the total number of video present in the playlist
            print(f"\n\nTotal number of videos in the playlist: {video_count}\n\n")

            # Asking the user that does he/she wants to really download the playlist

            check = input(f"Do you really wan to download the youtube playlist \"{playlistTitle}\" with {video_count} videos (y/n)? : ").lower()

            if check == "y":

                # Asking the user for the video resolution
                videoResolution = input("Choose a video resolution (nothing for highest video resolution): ")
                
                # Giving the details to the youtube_playlist_downloader function for downloading playlist
                
                youtube_playlist_downloader(url, filePath, videoResolution)

            elif check == "n":
                print("Exiting the program ....\n")

        elif user_option == 5:
            
            print("\n\nPlease Wait while we do the speed test. It takes around 20 to 60 seconds.\n\n")
            
            speed_test()

        elif user_option == 6:           
            print("\n\nExiting the program.....\n\n")


        # Alerting the user that the program has finished its work with some greetings
        print("Dear user, thank you for using our program.\nWe wish you a good day.")

    # Guiding the user to download all the required modules for running the prorgam
    except ModuleNotFoundError:
        print("Dear User, we kindly request you to download and install all the packages required for this program.")
        print("The modules required for this program are: ")
        print("SpeedTest - To install it type \"pip install speedtest-cli\" in your termimal.")
        print("PyTube - To install it type \"pip install pytube\" in your termimal.")
        print("PyTube - To install it type \"pip install pytube\" in your termimal.")
        print("OS - It is a built-in module")
        print("Time - It is a built-in module")
        print("Requests - It is a built-in module")
        print("Re - It is a built-in module")

    # Printing the error for the user to see that what error is coming
    # except Exception as e:
    #     print(f"Some error occured: {e}")
    except KeyboardInterrupt:
        print("KeyBoard Interrupt Found. Exiting ...")
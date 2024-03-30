# Importing all the important modules
import speedtest
from pytube import *
import speedtest
import requests
import time
import os

# Defining the fuctions

# Defining a function to show that how much percentage of the youtube video has been downloaded
def on_progress_pytube(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_complete = (bytes_downloaded / total_size) * 100

    # Print progress to the console (replace with your preferred output method)
    print(f"\nDownload Progress: {percentage_complete:.2f}%")

# Defining a function which will use the requests module to download data from normal websites
    
def file_downloader(url, output_filename, directory=None):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Get total file size (if available in headers)
        total_size = int(response.headers.get('Content-Length', 0))

        # Extract filename from URL or generate a default one
        if not output_filename:
            filename = os.path.basename(url)  # Extract filename from URL
        if not filename:
            filename = "download"  # Default filename if no name in URL

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
            print(f"\nFile Location :{directory}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading: {e}")



# Defining a function which will use the pytube module to download video from video streaming websites
def youtube_video_downloader(url, output_path=None, filename = None, resolution=None):
    startTime = time.time()
    if (output_path == None):
        output_path = os.getcwd()
    else:
        output_path = output_path

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

    print(f"\nDownload complete: {video.title}")
    

    endTime = time.time()
    timeTaken = endTime - startTime

    print(f"\nTime taken to download the file is: {timeTaken}")
    print(f"\nVideo Location :{directory}")

    global title
    title = video.title

# Defining a function which will use the pytube module to download all the videos from a playlist from video streaming websites

def youtube_playlist_downloader(playlist_url, playlist_name, output_path, video_resolution):

    os.mkdir(playlist_name)

    playlist_video_location = output_path + '/' + playlist_name

    playlist = Playlist(playlist_url)


    # declaring the value of video_download_completed variable to gui
    video_download_completed = 0

    # Loop through all videos in the playlist and download them
    for video_url in playlist.video_urls:
        try:
            # Download the video with the highest resolution
            yt = YouTube(video_url)
            if not video_resolution:
                stream = yt.streams.get_highest_resolution()
            else:
                stream = yt.streams.filter(res = video_resolution)
                
            filename = str(video_download_completed) + ". " + filename + '.mp4'

            stream.download(output_path=playlist_video_location, filename=filename) # Change the output path as needed
            print(f"Video Downloaded: {yt.title}")
            print(f"Videos left to download: {total_videos - video_download_completed}")

            video_download_completed = video_download_completed + 1
            print("Percentage of playlist downloaded :", video_download_completed + "%")

        # except Exception as e:
        #     print("Error downloading the following :")
        #     print(f"Video URL: {video_url}")
        #     print(f"\nYoutube Title: {yt.title}")
        #     print(f"\nException: {e}")
        except KeyboardInterrupt:
            print("KeyBoarddd...........")


# Defining a function which will use the pytube module to download music by extracting it from a video from a video streaming websites

def youtube_music_downloader(url, filename, directory):

    startTime = time.time()

    if (filename == ""):
        filename = url.split('/')[-1] + '.mp3'
    else:
        filename = filename  + '.mp3'

    yt = YouTube(url)

    # Register the progress callback function
    yt.register_on_progress_callback(on_progress_pytube)

    video = yt.streams.get_audio_only()

    video.download(directory, filename)

    endTime = time.time()
    timeTaken = endTime - startTime
    print(f"\nTime taken to download the file is: {timeTaken}")
    print(f"\nMusic File Location :{directory}")



# Defining a function which will use the speedtest module to show the internet upload and download speeds
def speed_test():
    startTime = time.time()
    # Create a Speedtest object
    st = speedtest.Speedtest()
    
    print("Running speed test...")
    
    # Perform download speed test
    download_speed = st.download() / 1024 / 1024  # Convert to Mbps
    
    # Perform upload speed test
    upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
    
    # Display the results
    print("Download Speed: {:.2f} Mbps".format(download_speed))
    print("Upload Speed: {:.2f} Mbps".format(upload_speed))
    
    endTime = time.time()
    timeTaken = endTime - startTime
    print(f"Time taken to do the speed test is: {timeTaken}")


if __name__ == "__main__" :
# We have used try for error handiling
    try:
        # Giving all the options to the user
        print("Choose from the following: ")
        print("Press 1 for downloading Youtube Videos")
        print("Press 2 for downloading music from Youtube Videos")
        print("Press 3 for downloading files from normal websites.")
        print("Press 4 for dowloading the whole playlist from Youtube.")
        print("Press 5 for Interent speed test.")
        print("Press 6 for Exit.")

        # Asking the user for the ption he/she selected
        user_option = int(input("Enter your choosed number/option: "))
        
        # Asking the user for the url where the file is saved
        url = input("Enter the url: ")

        # Asking the user for the filename by which the file should be saved
        filename = input("Enter the filename (enter nothing for default filename):")

        # Asking the user that where should we save the file
        directory = input("Enter the file path to save the file (nothing for current directory): ")

        if (user_option == 1):
            print("\nPlease wait until we load all the downloadable video resolutions.")

            # Asking the user for the video resolution
            videoResolution = input("Enter the video resolution (nothing for highest video resolution): ")

            youtube_video_downloader(url, directory, filename, videoResolution)

        elif (user_option == 2):
            youtube_music_downloader(url, filename, directory)

        elif (user_option == 3):
            file_downloader(url, filename, directory)

        elif (user_option == 4):

            playlist = Playlist(url)

            # Get the total number of videos in the playlist
            total_videos = len(playlist.video_urls)

            # Printing the total number of video present in the playlist
            print(f"\n\nTotal number of videos in the playlist: {total_videos}\n\n")

            # Asking the user that does he/she wants to really download the playlist
            check = input(f"Do you really wan to download the youtube playlist with {total_videos} (y/n)? : ").lower()

            if (check == 'y'):

                # Asking the user for the video resolution
                videoResolution = input("Choose a video resolution (nothing for highest video resolution): ")

                # Asking the user for the playlist name
                playlist_name = input("Enter the playlist name: ")

                print("\nHere the url you pasted should be the url to the playlist.\n")
                
                youtube_playlist_downloader(url, playlist_name, directory, videoResolution)

            elif(check == 'n'):
                print("\nExiting the program .....")

        elif (user_option == 5):
            print("\nThis process could take around 30 seconds to 60 seconds.")
            speed_test()

        elif (user_option == 6):
            print("Exiting the program ....")
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

    # Printing the error for the user to see that what error is coming
    except Exception as e:
        print(f"Some error occured: {e}")
    except TypeError:
        print("We recommend you to check that you have filled all the feilds correctly or not because this has caused an error.")
    except KeyboardInterrupt:
        print("KeyBoard Interrupt Found. Exiting ...")

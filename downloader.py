import os
import yt_dlp
from pathlib import Path

def getUrl():
    while(True):
        print("Enter the Youtube URL")
        inputUrl = input("> ")
        print("\nChecking URL...\n")

        ydl_opts = {'quiet': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(inputUrl, download=False)
            printColored("URL is valid\n", "green")
            return inputUrl
        except Exception:
            printColored("Invalid URL\n", "red")
            continue


def getFilePath():
    filePathDecider = {
        "y": True,
        "yes": True,
        "n": False,
        "no": False
    }


    while (True):
        print("Do you want to save the file in your Downloads folder? (Yes / no)")
        pathDecider = input("> ").lower()

        if not filePathDecider.get(pathDecider, True):
            return getCustomFilePath()

        defaultPath = os.path.join(Path.home(), "Downloads")
        printColored("Selected Downlods folder!\n", "green")
        return defaultPath


def getCustomFilePath():
    while(True):
        print("\nEnter path to your desired folder")
        customPath = input("> ")

        if not os.path.exists(customPath):
            printColored("Path doesn't excist\n", "red")
            continue

        if not os.path.isdir(customPath):
            printColored("Select a folder\n", "red")
            continue

        printColored(f"Selected '{customPath}'\n", "green")
        return customPath


def getFormatOption():
    mp4Options = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'}
    webmOptions = {'format': 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]'}
    mp3Options = {'format': 'bestaudio/best','postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',}]}
    m4aOptions = {'format': 'bestaudio/best','postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'm4a',
                        'preferredquality': '192',}]}
    
    format_options = {
        "1": mp4Options,
        "mp4": mp4Options,
        "2": webmOptions,
        "webm": webmOptions,
        "3": mp3Options,
        "mpe3": mp3Options,
        "4": m4aOptions,
        "m4a": m4aOptions
    }


    while (True):
        print("Select a format: ")
        print("[1] MP4 - Video (Default)")
        print("[2] WebM - Video")
        print("[3] MP3 - Sound only")
        print("[4] M4A - Sound only")

        inputFormat = input("> ")
        inputFormatlower = inputFormat.lower()

        format_option = format_options.get(inputFormatlower, None)

        if not format_option:
            printColored(f"{inputFormat} is not a valid format\n", "red")
            continue
        
        #TODO 
        #printColored(f"Selected '{inputFormat}'", "green")
        return format_option


def downloadFile(url, path, options):
    options["outtmpl"] = os.path.join(path, '%(title)s.%(ext)s')
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        printColored("Download completed successfully!", "green")
        print(f"File saved in: {path}")
    except Exception as e:
        printColored(f"An error occurred: {str(e)}", "red")


def printColored(text, color):
    if color == "red":
        print(f"\033[31m{text}\033[0m")
    elif color == "green":
        print(f"\033[32m{text}\033[0m")
    else:
        print(text)


def main():
    print("YOUTUBE DOWNLOADER\n")

    url = getUrl()
    
    path = getFilePath()

    format_option = getFormatOption()

    downloadFile(url, path, format_option)



# print(os.path.join(downloads_folder, '%(title)s.%(ext)s'))

if __name__ == "__main__":
    main()

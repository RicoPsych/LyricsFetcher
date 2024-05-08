import asyncio
import time
import azlyrics.azlyrics
import re
import unidecode
import tekstowo as tekstowo

from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

# https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python
async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        info = await current_session.try_get_media_properties_async()

        # song_attr[0] != '_' ignores system attributes
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        # converts winrt vector to list
        info_dict['genres'] = list(info_dict['genres'])

        return info_dict, current_session.source_app_user_model_id


def parse_az_lyrics(value: str) :
    value = value.lower()
    value = re.sub(r'\W+','', value)
    return value

def parse_tekstowo(value:str):
    value = value.lower().replace("&","")
    value = re.sub(r'\W+','_', value)
    return value

def removeCommonStrings(value:str):
    tokens = [" (Official Audio)"," (Official Video)"," (Official Music Video)", " (Official Visualizer)", "  (Official HD Video)", "[LYRICS]"]    
    for token in tokens:
        token_replace = re.compile(re.escape(token),re.IGNORECASE)
        value = token_replace.sub('',value)
#        value = value.replace(token,"")
    return value

def parseTitle(title:str,artist:str):
    return removeCommonStrings(title.replace(artist,"").strip().removeprefix("-")).strip()

def parseArtist(artist:str):
    return artist.replace(" - Topic","").replace("VEVO","").removeprefix("The").removeprefix("the").removesuffix("Official").rstrip().strip()




if __name__ == '__main__':
    old_title = ""
    old_artist = ""
    while(True):
        current_media_info,music_app_name = asyncio.run(get_media_info())
        artist = str(current_media_info["artist"])
        album_title = str(current_media_info["album_title"])
        title = str(current_media_info["title"])

        artist = parseArtist(artist)
        title = parseTitle(title,artist)
        if(artist != old_artist or title != old_title):
            old_title = title
            old_artist = artist
            if(len(artist) == 0 and len(title) == 0):
                continue

            print("_____________________________________________")
            print(f"Artist: {artist}\nAlbum: {album_title}\nSong: {title}")
            print("_____________________________________________")
            
            lyrics_source = ""
            wd = azlyrics.azlyrics.lyrics(parse_az_lyrics(artist), parse_az_lyrics(title))
            lyrics_source = "AZLyrics"
            if len(wd) == 1:
                wd = tekstowo.lyrics(parse_tekstowo(artist),parse_tekstowo(title))         
                lyrics_source = "Tekstowo"
            if len(wd) != 1:
                for line in wd:
                    print(line.strip("\n"))
                    print("_____________________________________________")
                    print(f"Lyrics source: {lyrics_source}")    
                    break

        time.sleep(1)
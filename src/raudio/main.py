#!/usr/bin/env python3

from dataclasses import dataclass, asdict
import logging
import json

import requests

HOST = 'https://127.0.0.1'
PORT = 8080

@dataclass(frozen=True, order=True)
class Song:
    title     : str 
    album     : str = None 
    artist    : str = None
    album_art : str = None # For now, assume the album art is a url to an image

class Raudio:
    def __init__(self, hostname, port) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        self.hostname = hostname
        self.port     = port

    def establish_connection(self):
        '''Makes an HTTP request to establish a connection to the server. After,
        should establish an event listener for the UDP stream'''
        raise NotImplementedError()
        
    def close_connection(self) -> bool:
        '''Makes an HTTP request to the api requesting to close and terminates
        the stream, returns True if successful, False otherwise'''
        raise NotImplementedError()

    def request_track_info(self) -> Song | None:
        '''Makes an HTTP request to request what song is playing. Returns the
        song with the song, or None if no song is playing'''
        resp = requests.get(f'{self.hostname}:{self.port}/song')

        if resp.status_code != 200:
            self.logger.error('Error in making request to api')
            return
        
        data = resp.json()

        return Song(
            data['title'],
            data['album']     if 'album'     in data else None,
            data['artist']    if 'artist'    in data else None,
            data['album_art'] if 'album_art' in data else None
        )

    def request_track(self, requested_song: Song) -> Song:
        '''Makes an HTTP request to request a track. Returns the track if the 
        request is successful'''
        self.logger.log(f'Requesting the following song: {asdict(requested_song)}')
        body = json.dumps(asdict(requested_song))

        resp = requests.post(f'{self.hostname}:{self.port}/request', data=body)

        if resp.status_code != 200:
            self.logger.error('Error in making request to api')
            return
        
        return requested_song

    def pause_track(self) -> bool:
        '''Makes an HTTP request to the api to pause the current track, returns
        True if the request is successful, False otherwise'''
        resp = requests.put(f'{self.hostname}:{self.port}/pause')

        if resp.status_code != 200:
            self.logger.error('Error in making request to api')
            return False
    
        return True

    def request_skip(self) -> Song | None:
        '''Makes an HTTP request to the api for the current song to be skipped, 
        returns None if the request fails or there is no song playing.'''
        resp = requests.put(f'{self.hostname}:{self.port}/play')

        if resp.status_code != 200:
            self.logger.error('Error in making request to api')
            return
        
        data = resp.json()

        return Song(
            data['title'],
            data['album']     if 'album'     in data else None,
            data['artist']    if 'artist'    in data else None,
            data['album_art'] if 'album_art' in data else None
        )

if __name__ == '__main__':
    raudio = Raudio(HOST, PORT)
    print(raudio)
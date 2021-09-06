# -*- coding: utf-8 -*-
#
# Advanced Emulator Launcher: API
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

#
# API client to connect to AEL server to retrieve ROM data.
#

# --- Python standard library ---
from __future__ import unicode_literals
from __future__ import division
from __future__ import annotations

import abc
import logging
import typing

# AEL modules
from ael.utils import net, io

logger = logging.getLogger(__name__)

###############################################################
# CLIENT METHODS
###############################################################
def client_get_rom(host: str, port:int, rom_id:str) -> ROMObj:
    uri = 'http://{}:{}/query/rom/?id={}'.format(host, port, rom_id)
    rom_data = net.get_URL_as_json(uri)    
    return ROMObj(rom_data)

def client_get_roms_in_collection(host: str, port:int, rom_collection_id:str) -> typing.List[ROMObj]:
    uri = 'http://{}:{}/query/romcollection/roms/?id={}'.format(host, port, rom_collection_id)
    rom_data = net.get_URL_as_json(uri)
    roms = []
    for rom_entry in rom_data:
        roms.append(ROMObj(rom_entry))
    return roms

def client_get_collection_launchers(host:str, port:int, rom_collection_id:str) -> dict:
    uri = 'http://{}:{}/query/romcollection/launchers/?id={}'.format(host, port, rom_collection_id)
    launchers = net.get_URL_as_json(uri)
    return launchers

def client_get_rom_launcher_settings(host: str, port:int, rom_id: str, launcher_id:str) -> dict:
    uri = 'http://{}:{}/query/rom/launcher/settings/?id={}&launcher_id={}'.format(host, port, rom_id, launcher_id)
    launcher_settings = net.get_URL_as_json(uri)    
    return launcher_settings

def client_get_collection_launcher_settings(host: str, port:int, rom_collection_id: str, launcher_id:str) -> dict:
    uri = 'http://{}:{}/query/romcollection/launcher/settings/?id={}&launcher_id={}'.format(host, port, rom_collection_id, launcher_id)
    launcher_settings = net.get_URL_as_json(uri)    
    return launcher_settings

def client_get_collection_scanner_settings(host: str, port:int, rom_collection_id: str, scanner_id:str) -> dict:
    uri = 'http://{}:{}/query/romcollection/scanner/settings/?id={}&scanner_id={}'.format(host, port, rom_collection_id, scanner_id)
    scanner_settings = net.get_URL_as_json(uri)    
    return scanner_settings

def client_post_launcher_settings(host: str, port:int, data: dict) -> bool:
    uri = 'http://{}:{}/store/launcher/'.format(host, port)
    response_data, code = net.post_JSON_URL(uri, data)
    return code == 200

def client_post_scanner_settings(host: str, port:int, data: dict) -> bool:
    uri = 'http://{}:{}/store/scanner/'.format(host, port)
    response_data, code = net.post_JSON_URL(uri, data)
    return code == 200

def client_post_scanned_roms(host: str, port:int, data: dict) -> bool:
    uri = 'http://{}:{}/store/roms/added'.format(host, port)
    response_data, code = net.post_JSON_URL(uri, data)
    return code == 200

def client_post_dead_roms(host: str, port:int, data: dict) -> bool:
    uri = 'http://{}:{}/store/roms/dead'.format(host, port)
    response_data, code = net.post_JSON_URL(uri, data)
    return code == 200

def client_post_scraped_rom(host: str, port:int, data: dict) -> bool:
    uri = 'http://{}:{}/store/rom/updated'.format(host, port)
    response_data, code = net.post_JSON_URL(uri, data)
    return code == 200

def client_post_scraped_roms(host: str, port:int, data: dict) -> bool:
    uri = 'http://{}:{}/store/roms/updated'.format(host, port)
    response_data, code = net.post_JSON_URL(uri, data)
    return code == 200

###############################################################
# CLIENT OBJECTS
###############################################################
class MetaDataObj(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, entity_data: dict = None):
        if entity_data is None:
            entity_data = {}
        self.entity_data = entity_data

    def get_id(self) -> str:
        return self.entity_data['id'] if 'id' in self.entity_data else None

    def get_data_dic(self):
        return self.entity_data

    def get_custom_attribute(self, key, default_value = None):
        return self.entity_data[key] if key in self.entity_data else default_value

    # --- Metadata --------------------------------------------------------------------------------
    def get_name(self):
        return self.entity_data['m_name'] if 'm_name' in self.entity_data else None

    def get_releaseyear(self):
        return self.entity_data['m_year'] if 'm_year' in self.entity_data else None

    def get_genre(self) -> str:
        return self.entity_data['m_genre'] if 'm_genre' in self.entity_data else None

    def get_developer(self) -> str:
        return self.entity_data['m_developer'] if 'm_developer' in self.entity_data else None

    def get_rating(self):
        return int(self.entity_data['m_rating']) if self.entity_data['m_rating'] else None

    def get_plot(self):
        return self.entity_data['m_plot'] if 'm_plot' in self.entity_data else None
        
    def get_number_of_players(self):
        return self.entity_data['m_nplayers']

    def get_esrb_rating(self):
        return self.entity_data['m_esrb']
        
    def has_asset(self, asset_id:str) -> bool:
        if 'assets' in self.entity_data: return False
        return asset_id in self.entity_data['assets']

    def get_data_dic(self):
        return self.entity_data
    
    def set_name(self, name):
        self.entity_data['m_name'] = name

    def set_releaseyear(self, releaseyear):
        self.entity_data['m_year'] = releaseyear

    def set_genre(self, genre):
        self.entity_data['m_genre'] = genre

    def set_developer(self, developer):
        self.entity_data['m_developer'] = developer

    def set_rating(self, rating):
        try:
            self.entity_data['m_rating'] = int(rating)
        except:
            self.entity_data['m_rating'] = ''

    def set_plot(self, plot):
        self.entity_data['m_plot'] = plot
    
    def set_number_of_players(self, amount):
        self.entity_data['m_nplayers'] = amount
        
    def set_esrb_rating(self, esrb):
        self.entity_data['m_esrb'] = esrb

    def set_asset(self, asset_id:str, asset_path:str):
        self.entity_data['assets'][asset_id] = asset_path
    
class ROMObj(MetaDataObj):

    def get_scanned_by(self) -> str:
        return self.entity_data['scanned_by_id'] if 'scanned_by_id' in self.entity_data else None
       
    def set_file(self, file: io.FileName):
        self.entity_data['filename'] = file.getPath()     

    def get_file(self):
        if not 'filename' in self.entity_data: return None
        path = self.entity_data['filename']
        if path == '': return None

        return io.FileName(path)

    def set_platform(self, platform): 
        self.entity_data['platform'] = platform   

    def get_platform(self): 
        return self.entity_data['platform']
    
    def get_asset_path(self, assetinfo_id: str) -> io.FileName:
        asset_paths = self.entity_data['asset_paths'] if 'asset_paths' in self.entity_data else {}
        return asset_paths[assetinfo_id] if assetinfo_id in asset_paths else None
     
    @staticmethod
    def get_data_template() -> dict:
        return {
             'id': '',
             'm_name': '',
             'm_year': '',
             'm_genre': '',
             'm_developer': '',
             'm_rating': '',
             'm_plot': '',
             'm_nplayers': '',
             'm_esrb': '',
             'platform': '',
             'filename': '',
             'scanned_by_id': '',
             'assets': {},
             'asset_paths': {}
         }
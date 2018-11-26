# ----------------------------------------------------------------------------
# Copyright (c) 2016--, BacDivePy development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import
import requests
from requests.exceptions import Timeout
from warnings import warn
import configparser
import json
from os import environ, path
from getpass import getpass
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
import pandas as pd
import numpy as np

from bacdive.build_url import get_url
from bacdive.clean import clean_cat,flatten_df

def retrieve(search,search_type): # pragma: no cover
    
    build_final=[]
    if not isinstance(search, list):
        search=[search]
    
    for search_value in search:
        flat_dfs=[]
        url=get_url(search_value,search_type)

        if search_type=='bacdive_id':
            locations={'count': 1,'next': None,'previous': None,'results': [{'url': url}]}
        else:
            try:
                locations=Dive(url).call()
            except:
                warn('no information found for: '+str(search_value))
                continue

        if isinstance(locations, dict):
            for ulrloc in tqdm(locations['results']):
                df_=flatten_df(Dive('%s?format=json'%ulrloc['url']).call())
                df_['DSMZ_id']=[ulrloc['url'].split('/')[-2]]*df_.shape[0]
                df_.index=(df_['DSMZ_id']+'||'+df_['Section']+'||'+df_['Subsection']+'||'+df_['Field_ID']).values
                flat_dfs.append(df_)
        if isinstance(locations, list):
            for ulrloc in tqdm(locations):
                df_=flatten_df(Dive('%s?format=json'%ulrloc['url']).call())
                df_['DSMZ_id']=[ulrloc['url'].split('/')[-2]]*df_.shape[0]
                df_.index=(df_['DSMZ_id']+'||'+df_['Section']+'||'+df_['Subsection']+'||'+df_['Field_ID']).values
                flat_dfs.append(df_)
        flat_dfs = pd.concat(flat_dfs)
        flat_dfs = flat_dfs.groupby(flat_dfs.index)['Field'].apply(list)
        build_final.append(flat_dfs)

    build_final = clean_cat(pd.DataFrame(build_final).T)
    return build_final


def DSMZ_login(username, password=None, timeout=30): # pragma: no cover

    """
    Get an authentication token for SEED web services.
    
    The authentication token is also stored in the .patric_config file in
    the user's home directory. The SeedClient object retrieves the
    authentication token from the file so the user does not need to keep
    getting a new token.
    
    Parameters
    ----------
    username : str
    User name
    password : str, optional
    Password or None to prompt and enter password
    timeout : integer
    Number of seconds to wait for response
    
    Returns
    -------
    str
    User ID (which can be different than user name)
    """
        
    # Prompt for a password if not specified.
    if password is None:
        password = getpass(prompt='{0} password: '.format('BacDive'))

    # Get an authentication token from the specified web service.
    headers = {'Accept': 'application/json'}
    credentials = HTTPBasicAuth(username, password)
    
    try:
        response = requests.get('https://bacdive.dsmz.de/api/bacdive/sequence/%s/' % ('ALAS01000001')
                                , headers=headers,auth=credentials, timeout=timeout)
    except Timeout as e:
        warn('The DSMZ BacDive authentication service did not return a response within {0} seconds. '
             'Try again with a larger timeout value. (Details: {1})'.format(timeout, e))
        return None
    if response.status_code != requests.codes.OK:
        raise ValueError(response.json()['detail'])
        
    # Save the authentication data in config file.
    config_file = path.join(environ['HOME'], '.DSMZ_config')
    config = configparser.ConfigParser()
    config.read(config_file)
    if not config.has_section('authentication'):
        config.add_section('authentication')
    config.set('authentication', 'password', password)
    config.set('authentication', 'user_id', username)
    config.write(open(config_file, 'w'))
    
    return username

class AuthenticationError(Exception): # pragma: no cover
    """ Exception for problem with login authen. """

class Dive(object): # pragma: no cover
    
    """ Client for DSMZ BacDive web services """
    
    def __init__(self, url):
        
        """ Initialize object.
        
        Parameters
        ----------
        url : str, URL of service endpoint
        Authentication token for SEED web services, when None get the
        token from the .patric_config file when calling a method
        
        """
        
        self.url = url
        self.password=None
        self.username=None
        return


    def call(self, timeout=1800): # pragma: no cover
        
        """ Call a server and wait for the response.
        
        Parameters
        ----------
        Dictionary of input parameters for method
        timeout : integer
        Number of seconds to wait for response
        
        Returns
        -------
        data
        Output of method in JSON format
        
        Raises
        ------
        ServerError
        When server returns an error response
        """
            
        # If needed, look for the authentication token in the Patric config file.
        if self.password is None or self.username is None:
            self.retrieve_authentication()
        
        header = {'Accept': 'application/json'}
        credentials = HTTPBasicAuth(self.username , self.password)
        # Send the request to the server and get back a response.
        response = requests.get(self.url,headers=header,auth=credentials, timeout=timeout)

        if response.status_code == requests.codes.server_error:
            if 'content-type' in response.headers and response.headers['content-type'] == 'application/json':
                raise ValueError(response.json()['detail'])
            else:
                raise ValueError(response.text)

        if response.status_code != requests.codes.OK:
            response.raise_for_status()
        return response.json()  # Get the output from the method in the response


    def retrieve_authentication(self): # pragma: no cover
        
        """ 
        Retrieve the authentication username and password from the config file.

        Raises
        ------
        AuthenticationError
        When there is a problem with the authentication section in the config file
        
        """

        config = configparser.ConfigParser()
        config.read(path.join(environ['HOME'], '.DSMZ_config'))
        try:
            self.username = config.get('authentication', 'user_id')
            self.password = config.get('authentication', 'password')
        except (configparser.NoSectionError, configparser.NoOptionError):
            self.password = None
            raise AuthenticationError('Call DSMZ_login() to login to the API before proceeding')
        return




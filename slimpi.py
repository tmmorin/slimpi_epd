#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8


# In[1]:


#get_ipython().run_line_magic('load_ext', 'autoreload')
#get_ipython().run_line_magic('autoreload', '2')

#get_ipython().run_line_magic('reload_ext', 'autoreload')




# In[12]:


#get_ipython().run_line_magic('alias', 'nbconvert nbconvert ./slimpi.ipynb')




# In[13]:


#get_ipython().run_line_magic('nbconvert', '')



# # NOTES
# * to properly run pyinstaller: 
#     * `pipenv run python -m PyInstaller --clean slimpi.spec`
# * Install PyInstaller
#     * use the following to install the development branch of PyInstaller: 
#         * `pipenv install -e git+https://github.com/pyinstaller/pyinstaller.git@develop#egg=PyInstaller`
#     * build the bootloader for this platform: 
#         * `python /home/pi/.local/share/virtualenvs/slimpi_epd-b1Rf9la8/src/pyinstaller/bootloader/waf all`
# * Ubuntu Regular Font appears to truncate the last few characters with long strings in some situations; this does not appear to occur with other fonts. 
# 
# * The release version of PyInstaller (v 3.5 July 9, 2019) has a [bug related to pipenv and distuitls] (https://github.com/pyinstaller/pyinstaller/issues/4064#issuecomment-568272182) that results in PIL being unable to open images properly.
#     * PyInstaller does not appropriately find all of the paths and modules within the pipenv and therefore needs to be installed directly in the pipenv rather than a system-wide with pip
#     * Resolve all of the above by installing the `develop` branch within the pipenv:
#         * `pipenv install -e git+https://github.com/pyinstaller/pyinstaller.git@develop#egg=PyInstaller`
#     * pipenv does not build all of the bootloaders needed for the Raspberry Pi architecture (ARMv6). Resolve this by [building for this plaform] (https://pyinstaller.readthedocs.io/en/stable/bootloader-building.html):
#         * `python ~/.local/share/virtualenvs/slimpi_epd-b1Rf9la8/src/pyinstaller/bootloader/waf all`
# 
# # TO DO
# ## General
# - [x] order parts at RS https://nl.rs-online.com/web/ca/overzichtwinkelwagen/
# - [ ] document and publish case
#     - [ ] move hole in front down thickness of two washers 
# - [ ] create a runnable package that does not depend on pipenv
#     - [ ] something is still broken in pyinstaller/PIL and jpg images are not loaded properly see: https://github.com/notifications/beta/MDE4Ok5vdGlmaWNhdGlvblRocmVhZDQ1MDMyMjU1NjoxNDI2MjUwNQ==?query=&show_full=true
#     - [ ] switch to single file mode for pyinstaller 
#     - pipenv and PyInstaller are not playing nice and have an issue with distutils not being added properly see this link for help: https://stackoverflow.com/questions/59444914/pyinstaller-failing-to-import-distuitls-when-used-with-pipenv/59444915#59444915 - this has already been patched in the PyInstaller hooks directory for *this* project 
#   - see /home/pi/.local/share/virtualenvs/slimpi_epd-b1Rf9la8/lib/python3.7/site-packages/PyInstaller/hooks/pre_find_module_path/hook-distutils.py
#   
# ```
# from PyInstaller.utils.hooks import logger
# 
# 
# def pre_find_module_path(api):
#     # Absolute path of the system-wide "distutils" package when run from within
#     # a venv or None otherwise.
#     distutils_dir = getattr(distutils, 'distutils_path', None)
#     if distutils_dir is not None:
#         # workaround for https://github.com/pyinstaller/pyinstaller/issues/4064
#         if distutils_dir.endswith('__init__.py'):
#             distutils_dir = os.path.dirname(distutils_dir)
# 
#         # Find this package in its parent directory.
#         api.search_dirs = [os.path.dirname(distutils_dir)]
#         logger.info('distutils: retargeting to non-venv dir %r' % distutils_dir)  
# ```
# - [ ] create installation scripts for building, deploying
# 
# ## Building
# - [ ] ~~move waveshare_epd as a static library into project? pyinstaller chokes on this - unclear why~~
# - [ ] write script that does the following build steps:
#     - [ ] check build environment:
#         * Install needed pipenv modules
#             * 
#         * Build appropriate bootloaders
#         * 
# 
# 
# ## Structure
# - [x] move classes out of main program structure
# - [ ] Test with smaller screen
# - [ ] speed up initialization - what takes so long?
# - [ ] configuration module can probably be improved to ignore non-set commandline options -see notes in file
# - [ ] move all the support files into the library folder or something similar???
# - [x] *THIS MAY NOT BE NEEDED* add hook-waveshare_epd file to assist pyinstaller in finding the waveshare libraries for the module load in the main function
#    - [x] solved by explicitly including waveshare_epd in slimpi.py 
#    ```
#    from PyInstaller.utils.hooks import collect_submodules
#    hidenimports = collect_submodules('waveshare_epd')
#    ```
# 
# ## Bugs
# - [x] image does not appear to hcenter
# - [ ] TextBlock does not use padding
# - [X] configuration always kicks error for "unknown options" even when none are specified
# - [x] Compiled version cannot use images that are downloaded - add more verbose debugging around this to figure out why
#   - [x] Due to issue with distutil, virtual env and pyInstaller (see notes above)
# - [ ] splash_screen = False does not work
# 
# ## Logging
# - [x] change destination for log files - /var/log? - this may be handled by moving to a daemon model and allowing the system to manage logging
# - [ ] filtering of log files filter based on source module?
# - [X] WARNING with log level is uneeded
# - [X] some "DEBUG" level messages still slip through even when set to "WARNING"
# - [X] should /etc/slimpi.cfg missing be a warn level event? - probably not
# 
# 
# ## Configuration
# - [ ] method for installing user config?
# - [ ] script for installing as daemon
# 
# ## Testing
# - [x] Test and confirm command line switches
#   - [x] -p --player-name
#   - [X] -l --log-level
#   - [x] -c --config
#   - [X] -s --list-servers
#   - [x] -V --version 
# - [x] Meta/help strings are a mess in command line switches
# 
# ## Daemon
# - [ ] implement daemon start/stop/restart features
# - [ ] https://www.python.org/dev/peps/pep-3143 - instructions: https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/
# - [ ] restart on crash
# - [ ] **This** is likely the best way forward: https://stackoverflow.com/questions/13069634/python-daemon-and-systemd-service
# 
# ## Documentation
# - [ ] README.md in epdlib module
# - [ ] comsistently document attributes, methods 
# 
# ## Feature Creep
# - [x] Clock that tells time as 'Quarter to Eight' or 'Half past Nine' or 'Ten after Seven'
# - [ ] disable the Pi power/activity lights https://www.jeffgeerling.com/blogs/jeff-geerling/controlling-pwr-act-leds-raspberry-pi
# - [ ] Repurpose the Pi lights to show heartbeat/activity/other https://raspberrypi.stackexchange.com/questions/697/how-do-i-control-the-system-leds-using-my-software
# - [ ] add a decimal doted binary clock
# 


# In[19]:


import logging
import logging.config

# from pathlib import Path
# change directory to the location where the script is running
from os import chdir

# parse arguments
import sys

# handle importing libraries based on config file
import importlib

# loop delay - sleep
from time import sleep

# clock
from datetime import datetime

##### PyPi Modules #####
# handle http requests
import requests

# rate limit the queries on the LMS server
from ratelimiter import RateLimiter

# lmsquery-fork for managing communications with lms server
import lmsquery




# In[20]:


import constants
import epdlib
from library import configuration
from library import signalhandler
from library import cacheart

import waveshare_epd # explicitly import this to make sure that PyInstaller can find it




# In[7]:


def test_epd():
    import layouts
    epd = importlib.import_module('waveshare_epd.epd5in83')
    s = epdlib.Screen()
    s.epd = epd.EPD()
    l = epdlib.Layout(layout=layouts.test)
    u = {'a': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse laoreet mauris vel felis convallis, id maximus felis tincidunt.', 
         'wb': 'Donec consequat felis ut sem aliquam, in consectetur dolor pellentesque. Donec nec velit faucibus, dignissim mauris congue, eleifend tellus.', 
         'c1': 'Donec vitae leo sed nibh pulvinar tristique. Interdum et malesuada fames ac ante ipsum primis in faucibus. ',
         'c2': 'Aenean blandit, mi non iaculis placerat, libero urna elementum nisi, vel sodales eros odio non massa. '}
    l.update_contents(u)
    s.elements = l.blocks.values()
    s.concat()
    s.initEPD()
    s.clearEPD()
    s.initEPD()

    s.writeEPD()
    return s.concat()
    




# In[8]:


def do_exit(status=0):
    if 'TESTING' in globals():
        if TESTING:
            logging.fatal(f'Exit called, but ignored due to global var `TESTING` = {TESTING}')
    else:
        sys.exit(status)




# In[9]:


def scan_servers():
    """scan for and list all available LMS Servers and players"""
    print(f'Scanning for available LMS Server and players')
    servers = lmsquery.scanLMS()
    if not servers:
        print('Error: no LMS servers were found on the network. Is there one running?')
        do_exit(1)
    print('servers found:')
    print(servers)
    players = lmsquery.LMSQuery().get_players()
    # print selected keys for each player
    keys = ['name', 'playerid', 'modelname']
    for p in players:
        print('players found:')
        try:
            for key in keys:
                print(f'{key}: {p[key]}')
            print('\n')
        except KeyError as e:
            pass 




# In[23]:


def main():
    
    
    ########## CONSTANTS #########
    # pull the absolute path from the constants file that resides in 
    # the root of this project
    absPath = constants.absPath
    chdir(absPath)
    
    version = constants.version
    app_name = constants.app_name
    app_long_name = constants.app_long_name
    url = constants.url
    # this is a bit of a kludge to fix the relative path issues associated with pyinstaller
#     logging_cfg = Path(absPath) / Path(constants.logging_cfg)
    logging_cfg = constants.logging_cfg
#     default_cfg = Path(absPath) / Path(constants.default_cfg)
    default_cfg = constants.default_cfg
    system_cfg = constants.system_cfg
    user_cfg = configuration.fullPath(constants.user_cfg)
#     noartwork = Path(absPath) / Path(constants.noartwork)
    noartwork = constants.noartwork
    
   
    print('*'*20)
    print(f'abspath {absPath}')
    print(f'logging_cfg {logging_cfg}')
    print(f'default_cfg {default_cfg}')
    print(f'noartwork {noartwork}')
    print('*'*20)
    
    waveshare = constants.waveshare
    plugins = constants.plugins
    layouts_file = constants.layouts
    default_clock = constants.clock
    
    # formatters for errors
    keyError_fmt = 'KeyError: config file section [{}] is missing value: {}'
    configError_fmt = 'see section [{}] in config file {}'
    valError_fmt = ''
#     cfg_file_fmt = f''
    
    ######### CONFIGURATION #########
    
    ##### SETUP LOGGING #####
    logging.config.fileConfig(logging_cfg)
    
    ##### PARSE COMMAND LINE ARGUMENTS #####
    options = configuration.Options(sys.argv)
    # add options to the configuration object
    # for options that override the configuration file options, add in the format: 
    # dest=[[ConfigFileSectionName]]__[[Option_Name]]
    # specifying arguments with #ignore_none=True and ignore_false=True will exclude
    # these arguments entirely from the nested dictionary making it easier to merge
    # the command line arguments into the configuration file without adding unwanted options
    
    # set logging level
    options.add_argument('-l', '--log-level', ignore_none=True, metavar='LOG_LEVEL',
                         type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                         dest='main__log_level', 
                         help='set logging level: DEBUG, INFO, WARNING, ERROR')

    # alternative user_cfg file
    options.add_argument('-c', '--config', type=str, required=False, metavar='/path/to/cfg/file.cfg',
                         dest='user_cfg', ignore_none=True, default=user_cfg,
                         help=f'use the specified configuration file; default user config: {user_cfg}')
    
    # list servers - 
    options.add_argument('-s', '--list-servers', action='store_true', 
                         dest='list_servers',
                         default=False, 
                         help='list servers and any players found on local network and exit')
    
    options.add_argument('-p', '--player-id', type=str, required=False, metavar='playerName',
                         default=False, dest='lms_server__player_id', ignore_none=True,
                         help='set the name of the player to monitor')
    
    options.add_argument('-V', '--version', action='store_true', required=False,
                         dest='version', default=False, 
                         help='display version nubmer and exit')

    
    # parse the command line options-
    options.parse_args()
#     return(options)
    ##### ACTION COMMANDLINE ARGS #####
    if options.options.version:
        print(f'{version}')
        do_exit(0)
    
    # use an alternative user configuration file
    if 'user_cfg' in options.opts_dict:
        user_cfg = options.opts_dict['user_cfg']
        logging.info(f'using configuration file: {user_cfg}')
    
    # read the configuration right most values overwrite left values
    # system overwrites default; user overwrites system
    config_file = configuration.ConfigFile(config_files=[default_cfg, system_cfg, user_cfg])    
    
    # merge the configuration files and the command line options
    config = configuration.merge_dict(config_file.config_dict, options.nested_opts_dict)
    
    # set root log level now
    ll = config['main']['log_level']
    logging.root.setLevel(ll)
    logging.debug(f'log level: {ll}')

    
    ##### OBJECTS #####
    # Signal handler for gracefully handling HUP/KILL signals
    sigHandler = signalhandler.SignalHandler()
    
    # LMS Query rate limiter wrapper - allow max of `max_calls` per `period` (seconds)
    lmsQuery_ratelimit = RateLimiter(max_calls=1, period=3)
    # create lms query object
    try:
        lms = lmsquery.LMSQuery(**config['lms_server'])
        
        if options.options.list_servers:
            scan_servers()
            do_exit(0)
        
        if not lms.player_id:
            raise ValueError(keyError_fmt.format('lms_server', 'player_id'))
            
    except TypeError as e:
        logging.fatal(configError_fmt.format('lms_server', user_cfg))
        logging.fatal(f'Error: {e}')
        do_exit(0)

    except ValueError as e:
        logging.fatal(e)
        logging.fatal(f'locate server and player information with:\n$ {app_name} --list-servers')
        do_exit(0)

    

    # setup EPD Display
    try:
        epd = importlib.import_module('.'.join([waveshare, config['layouts']['display']]))
        
    except (KeyError) as e:
        logging.fatal(keyError_fmt.format('layouts', 'display'))
        logging.fatal(configError_fmt.format('layouts', user_cfg))
        logging.fatal(e)
        do_exit(0)
    except (ModuleNotFoundError) as e:
        logging.fatal(keyError_fmt.format('layouts', 'display'))
        logging.fatal(configError_fmt.format('layouts', user_cfg))
        logging.fatal(e)
        do_exit(0)
    
    # import additonal modules
    try:
        clock = importlib.import_module('.'.join([plugins, config['modules']['clock']]))
    except KeyError as e:
            logging.error(keyError_fmt.format('modules', 'clock'))
    except (ModuleNotFoundError) as e:
        mod = config['modules']['clock']
        logging.error(keyError_fmt.format('modules', 'clock'))
        logging.error(f'could not load module: {mod} due to error: {e}')
        logging.error('falling back to default')
        try:
            clock = importlib.import_module(default_clock)
        except ModuleNotFoundError as e:
            logging.fatal(f'failed to load module with error: {e}')
            
    try:
        clock_update = int(config['modules']['clock_update'])
    except KeyError as e:
        logging.error(keyError_fmt.format('modules', 'clock_update'))
        logging.error(f'setting clock update to 60 seconds')
        clock_update = 60
    
    # setup layouts for displaying content
    try:
        layouts = importlib.import_module(layouts_file)
        playing_layout_format = getattr(layouts, config['layouts']['now_playing'])
        stopped_layout_format = getattr(layouts, config['layouts']['stopped'])
        splash_layout_format = getattr(layouts, config['layouts']['splash'])
    except (ModuleNotFoundError) as e:
        logging.fatal(f'could not import layouts file: {layouts_file}')
        logging.fatal(e)
        do_exit(0)
    except (KeyError, AttributeError) as e:
        logging.fatal(keyError_fmt.format('layouts', e.args[0]))
        logging.fatal(configError_fmt.format('layouts', user_cfg))
        logging.fatal(e)
        do_exit(0)
    
    # set resolution for screen
    resolution = [epd.EPD_HEIGHT, epd.EPD_WIDTH]
    # sort to put longest dimension first for landscape layout
    resolution.sort(reverse=True)
    
    playing_layout = epdlib.Layout(layout=playing_layout_format, resolution=resolution)
    
    
    splash_layout = epdlib.Layout(layout=splash_layout_format, resolution=resolution)
    splash_layout.update_contents({'app_name': app_name,
                                   'version': version,
                                   'url': url})
    
    playing_layout = epdlib.Layout(layout=playing_layout_format, resolution=resolution)
    stopped_layout = epdlib.Layout(layout=stopped_layout_format, resolution=resolution)
    
    # scren objects for managing writing to screen
    screen = epdlib.Screen()
    screen.epd = epd.EPD()
    screen.initEPD()
    
    
    ########## EXECUTION ##########
    # Show splash screen
    logging.debug(f'starting up with this configuration: {config}')
    if config['main']['splash_screen']:
        # push the images in the layout to the screen
        screen.elements = splash_layout.blocks.values()
        # concat all the individual images
        screen.concat()
        # write the image
        screen.writeEPD()
    
    # refresh the screen when true
    refresh = False
    # maximum amount of time to wait before refreshing display
    refresh_delay = 60
    
    # vars for managing track ID, mode, album art
    nowplaying_id = None
    nowplaying_mode = None
    artwork_cache = cacheart.CacheArt(app_long_name)
    
    # loop forever waiting for a kill/interrupt signal
    try:
        while not sigHandler.kill_now:
            # clear the lms server response 
            response = None
        
            # use the ratelimiter to throttle requests
            with lmsQuery_ratelimit:
                try:
                    logging.debug(f'querying lms server for status of player: {lms.player_id}')
                    response = lms.now_playing()
                except requests.exceptions.ConnectionError as e:
                    logging.warning(f'Server could not find active player_id: {lms.player_id}')
                    logging.warning('is the specified player active?')
                    response = {'title': f'Could not connect player: {lms.player_id}',
                                'album': 'is player_id valid?',
                                'artist': 'see logs for more info',
                                'id': 'NONE', 'mode': 'ERROR - SEE LOGS'}
                    nowplaying_mode = response['mode']

                except KeyError as e:
                    logging.info(f'No playlist is active on player_id: {lms.player_id}')
                    response = {'title': 'No music is queued', 'id': 'NONE', 'mode': 'No Playlist'}
                    nowplaying_mode = response['mode']
                    
            if response:
                resp_id = response['id']
                resp_mode = response['mode']
                if resp_id != nowplaying_id or resp_mode != nowplaying_mode:
                    logging.info(f'track/mode change to: {resp_mode}')
                    nowplaying_id = resp_id
                    nowplaying_mode = resp_mode
                    
                    # attempt to fetch artwork 
                    try:
                        artwork = artwork_cache.cache_artwork(response['artwork_url'], response['album_id'])
                    except KeyError as e:
                        logging.warning('no artwork available')
                        artwork = None
                    if not artwork:
                        artwork = noartwork
                    # add the path to the downloaded album art into the response
                    response['coverart'] = str(artwork)
                             
                    # update the layout with the values in the response
                    playing_layout.update_contents(response)
                    
                    # refresh contains the current layout
                    refresh = playing_layout
                    #set delay to 60 seconds
                    refresh_delay = 60
                else:
                    refresh = False
                
            if nowplaying_mode != "play" and screen.update.last_updated > refresh_delay:
                logging.debug(f'next update will be in {refresh_delay} seconds')
                logging.info('music appears to be paused, switching to clock display')
                update = clock.get_time()
                update['mode'] = nowplaying_mode
                stopped_layout.update_contents(update)
                refresh = stopped_layout
                refresh_delay = clock_update


        
            # only refresh if needed
            if refresh:
                logging.debug('refreshing display')
                screen.initEPD()
                screen.elements=refresh.blocks.values()
                screen.concat()
                screen.writeEPD()   
                # set refresh to False; this will be updated as needed
                refresh = False                            
                    
    
            sleep(0.5)
    finally:
        print('Caught exit signal - exiting')
        logging.info('cleaning up and wiping screen')
        artwork_cache.clear_cache()
        
        screen.initEPD()
        screen.clearEPD()
        
    return config




# In[ ]:


# TESTING = True
if __name__ == '__main__':
    o = main()




# In[ ]:





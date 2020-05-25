"""
 Author: LiveTvTuga

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
 """

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime
from resources.lib.common_variables import *
from resources.lib.directory import *
from resources.lib.youtubewrapper import *
from resources.lib.watched import * 

fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.LiveTube', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.LiveTube/resources/art', ''))

def CATEGORIES():
	
        addDir('[COLOR red]This addon is brought to you by Live Tv Tuga[/COLOR]','',1,art + 'LiveTvTuga.png')
        addDir('Live Coronavirus Pandemic','PLDsxHUqbx2tUf63KHYVK4zNhJNuWmOnG7',1,art + 'Live.png')
        addDir('Coronavirus Covid-19', 'PLDsxHUqbx2tUBxViwgHycT5M24vC5y8zm', 1, art + 'Live.png')
        addDir('Music R&B','PLDsxHUqbx2tWCHkHwnNKksTlsU5eRmQfw',1,art + 'Live.png')
        addDir('Music Mix','PLDsxHUqbx2tUbFD0WciTcodw93fTCCBkl',1,art + 'Live.png')
        addDir('Channel Live Tv Tuga','PLDsxHUqbx2tUU7LETiU72uKAJdIwp2jJL',1,art + 'Live.png')
        addDir('Webcam Live Streams','PLDsxHUqbx2tX5ugQIW6Pv3V7Rt2i6nBiA',1,art + 'Live.png')
        addDir('Soggy Dollar Bar','PLDsxHUqbx2tUT7JYbfxpZbtI5VOpSbHnI',1,art + 'Live.png')
        addDir('Nature Relaxation','PLDsxHUqbx2tVaj653fd88_oC0tTn4lPwc',1,art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('', '', 1, art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','', 1, art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','',1,art + 'Live.png')
        addDir('','', 1, art + 'Live.png')
		
        
 
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


params=get_params()
url=None
name=None
mode=None
iconimage=None
page = None
token = None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except:
	try: 
		mode=params["mode"]
	except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: token=urllib.unquote_plus(params["token"])
except: pass
try: page=int(params["page"])
except: page = 1

print ("Mode: "+str(mode))
print ("URL: "+str(url))
print ("Name: "+str(name))
print ("iconimage: "+str(iconimage))
print ("Page: "+str(page))
print ("Token: "+str(token))

		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        return_youtubevideos(name,url,token,page)

elif mode==5: 
        play_youtube_video(url)

elif mode==6:
        mark_as_watched(url)

elif mode==7:
        removed_watched(url)

elif mode==8:
        add_to_bookmarks(url)

elif mode==9:
        remove_from_bookmarks(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

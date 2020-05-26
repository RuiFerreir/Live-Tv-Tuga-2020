#   script.amaintenance
#   Copyright (C) 2016  LiveTvTuga
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.



import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import os
import plugintools
addon_id = 'script.amaintenance'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID = 'script.amaintenance'
AddonTitle = "LiveTvTuga Maintenance"
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
iconf = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'iconf.png'))
thumbnailPath = xbmc.translatePath('special://thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'script.amaintenance')
mediaPath = os.path.join(addonPath, 'media')
databasePath = xbmc.translatePath('special://database')
THUMBS    =  xbmc.translatePath(os.path.join('special://home/userdata/Thumbnails',''))
#######################################################################
#                          CLASSES
#######################################################################

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi



def mainMenu():

    addItem('Clear Cache','url', 1,icon)
    addItem('Delete Thumbnails', 'url', 2,icon)
    addItem('Purge Packages', 'url', 3,icon)
    addItem('FRESHSTART', 'url', 6,iconf)
    
#######################################################################
#						Add to menus
#######################################################################

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok


def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	
def addItem(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def killxbmc():
    choice = xbmcgui.Dialog().yesno('FForce Close Kodi', 'You are about to close Kodi', 'Would you like to continue?',
                                    nolabel='No, Cancel', yeslabel='Yes, Close')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx':  # OSX
        print "############   try osx force close  #################"
        try:
            os.system('killall -9 XBMC')
        except:
            pass
        try:
            os.system('killall -9 Kodi')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",
                  '')
    elif myplatform == 'linux':  # Linux
        print "############   try linux force close  #################"
        try:
            os.system('killall XBMC')
        except:
            pass
        try:
            os.system('killall Kodi')
        except:
            pass
        try:
            os.system('killall -9 xbmc.bin')
        except:
            pass
        try:
            os.system('killall -9 kodi.bin')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",
                  '')
    elif myplatform == 'android':  # Android
        print "############   try android force close  #################"
        try:
            os.system('adb shell am force-stop org.xbmc.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc.xbmc')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",  "Pulling the power cable is the simplest method to force close, or exit via Task Manager.")
    elif myplatform == 'windows':  # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.", "Use task manager and NOT ALT+F4")
    else:  # ATV
        print "############   try atv force close  #################"
        try:
            os.system('killall AppleTV')
        except:
            pass
        print "############   try raspbmc force close  #################"  # OSMC / Raspbmc
        try:
            os.system('sudo initctl stop kodi')
        except:
            pass
        try:
            os.system('sudo initctl stop xbmc')
        except:
            pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.", "iOS detected. Press and hold both the Sleep/Wake and Home button for at least 10 seconds, until you see the Apple logo.")

##########################
###DETERMINE PLATFORM#####
##########################

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
		
############################
#########FRESH START########
############################

def FRESHSTART(params):
    plugintools.log("freshstart.main_list " + repr(params));
    yes_pressed = plugintools.message_yes_no(AddonTitle, "Do you want to remove everything.")
    if yes_pressed:
        addonPath = xbmcaddon.Addon(id=AddonID).getAddonInfo('path')
        addonPath = xbmc.translatePath(addonPath)
        xbmcPath = os.path.join(addonPath, "..", "..")
        xbmcPath = os.path.abspath(xbmcPath)
        plugintools.log("freshstart.main_list xbmcPath=" + xbmcPath)
        failed = False
        try:
            for root, dirs, files in os.walk(xbmcPath, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                        
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass	
    killxbmc()
	
#######################################################################
#						Parses Choice
#######################################################################
      
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

#######################################################################
#						Work Functions
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
					"special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries


def clearCache():

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            if (f == "xbmc.log" or f == "xbmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f == "xbmc.log" or f == "xbmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    dialog = xbmcgui.Dialog()
                    if dialog.yesno("Manager",str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
                

    dialog = xbmcgui.Dialog()
    dialog.ok("Maintenance", "Done Clearing Cache files")
    
    
def deleteThumbnails():
    print '############################################################       DELETING THUMBNAILS             ###############################################################'
    packages_thumbnails = xbmc.translatePath(os.path.join('special://masterprofile/Thumbnails/', ''))
    try:
        for root, dirs, files in os.walk(packages_thumbnails):
            file_count = 0
            file_count += len(dirs)

            # Count files and give option to delete
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Apagar diretorio de Thumbnails", str(file_count) + " diretorios encontrados.",
                                "Deseja excluir?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Tools LiveTvTuga", "Os pacotes apagados")
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok("Tools LiveTvTuga", "Desculpe, tente novamente remover arquivos de pacote")			
    killxbmc()				
	
        
def purgePackages():

    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    if dialog.yesno("Delete Package Cache Files", "%d packages found."%file_count, "Delete Them?"):  
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                dialog = xbmcgui.Dialog()
                dialog.ok("Maintenance", "Deleting Packages all done")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Maintenance", "No Packages to Purge")
               
#######################################################################
#                       Support
#######################################################################


params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

if mode==None or url==None or len(url)<1:
        mainMenu()
       
elif mode==1:
		clearCache()
        
elif mode==2:
        deleteThumbnails()

elif mode==3:
		purgePackages()

elif mode == 6:
    FRESHSTART(params)		

xbmcplugin.endOfDirectory(int(sys.argv[1]))


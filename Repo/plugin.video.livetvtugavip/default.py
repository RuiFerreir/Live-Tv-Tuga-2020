 #############Imports#############
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,base64,os,re,unicodedata,requests,time,string,sys,urllib,urllib2,json,urlparse,datetime,zipfile,shutil
from resources.modules import client,control,tools,shortlinks
from resources.ivue import ivuesetup
from datetime import date
import xml.etree.ElementTree as ElementTree
#################################

#############Defined Strings#############
addon_id     = 'plugin.video.livetvtugavip'
selfAddon    = xbmcaddon.Addon(id=addon_id)
icon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
search2      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icons/search.png'))
system       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icons/system.png'))
airing       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icons/airing.png'))
guide         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icons/guide.png'))
extra         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icons/extra.png'))
catch         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icons/catch.png'))
vodtv         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icons/vodtv.png'))


username     = control.setting('Username')
password     = control.setting('Password')

host         = 'http://livegopanel.club'
port         = '8080'

live_url     = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(host,port,username,password)
vod_url      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
panel_api    = '%s:%s/panel_api.php?username=%s&password=%s'%(host,port,username,password)
play_url     = '%s:%s/live/%s/%s/'%(host,port,username,password)


Guide = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.livetvtugavip/resources/catchup', 'guide.xml'))
GuideLoc = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.livetvtugavip/resources/catchup', 'g'))

advanced_settings           =  xbmc.translatePath('special://home/addons/'+addon_id+'/resources/advanced_settings')
advanced_settings_target    =  xbmc.translatePath(os.path.join('special://home/userdata','advancedsettings.xml'))
#########################################


def start():
	if username=="":
		user = userpopup()
		passw= passpopup()
		control.setSetting('Username',user)
		control.setSetting('Password',passw)
		xbmc.executebuiltin('Container.Refresh')
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,user,passw)
		auth = tools.OPEN_URL(auth)
		if auth == "":
			line1 = "[COLOR red]Detalhes de Login Incorretos![/COLOR]"
			line2 = "Por favor, reinsira" 
			line3 = "Para comprar uma conta:[COLOR yellowgreen] info@livetvtuga.ch[/COLOR]" 
			xbmcgui.Dialog().ok('[COLOR lime]Live Tv Tuga RF [/COLOR]', line1, line2, line3)
			start()
		else:
			line1 = "[COLOR lime]Login bem sucedido![/COLOR]"
			line2 = "Bem-vindo ao [COLOR lime]VIP Live Tv Tuga [/COLOR]" 
			line3 = ('[COLOR lime]%s[/COLOR]'%user)
			xbmcgui.Dialog().ok('[COLOR lime]VIP Live Tv Tuga  [COLOR white]IPTV[/COLOR]', line1, line2, line3)
			#tvguidesetup()
			#addonsettings('ADS2','')
			xbmc.executebuiltin('Container.Refresh')
			home()
	else:
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
		auth = tools.OPEN_URL(auth)
		if not auth=="":
			tools.addDir('[COLOR lime]Account Information[/COLOR]','url',6,icon,fanart,'')
			tools.addDir('[COLOR lime]Live TV[/COLOR]','live',1,airing,fanart,'')
			#tools.addDir('Catchup TV','url',12,catch,fanart,'')
			#if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') or xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
				#tools.addDir('TV Guide','pvr',7,guide,fanart,'')
			tools.addDir('[COLOR lime]VOD[/COLOR]','vod',3,vodtv,fanart,'')
			tools.addDir('[COLOR lime]Search[/COLOR]','url',5,search2,fanart,'')
			tools.addDir('[COLOR lime]Settings[/COLOR]','url',8,system,fanart,'')
			tools.addDir('[COLOR lime]Extras[/COLOR]','url',16,extra,fanart,'')
def home():
	tools.addDir('[COLOR lime]Account Information[/COLOR]','url',6,icon,fanart,'')
	tools.addDir('[COLOR lime]Live TV[/COLOR]','live',1,airing,fanart,'')
	#tools.addDir('Catchup TV','url',12,catch,fanart,'')
	#if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		#tools.addDir('TV Guide','pvr',7,guide,fanart,'')
	tools.addDir('[COLOR lime]VOD[/COLOR]','vod',3,vodtv,fanart,'')
	tools.addDir('[COLOR lime]Search[/COLOR]','',5,search2,fanart,'')
	tools.addDir('[COLOR lime]Settings[/COLOR]','url',8,system,fanart,'')
	tools.addDir('[COLOR lime]Extras[/COLOR]','url',16,extra,fanart,'')
		
def livecategory(url):
	
	open = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
		tools.addDir(name,url1,2,icon,fanart,'')
		
def Livelist(url):
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
		
	
def vod(url):
	if url =="vod":
		open = tools.OPEN_URL(vod_url)
	else:
		open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		if '<playlist_url>' in open:
			name = tools.regex_from_to(a,'<title>','</title>')
			url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
			tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,3,icon,fanart,'')
		else:
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				try:
					name = tools.regex_from_to(a,'<title>','</title>')
					name = base64.b64decode(name)
					thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
					url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
					desc = tools.regex_from_to(a,'<description>','</description>')
					desc = base64.b64decode(desc)
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					cast = tools.regex_from_to(desc,'CAST:','\n')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					tools.addDirMeta(str(name).replace('[COLOR lime].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
				except:pass
				xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			else:
				name = tools.regex_from_to(a,'<title>','</title>')
				name = base64.b64decode(name)
				thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
				url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
				desc = tools.regex_from_to(a,'<description>','</description>')
				tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
		
		
##########################################
def catchup():
    loginurl   = "http://livegopanel.club:8080/get.php?username=" + username + "&password=" + password + "&type=m3u_plus&output=ts"
    try:
        connection = urllib2.urlopen(loginurl)
        print connection.getcode()
        connection.close()
        #playlist found, user active & login correct, proceed to addon
        pass
        
    except urllib2.HTTPError, e:
        print e.getcode()
        dialog.ok("[COLOR white]Expired Account[/COLOR]",'[COLOR white]You cannot use this service with an expired account[/COLOR]',' ','[COLOR white]Please check your account information[/COLOR]')
        sys.exit(1)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    url = "%s:%s/xmltv.php?username=%s&password=%s"%(host,port,username,password)
    DownloaderClass(url,GuideLoc + "uide.xml")
    
    f = open(Guide, 'r+')
    input = open(Guide).read().decode('UTF-8')
    output = unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')
    f.write(output)
    f.truncate()
    f.close()
    listcatchup()
		
def listcatchup():
	open = tools.OPEN_URL(panel_api)
	all  = tools.regex_get_all(open,'{"num','direct')
	for a in all:
		if '"tv_archive":1' in a:
			name = tools.regex_from_to(a,'"epg_channel_id":"','"')
			thumb= tools.regex_from_to(a,'"stream_icon":"','"').replace('\/','/')
			id   = tools.regex_from_to(a,'stream_id":"','"')
			tools.addDir(name.replace('ENT:','[COLOR lime]ENT:[/COLOR]').replace('DOC:','[COLOR lime]DOC:[/COLOR]').replace('MOV:','[COLOR lime]MOV:[/COLOR]').replace('SSS:','[COLOR lime]SSS[/COLOR]').replace('BTS:','[COLOR lime]BTS:[/COLOR]').replace('TEST','[COLOR lime]TEST[/COLOR]').replace('Install','[COLOR lime]Install[/COLOR]').replace('24/7','[COLOR lime]24/7[/COLOR]').replace('INT:','[COLOR lime]INT:[/COLOR]').replace('DE:','[COLOR lime]DE:[/COLOR]').replace('FR:','[COLOR lime]FR:[/COLOR]').replace('PL:','[COLOR lime]PL:[/COLOR]').replace('AR:','[COLOR lime]AR:[/COLOR]').replace('LIVE:','[COLOR lime]LIVE:[/COLOR]').replace('ES:','[COLOR lime]ES:[/COLOR]').replace('IN:','[COLOR lime]IN:[/COLOR]').replace('PK:','[COLOR lime]PK:[/COLOR]'),'url',13,thumb,fanart,id)
			

def tvarchive(name,description):
    name = str(name.replace('[COLOR lime]ENT:[/COLOR]','ENT:').replace('[COLOR lime]DOC:[/COLOR]','DOC:').replace('[COLOR lime]MOV:[/COLOR]','MOV').replace('[COLOR lime]SSSS[/COLOR]','SSS:').replace('[COLOR lime]BTS:[/COLOR]','BTS:').replace('[COLOR lime]INT:[/COLOR]','INT:').replace('[COLOR lime]DE:[/COLOR]','DE:').replace('[COLOR lime]FR:[/COLOR]','FR:').replace('[COLOR lime]PL:[/COLOR]','PL:').replace('[COLOR lime]AR:[/COLOR]','AR:').replace('[COLOR lime]LIVE:[/COLOR]','LIVE:').replace('[COLOR lime]ES:[/COLOR]','ES:').replace('[COLOR lime]IN:[/COLOR]','IN:').replace('[COLOR lime]PK:[/COLOR]','PK'))
    filename = open(Guide)
    tree = ElementTree.parse(filename)
    pony = "apples"
    import datetime as dt
    from datetime import time
    date3 = datetime.datetime.now() - datetime.timedelta(days=5)
    date = str(date3)
    now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
    programmes = tree.findall("programme")
    for programme in programmes:
        if name in programme.attrib.get('channel'):
            showtime = programme.attrib.get('start')
            head, sep, tail = showtime.partition(' +')
            date = str(date).replace('-','').replace(':','').replace(' ','')
            year, month, day = showtime.partition('2017')
            kanalinimi = programme.find('title').text + showtime
            day = day[:-6]
            if head > date:
                if head < now:
                    head2 = head
                    head2 = head2[:4] + '/' + head2[4:]
                    head = head[:4] + '-' + head[4:]
                    head2 = head2[:7] + '/' + head2[7:]
                    head = head[:7] + '-' + head[7:]
                    head2 = head2[:10] + ' - ' + head2[10:]
                    head = head[:10] + ':' + head[10:]
                    head2 = head2[:15] + ':' + head2[15:]
                    head = head[:13] + '-' + head[13:]
                    head2 = head2[:-2]
                    head = head[:-2]
                    poo1 = ("%s:%s/streaming/timeshift.php?username=%s&password=%s&stream=%s&start=")%(host,port,username,password,description)
                    pony = poo1 + str(head) + "&duration=240"
                    head2 = '[COLOR lime]%s - [/COLOR]'%head2 
                    kanalinimi = str(head2)+ programme.find('title').text
                    desc  = programme.find('desc').text
                    tools.addDir(kanalinimi,pony,4,icon,fanart,desc)
                    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
	
					
def DownloaderClass(url, dest):
    dp = xbmcgui.DialogProgress()
    dp.create('Fetching latest Catch Up',"Fetching latest Catch Up...",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[COLOR white]%.02f MB of less than 5MB[/COLOR]' % (currently_downloaded)
            e = '[COLOR white]Speed:  %.02f Mb/s ' % mbps_speed  + '[/COLOR]'
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled():
            dialog = xbmcgui.Dialog()
            dialog.ok("Live Tv Tuga RFIPTV2", 'The download was cancelled.')
				
            sys.exit()
            dp.close()
#####################################################################

#def tvguide():
	if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') and xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
		dialog = xbmcgui.Dialog().select('Select a TV Guide', ['PVR TV Guide','iVue TV Guide'])
		if dialog==0:
			xbmc.executebuiltin('ActivateWindow(TVGuide)')
		elif dialog==1:
			xbmc.executebuiltin('RunAddon(script.ivueguide)')
	elif not xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') and xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
		xbmc.executebuiltin('RunAddon(script.ivueguide)')
	elif xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') and not xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
		xbmc.executebuiltin('ActivateWindow(TVGuide)')
def stream_video(url):
	url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
	liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(url))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def searchdialog():
	search = control.inputDialog(heading='Search Live Tv Tuga RF :')
	if search=="":
		return
	else:
		return search

	
def search():
	if mode==3:
		return False
	text = searchdialog()
	if not text:
		xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
		return
	xbmc.log(str(text))
	open = tools.OPEN_URL(panel_api)
	all_chans = tools.regex_get_all(open,'{"num":','epg')
	for a in all_chans:
		name = tools.regex_from_to(a,'name":"','"').replace('\/','/')
		url  = tools.regex_from_to(a,'"stream_id":"','"')
		thumb= tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
		if text in name.lower():
			tools.addDir(name,play_url+url+'.ts',4,thumb,fanart,'')
		elif text not in name.lower() and text in name:
			tools.addDir(name,play_url+url+'.ts',4,thumb,fanart,'')

	
def settingsmenu():
	tools.addDir('Edit Advanced Settings','ADS',10,icon,fanart,'')
	tools.addDir('Log Out','LO',10,icon,fanart,'')
	

def addonsettings(url,description):
	if   url =="CC":
		tools.clear_cache()
	elif url =="AS":
		xbmc.executebuiltin('Addon.OpenSettings(%s)'%addon_id)
	elif url =="ADS":
		dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
		elif dialog==5:
			advancedsettings('remove')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Advanced Settings Removed')
	elif url =="ADS2":
		dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','Nvidia Shield'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok('Live Tv Tuga RF', 'Set Advanced Settings')
	
	elif url =="ST":
		xbmc.executebuiltin('Runscript("special://home/addons/plugin.video.livetvtugavip/resources/modules/speedtest.py")')
	elif url =="META":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('meta','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('meta','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="LO":
		xbmcaddon.Addon().setSetting('Username','')
		xbmcaddon.Addon().setSetting('Password','')
		xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
		xbmc.executebuiltin('Container.Refresh')
	elif url =="UPDATE":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('update','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('update','true')
			xbmc.executebuiltin('Container.Refresh')
	
		
def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(advanced_settings_target)
	
	try:
		read = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(read)
		f.close()
	except:
		pass
		
	
#def pvrsetup():
	correctPVR()
	return
		
		
def asettings():
	choice = xbmcgui.Dialog().yesno('Live Tv Tuga RF', 'Please Select The RAM Size of Your Device', yeslabel='Less than 1GB RAM', nolabel='More than 1GB RAM')
	if choice:
		lessthan()
	else:
		morethan()
	

def morethan():
		file = open(os.path.join(advanced_settings, 'morethan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()

		
def lessthan():
		file = open(os.path.join(advanced_settings, 'lessthan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()
		
		
def userpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Username')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False

		
def passpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Password')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False
		
		
def accountinfo():
	open = tools.OPEN_URL(panel_api)
	try:
		username   = tools.regex_from_to(open,'"username":"','"')
		password   = tools.regex_from_to(open,'"password":"','"')
		status     = tools.regex_from_to(open,'"status":"','"')
		connects   = tools.regex_from_to(open,'"max_connections":"','"')
		active     = tools.regex_from_to(open,'"active_cons":"','"')
		expiry     = tools.regex_from_to(open,'"exp_date":"','"')
		expiry     = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
		expreg     = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
		for day,month,year in expreg:
			month     = tools.MonthNumToName(month)
			year      = re.sub(' -.*?$','',year)
			expiry    = month+' '+day+' - '+year
			ip        = tools.getlocalip()
			extip     = tools.getexternalip()
			tools.addDir('[COLOR lime]Username :[/COLOR] '+username,'','',icon,fanart,'')
			tools.addDir('[COLOR lime]Password :[/COLOR] '+password,'','',icon,fanart,'')
			tools.addDir('[COLOR lime]Expiry Date:[/COLOR] '+expiry,'','',icon,fanart,'')
			tools.addDir('[COLOR lime]Account Status :[/COLOR] %s'%status,'','',icon,fanart,'')
			tools.addDir('[COLOR lime]Current Connections:[/COLOR] '+ active,'','',icon,fanart,'')
			tools.addDir('[COLOR lime]Allowed Connections:[/COLOR] '+connects,'','',icon,fanart,'')
			tools.addDir('[COLOR lime]Local IP Address:[/COLOR] '+ip,'','',icon,fanart,'')
			tools.addDir('[COLOR lime]External IP Address:[/COLOR] '+extip,'','',icon,fanart,'')
	except:pass
		
	
def correctPVR():

	addon = xbmcaddon.Addon('plugin.video.livetvtugavip')
	username_text = addon.getSetting(id='Username')
	password_text = addon.getSetting(id='Password')
	jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
	IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
	nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
	loginurl   = "http://livegopanel.club:8080/get.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"
	EPGurl     = "http://livegopanel.club:8080/xmltv.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"

	xbmc.executeJSONRPC(jsonSetPVR)
	xbmc.executeJSONRPC(IPTVon)
	xbmc.executeJSONRPC(nulldemo)
	
	moist = xbmcaddon.Addon('pvr.iptvsimple')
	moist.setSetting(id='m3uUrl', value=loginurl)
	moist.setSetting(id='epgUrl', value=EPGurl)
	moist.setSetting(id='m3uCache', value="false")
	moist.setSetting(id='epgCache', value="false")
	xbmc.executebuiltin("Container.Refresh")
	
#def ivueint():
	ivuesetup.iVueInt()
	
def tvguidesetup():
		dialog = xbmcgui.Dialog().yesno('Live Tv Tuga RF','Would You like us to Setup the TV Guide for You?')
		if dialog:
			dialog = xbmcgui.Dialog().select('Select a TV Guide to Setup', ['iVue TV Guide','PVR TV Guide','Both'])
			if dialog==0:
				ivueint()
				xbmcgui.Dialog().ok('Live Tv Tuga RF', 'iVue Integration Complete')
			elif dialog==1:
				pvrsetup()
				xbmcgui.Dialog().ok('Live Tv Tuga RF', 'PVR Integration Complete')
			elif dialog==2:
				pvrsetup()
				ivueint()
				xbmcgui.Dialog().ok('Live Tv Tuga RF', 'PVR & iVue Integration Complete')

def num2day(num):
	if num =="0":
		day = 'monday'
	elif num=="1":
		day = 'tuesday'
	elif num=="2":
		day = 'wednesday'
	elif num=="3":
		day = 'thursday'
	elif num=="4":
		day = 'friday'
	elif num=="5":
		day = 'saturday'
	elif num=="6":
		day = 'sunday'
	return day
	
def extras():
	tools.addDir('Create a Short M3U & EPG URL','url',17,icon,fanart,'')
	#tools.addDir('Integrate With TV Guide','tv',10,icon,fanart,'')
	tools.addDir('Run a Speed Test','ST',10,icon,fanart,'')
	tools.addDir('Clear Cache','CC',10,icon,fanart,'')

params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass

if mode==None or url==None or len(url)<1:
	start()

elif mode==1:
	livecategory(url)
	
elif mode==2:
	Livelist(url)
	
elif mode==3:
	vod(url)
	
elif mode==4:
	stream_video(url)
	
elif mode==5:
	search()
	
elif mode==6:
	accountinfo()
	
elif mode==7:
	tvguide()
	
elif mode==8:
	settingsmenu()
	
elif mode==9:
	xbmc.executebuiltin('ActivateWindow(busydialog)')
	tools.Trailer().play(url) 
	xbmc.executebuiltin('Dialog.Close(busydialog)')
	
elif mode==10:
	addonsettings(url,description)
	
#elif mode==11:
	pvrsetup()
	
elif mode==12:
	catchup()

elif mode==13:
	tvarchive(name,description)
	
elif mode==14:
	listcatchup2()
	
#elif mode==15:
	ivueint()
	
elif mode==16:
	extras()
	
elif mode==17:
	shortlinks.Get()

elif mode==18:
	footballguidesearch(description)
	
elif mode==19:
	get()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
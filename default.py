#############################################################################
#############################################################################
import common
from common import *
from common import (addon_id,addon_name,addon_path)

#############################################################################
#############################################################################
ContTypes={'.txt':"text/plain",'.js':"application/javascript",'.css':"text/css",'.swf':"application/x-shockwave-flash",'.mkv':"video/x-matroska",'.wmv':"video/x-ms-wmv",'.apk':"application/vnd.android.package-archive",'.pdf':"application/pdf",'.atom':"application/atom+xml",'.xml':"application/atom+xml",'.avi':"video/x-msvideo",'.torrent':"application/x-bittorrent",'.sh':"application/x-sh",'.bz':"application/x-bzip",'.bz2':"application/x-bzip2",'.res':"application/x-dtbresource+xml",'.flv':"video/x-flv",'.f4v':"video/x-f4v",'.gtar':"application/x-gtar",'.gif':"image/gif",'.h261':"video/h261",'.h262':"video/h262",'.h263':"video/h263",'.ico':"image/x-icon",'.jar':"application/java-archive",'.class':"application/java-vm",'.jnlp':"application/x-java-jnlp-file",'.ser':"application/java-serialized-object",'.java':"text/x-java-source,java",'.json':"application/json",'.jpeg':"image/jpeg",'.jpg':"image/jpeg",'.m3u':"audio/x-mpegurl",'.exe':"application/x-msdownload",'.cab':"application/vnd.ms-cab-compressed",'.doc':"application/msword",'.mid':"audio/midi",'.midi':"audio/midi",'.mpga':"audio/mpeg",'.mpeg':"video/mpeg",'.mxu':"video/vnd.mpegurl",'.mp4a':"audio/mp4",'.mp4':"video/mp4",'.ogg':"video/ogg",'.oga':"audio/ogg",'.ogx':"application/ogg",'.otf':"application/x-font-otf",'.pcx':"image/x-pcx",'.psd':"image/vnd.adobe.photoshop",'.pic':"image/x-pict",'.chat':"application/x-chat",'.png':"image/png",'.ppm':"image/x-portable-pixmap",'.ram':"audio/x-pn-realaudio",'.rar':"application/x-rar-compressed",'.rmp':"audio/x-pn-realaudio-plugin",'.rm':"application/vnd.rn-realmedia",'.svg':"image/svg+xml",'.au':"audio/basic",'.tiff':"image/tiff",'.tar':"application/x-tar",'.ttf':"application/x-font-ttf",'.vcd':"application/x-cdlink",'.hlp':"application/winhlp",'.xpi':"application/x-xpinstall",'.zip':"application/zip"}
PAGELIST=['addoninfo','current_list','dir','img','lastscreenshot','m','m_dreamcatcher','m_playing','m_stopserver','page','stopserver','test','txt','webplay','whats_playing','form','hello','say','list','favourites']


#############################################################################
#############################################################################
import os,SimpleHTTPServer,SocketServer,socket,cgi,urlparse
try: PORT=int(getSet("port",'8025'))
except: PORT=8025
try: ADDRESS=getSet("address",'')
except: ADDRESS=''
if len(str(ADDRESS)) > 0: debob(ADDRESS)
MIME_TYPES=mimetypes.types_map
MIME_TYPES[".ogg"] = u"audio/ogg"

try: HTMLBODY=FileOPEN(addonPath2('body.html'))
except: HTMLBODY=''
try: HTMLBODYidx=FileOPEN(addonPath2('index.html'))
except: HTMLBODYidx=''
stext='<!--SPLIT-->'
if stext in HTMLBODY:
    HTMLBODYs=HTMLBODY.split(stext)[0]
    HTMLBODYe=HTMLBODY.split(stext)[1]
else:
    HTMLBODYs='<html><body style="background-color:#333333;margin:0px 0px 0px 0px;padding:0px 0px 0px 0px;width:100%;" color="red" forecolor="red" textcolor="red" link="red" link="red">'
    HTMLBODYe='</body></html>'
#try: 
#    print socket.gethostname()
#    print socket.gethostbyaddr(socket.gethostname())
#except: pass
HOSTNAME=socket.gethostbyaddr(socket.gethostname())[0]
class webDispatcher(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def req_stopserver(self):
        self.whead(200)
        self.w_body_s()
        self.w('Attempting shutdown of the server.')
        self.w_body_e()
        try: 
        	httpd.shutdown()
        except Exception,e: debob(e)
        except: pass
    def req_m_stopserver(self):
        self.whead(200)
        self.w('Attempting shutdown<br> of the server.')
        try: 
        	httpd.shutdown()
        except Exception,e: debob(e)
        except: pass
    def req_hello(self):
        self.whead()
        self.w_body_s()
        self.w('Hello. Go to <a href="/form">the form<a>.')
        self.w_body_e()
    def req_form(self):
        self.whead()
        self.w_body_s()
        self.w('<form action="/say" method="GET">Enter a phrase:<input name="phrase" type="text" size="60"><input type="submit" value="Say it !"></form>')
        self.w_body_e()
    def req_say(self,phrase):
        self.whead()
        self.w_body_s()
        for item in phrase:       
            self.w("I say %s<br>"%item)
        self.w_body_e()
    def req_list(self):
        def aLink(u,m):
            return '[<a href="%s" style="background-color:grey;text-color:red;"> %s </a>]'%(u,m)
        self.whead()
        self.w_body_s()
        s =''
        s+='<hr></hr>\n'
        s+='<a href="/hello">Hello</a><br>\n'
        #s+='<hr></hr>\n'
        #s+='[<a href="/"></a>]<br>\n'
        #s+='[<a href="/"></a>]<br>\n'
        #s+='\n'
        #s+='\n'
        #s+='\n'
        #s+='</body>\n</html>\n'
        self.w(s)
        self.w_body_e()
    def req_addoninfo(self,**kwargs):
        s=''
        self.webparams={}
        self.webparamnames=['cmd','test','url','path','core','resolver','body']
        for a in self.webparamnames:
            self.webparams[a]=''
        for (k,v) in kwargs.items():
            for a in self.webparamnames:
                if k.lower()==a:
                    for item in v:
                        self.webparams[a]=item
        if not self.webparams['cmd'].lower() in ['author','description','disclaimer','name','id','stars','summary','type','version']: 
            self.webparams['cmd']=''
        try:
            if len(self.webparams['cmd']) > 0:
                self.whead(200,"text/plain")
                s+=addon.getAddonInfo(self.webparams['cmd'])
                self.w(s)
        except: pass
        self.whead(404,"text/plain")
    def req_txt(self,**kwargs):
        #self.whead()
        self.webparams={}
        self.webparamnames=['cmd','test','url','path','core','resolver','body']
        for a in self.webparamnames:
            self.webparams[a]=''
        for (k,v) in kwargs.items():
            for a in self.webparamnames:
                if k.lower()==a:
                    for item in v:
                        self.webparams[a]=item
        if len(self.webparams['path'])==0:
            if isFile(tP(art('index.txt'))):
                self.webparams['path']='index.txt'
        if len(self.webparams['path']) > 0:
            if self.webparams['path'].endswith('.log') or self.webparams['path'].endswith('.txt'):
                if self.webparams['path'].lower().startswith('special://logpath'):
                    u=tP(self.webparams['path'])
                else:
                    u=tP(art(self.webparams['path']))
                if isFile(u):
                    self.whead(200,"text/plain")
                    html=FileOPEN(u)
                    self.w(html)
                    return
        self.whead(404)
    def req_lastscreenshot(self):
        self.webparams={}
        self.webparams['path']=''
        c='special://screenshots/screenshot%s.png'
        d=tP(c%'000'); i=0
        while isFile(d):
            self.webparams['path']=''+d; i=i+1
            e=str(i)
            if len(e) < 3: e='0'+e
            if len(e) < 3: e='0'+e
            d=tP(c%e)
        if len(self.webparams['path']) > 0:
            u=tP(self.webparams['path'])
        if len(u) > 0:
            if isFile(u)==False:
                u=tP(art(self.webparams['path']))
            if isFile(u):
                extension = os.path.splitext(u)[1].lower()
                mimetype = "application/octet-stream"
                if extension in MIME_TYPES: mimetype = MIME_TYPES[extension]
                self.send_response(200)
                self.send_header('Content-Type',mimetype)
                self.send_header('Content-Length',str(os.path.getsize(u)))
                self.end_headers()
                self.wfile.write(open(u,"rb").read())
    def req_img(self,**kwargs):
        #self.whead()
        self.webparams={}
        self.webparamnames=['cmd','test','url','path','core','resolver']
        for a in self.webparamnames:
            self.webparams[a]=''
        for (k,v) in kwargs.items():
            for a in self.webparamnames:
                if k.lower()==a:
                    for item in v:
                        self.webparams[a]=item
        if self.webparams['path']=='icon':
            u=tP(addonIcon)
        elif self.webparams['path']=='fanart':
            u=tP(addonFanart)
        elif self.webparams['path']=='favicon.ico':
            if isFile(tP(art('favicon.ico'))):
                u=tP(art('favicon.ico'))
            elif isFile(tP(art('favicon.png'))):
                u=tP(art('favicon.png'))
            else:
                u=''
        elif len(self.webparams['path']) > 0:
            if self.webparams['path'].startswith('skin://'):
                u=self.webparams['path']
                u=u.replace('skin://','')
                if xbmc.skinHasImage(u):
                    gSD=xbmc.getSkinDir()
                    if os.path.exists(tP(os.path.join('special://home','addons',gSD,'media'))):
                        u=tP(os.path.join('special://home','addons',gSD,'media',u))
                    elif os.path.exists(tP(os.path.join('special://xbmc','addons',gSD,'media'))):
                        u=tP(os.path.join('special://xbmc','addons',gSD,'media',u))
            u=tP(self.webparams['path'])
        if len(u) > 0:
          if u.endswith('.png') or u.endswith('.jpg') or u.endswith('.gif') or u.endswith('.ico') or u.endswith('.bmp') or u.endswith('/'):
            if isFile(u)==False:
                u=tP(art(self.webparams['path']))
            if isFile(u):
                extension=os.path.splitext(u)[1].lower()
                mimetype="application/octet-stream"
                if extension in MIME_TYPES: mimetype=MIME_TYPES[extension]
                elif u.endswith('/'): mimetype='image/png'
                self.send_response(200)
                self.send_header('Content-Type',mimetype)
                self.send_header('Content-Length',str(os.path.getsize(u)))
                self.end_headers()
                self.wfile.write(open(u,"rb").read())
                return
        self.whead(404)
    def req_m(self): #mobile
        u=tP(art('mobile.html'))
        if isFile(u):
            html=FileOPEN(u)
            self.whead(200); self.w(html); return
        self.whead(404)
    def req_m_dreamcatcher(self): #mobile
        Plyr=xbmc.Player(GetPlayerCore())
        if Plyr.isPlaying():
            try: u=Plyr.getPlayingFile()
            except: u=''
            self.whead(200); 
            self.w('<b>Currently Playing: </b><br> <a class="ainbody" href="%s">%s</a><br>\n'%(u,u))
            if len(u) > 0:
                DoRP('plugin://plugin.program.dreamcatcher/?mode=Record')
                self.w('<b>Attempting to activate: </b><br> %s<br>\n'%('Dreamcatcher'))
        self.whead(404); 
    def req_whats_playing(self): #mobile
#        elif self.webparams['cmd']=='mobile_whatsplaying':
            Plyr=xbmc.Player(GetPlayerCore())
            if Plyr.isPlaying():
                try: u=Plyr.getPlayingFile()
                except: u=''
                uTC=str(Plyr.getTime())
                uTT=str(Plyr.getTotalTime())
            else:
                u=''
                uTC=''
                uTT=''
            u2=tP(art('whatsplaying.html'))
            if len(u) > 0:
                    u3=urllib.quote_plus(u)
            else:
                    u3=u
            htmlWebPlayer=FileOPEN(u2)
            u2tag='%%FILE%%'
            u3tag='%%QPFILE%%'
            u4tag='%%TIMECUR%%'
            u5tag='%%TIMETOTAL%%'
            if u2tag in htmlWebPlayer:
                htmlWebPlayer=htmlWebPlayer.replace(u2tag,u)
            if u3tag in htmlWebPlayer:
                htmlWebPlayer=htmlWebPlayer.replace(u3tag,u3)
            if u4tag in htmlWebPlayer:
                htmlWebPlayer=htmlWebPlayer.replace(u4tag,uTC)
            if u5tag in htmlWebPlayer:
                htmlWebPlayer=htmlWebPlayer.replace(u5tag,uTT)
            self.whead(200); 
            self.w_body_s()
            self.w(htmlWebPlayer)
            self.w_body_e()
    def req_m_playing(self): #mobile
#        elif self.webparams['cmd']=='mobile_whatsplaying':
            #self.w_body_s()
            Plyr=xbmc.Player(GetPlayerCore())
            if Plyr.isPlaying():
                try: u=Plyr.getPlayingFile()
                except: u=''
                uTC=str(Plyr.getTime())
                uTT=str(Plyr.getTotalTime())
            else:
                u=''
                uTC=''
                uTT=''
            u2=tP(art('mobile_whatsplaying.html'))
            if len(u) > 0:
                    u3=urllib.quote_plus(u)
            else:
                    u3=u
            htmlWebPlayer=FileOPEN(u2)
            u2tag='%%FILE%%'
            u3tag='%%QPFILE%%'
            u4tag='%%TIMECUR%%'
            u5tag='%%TIMETOTAL%%'
            if u2tag in htmlWebPlayer:
                htmlWebPlayer=htmlWebPlayer.replace(u2tag,u)
            if u3tag in htmlWebPlayer:
                htmlWebPlayer=htmlWebPlayer.replace(u3tag,u3)
            if u4tag in htmlWebPlayer:
                htmlWebPlayer=htmlWebPlayer.replace(u4tag,uTC)
            if u5tag in htmlWebPlayer:
                htmlWebPlayer=htmlWebPlayer.replace(u5tag,uTT)
            self.whead(200); 
            self.w(htmlWebPlayer)
    def req_current_list(self,**kwargs):
        self.webparams={}; DoneHead=False; DoTheList=True; 
        self.webparamnames=['cmd','test','url','path','core','resolver','body']; 
        for a in self.webparamnames:
            self.webparams[a]=''
        for (k,v) in kwargs.items():
            for a in self.webparamnames:
                if k.lower()==a:
                    for item in v:
                        self.webparams[a]=item
        cmdL=self.webparams['cmd'].lower()
        if (cmdL=='action') and (len(self.webparams['path']) > 0):
            try: DoA(self.webparams['path'])
            except: pass
        if (cmdL=='activatewindow') and (len(self.webparams['path']) > 0):
            try: DoAW(self.webparams['path'])
            except: pass
        if (cmdL=='runplugin') and (len(self.webparams['path']) > 0):
            try: DoRP(self.webparams['path'])
            except: pass
        if (cmdL=='runscript') and (len(self.webparams['path']) > 0):
            try: DoRS(self.webparams['path'])
            except: pass
        if len(cmdL) > 0:
            xbmc.sleep(3000)
        try: sysCurWin=str(xbmc.getInfoLabel("System.CurrentWindow"))
        except: sysCurWin=''
        sysCurWin2=''
        if   sysCurWin=='':
            #try: sysCurCtrl=str(xbmc.getInfoLabel("System.System.CurrentControl"))
            #except: sysCurCtrl=''
            #debob(['sysCurCtrl',type(sysCurCtrl).__name__])
            #debob(sysCurCtrl)
            #sysCurCtrlType=type(sysCurCtrl).__name__
            #if sysCurCtrlType=="str":
            #    self.whead(200); 
            #    self.w(str(sysCurCtrl.getLabel()))
            #dwin=xbmcgui.Window(xbmcgui.getCurrentWindowId())
            #self.whead(200); DoneHead=True; 
            #u2=tP(art('current_list_home.html'))
            #htmlWebPlayer=FileOPEN(u2)
            #self.w(htmlWebPlayer)
            #DoTheList=False; 
            sysCurWin2='Home'
            pass
            #return
        if (len(sysCurWin) > 0) and (sysCurWin in ['Settings','Reset','Web Browser','Settings - Videos','Settings - Music','Settings - Pictures','Settings - Weather','Add-on browser','File browser','Done','Settings - Network','Settings - System','System Information','Select dialogue','Favourites']):
            sysCurWin2='Home'
        if sysCurWin=='Fullscreen video': ## Player controls hidden.
            self.whead(200); DoneHead=True; 
            html=FileOPEN(tP(art('current_list_body.html')))
            html+=FileOPEN(tP(art('current_list_playing.html')))
            self.w(html)
            DoTheList=False; 
            return
        elif sysCurWin=='Fullscreen OSD': ## Player controls visible.
            self.whead(200); DoneHead=True; 
            html=FileOPEN(tP(art('current_list_body.html')))
            html+=FileOPEN(tP(art('current_list_playing.html')))
            self.w(html)
            DoTheList=False; 
            return
        elif sysCurWin=='Weather': ## Weather
            self.whead(200); DoneHead=True; 
            html=FileOPEN(tP(art('current_list_body.html')))
            html+=FileOPEN(tP(art('current_list_weather.html')))
            self.w(html)
            DoTheList=False; 
            return
        elif (sysCurWin=='Home') or (sysCurWin2=='Home'): ## Home Screen
            self.whead(200); DoneHead=True; 
            html=FileOPEN(tP(art('current_list_body.html')))
            html+=FileOPEN(tP(art('current_list_home.html')))
            self.w(html)
            DoTheList=False; 
            return
        elif (sysCurWin=='Videos') or (sysCurWin=='Pictures') or (sysCurWin=='Music') or (sysCurWin=='Videos') or (sysCurWin=='Programs'):
            DoTheList=True; 
        #else:
        #    self.whead(200); DoneHead=True; 
        #    html=FileOPEN(tP(art('current_list_body.html')))
        #    html+=FileOPEN(tP(art('current_list_home.html')))
        #    self.w(html)
        #    DoTheList=False; 
        #    return
        ##
        #elif sysCurWin=='':
        #    pass
        #elif sysCurWin=='':
        #    pass
        #try:
        #if len(self.webparamnames) > 0:
        if DoTheList==True:
            #win=xbmcgui.Window(xbmcgui.getCurrentWindowId())
            #curctl=win.getFocus()
            #debob("Type of curctl is "+type(curctl).__name__)
#          if str(type(curctl).__name__)=="ControlList":
            #SizeOfList=int(curctl.size())
            SizeOfList=int(xbmc.getInfoLabel('Container.NumItems'))
            SizeOfListPages=int(xbmc.getInfoLabel('Container.NumPages'))
            SizeOfListCurrentPage=int(xbmc.getInfoLabel('Container.CurrentPage'))
            debob(['SizeOfList',SizeOfList,SizeOfListPages])
            #cursel=curctl.getSelectedItem()
            #debob("Type of cursel is "+type(cursel).__name__)
            #curselItemLabel=cursel.getLabel()
            #curselItemPos=cursel.getSelectedPosition()
            #debob([curselItemPos,curselItemLabel])
            if DoneHead==False:
                self.whead(200); 
                html=FileOPEN(tP(art('current_list_body.html')))
                self.w(html)
                #self.w('<h3>[[ %s ]]</h3><br>'%(sysCurWin))
            if int(SizeOfList) > 0:
              UPDOWN=''
              if SizeOfListCurrentPage < SizeOfListPages:
                  UPDOWN+='<a class="" href="/current_list?cmd=action&path=%s"><img src="/img?path=%s"></a>'%('PageDown','btn2/scroll-down-round-focus-2.png')
              else:
                  UPDOWN+='<img src="/img?path=%s">'%('btn2/scroll-down-round-2.png')
              if SizeOfListCurrentPage > 1:
                  UPDOWN+='<a class="" href="/current_list?cmd=action&path=%s"><img src="/img?path=%s"></a>'%('PageUp','btn2/scroll-up-round-focus-2.png')
              else:
                  UPDOWN+='<img src="/img?path=%s">'%('btn2/scroll-up-round-2.png')
              UPDOWN+='&nbsp;<b>(%s) Items - Page (%s/%s)</b><br>'%(str(SizeOfList),str(SizeOfListCurrentPage),str(SizeOfListPages))
              UPDOWN+='<br><ul>'
              self.w(UPDOWN)
              for i in range(0,int(SizeOfList)+1):
                try:
                  DoTheRight=True
                  ##L0=curctl.getListItem(i)
                  ##debob("Type of L0 is "+type(L0).__name__)
                  #try: print ['Path',str(xbmc.getInfoLabel('Container.ListItem(%s).Path'%(str(i))))]
                  #except: pass
                  #try: print ['FileNameAndPath',str(xbmc.getInfoLabel('Container.ListItem(%s).FileNameAndPath'%(str(i))))]
                  #except: pass
                  #try: print ['FileName',str(xbmc.getInfoLabel('Container.ListItem(%s).FileName'%(str(i))))]
                  #except: pass
                  #try: print ['FolderName',str(xbmc.getInfoLabel('Container.ListItem(%s).FolderName'%(str(i))))]
                  #except: pass
                  #try: print ['FileExtension',str(xbmc.getInfoLabel('Container.ListItem(%s).FileExtension'%(str(i))))]
                  #except: pass
                  ##try: print ['',str(xbmc.getInfoLabel('Container.ListItem(%s).Path'%(str(i))))]
                  ##except: pass
                  ##try: print ['',str(xbmc.getInfoLabel('Container.ListItem(%s).Path'%(str(i))))]
                  ##except: pass
                  try: 
                  	L1=str(xbmc.getInfoLabel('Container.ListItem(%s).FileNameAndPath'%(str(i))))
                  	#L1=str(xbmc.getInfoLabel('Container.ListItem(%s).FileName'%(str(i))))
                  	#L1=str(xbmc.getInfoLabel('Container.ListItem(%s).Path'%(str(i))))
                  	#L1=str(xbmc.getInfoLabel('Container.ListItem(%s).FolderName'%(str(i))))
                  	#L1=str(xbmc.getInfoLabel('Container.ListItem(%s).FileExtension'%(str(i))))
                  	## "Start Server" = plugin://plugin.a.web.server/?mode=start
                  	## "Stop Server" = plugin://plugin.a.web.server/?mode=end
                  	## ".." = addons://sources/executable/
                  	## "Blackjack" = script://plugin.game.blackjack/
                  	## "" = plugin://plugin.video.example/?mode=SubMenu&section=movies
                  except: L1=''
                  try: 
                  	L2=str(xbmc.getInfoLabel('Container.ListItem(%s).Label'%(str(i))))
                  	## ".." seems to show up last instead of first.
                  except: L2='UNKNOWN'
                  for a in ['[B]','[/B]','[I]','[/I]','[/COLOR]']:
                      L2=L2.replace(a,'')
                  if '[COLOR ' in L2:
                      try: L2r=re.compile('(\[COLOR [A-Za-z0-9]+\])').findall(L2)
                      except: L2r=[]
                      if len(L2r) > 0:
                        for a in L2r:
                          L2=L2.replace(a,'')
                  #debob([i,L2,L1])
                  try: 
                  	L3=FixServerArt(str(xbmc.getInfoLabel('Container.ListItem(%s).Thumb'%(str(i)))))
                  except: L3=''
                  #if (L3=='') and (L2==".."): L3='/img?path=defaultfolderback.png'
                  #print ['L1',L1]
                  #if (L2==".."):
                  #    L3=FixServerArt(tP(art('btn2/icon_back.png')))
                  if (L2==".."):
                      L4='/current_list?cmd=%s&path=%s'%('action','back')
                      L3=FixServerArt(tP(art('btn2/icon_back.png')))
                  elif (L1=="add"):
                      L4=''; L3=''; 
                      DoTheRight=False
                  elif (L1.lower()=='none') or (L1=='') or (qP(L1)=='None'):
                      #L4='/current_list?cmd=%s&path=%s'%('activatewindow','Home')
                      L4='/current_list?cmd=%s&path=%s'%('action','back')
                      L3=FixServerArt(tP(art('btn2/icon_back.png')))
                  elif L1.startswith('plugin://'):
                      #L4='/current_list?cmd=%s&path=%s'%('runplugin',qP(L1))
                      L4='/current_list?cmd=%s&path=%s'%('activatewindow',sysCurWin+','+qP(L1))
                  elif L1.startswith('addons://'):
                      #L4='/current_list?cmd=%s&path=%s'%('addons',qP(L1))
                      L4='/current_list?cmd=%s&path=%s'%('activatewindow',sysCurWin+','+qP(L1))
                  elif L1.startswith('script://'):
                      #L4='/current_list?cmd=%s&path=%s'%('runscript',qP(L1))
                      L4='/current_list?cmd=%s&path=%s'%('activatewindow',sysCurWin+','+qP(L1))
                  else:
                      if (L2==".."): # and (len(L1)==0):
                          #L4='/current_list?cmd=%s&path=%s'%('activatewindow','Home')
                          L4='/current_list?cmd=%s&path=%s'%('action','back')
                          #L3=FixServerArt(tP(art('btn2/icon_back.png')))
                      else:
                          L4='/current_list?cmd=%s&path=%s'%('activatewindow',sysCurWin+','+qP(L1))
                  #print ['L4',L4]
                  if (i < 4) or (L2==".."): debob([i,L2,L4,L1])
                  if DoTheRight==True:
                      self.w('<li><a class="ScreenListItem" href="%s"><img class="ScreenListItem" src="%s">&nbsp;&nbsp;%s</a></li>\n'%(L4,L3,L2))
                except: pass
              self.w('</ul>')
            return
            ##
        #except: pass
        self.whead(404); 
    def req_dir(self,**kwargs):
        self.webparams={}
        self.webparamnames=['cmd','test','url','path','core','resolver','body']
        for a in self.webparamnames:
            self.webparams[a]=''
        for (k,v) in kwargs.items():
            for a in self.webparamnames:
                if k.lower()==a:
                    for item in v:
                        self.webparams[a]=item
        if len(self.webparams['path'])==0:
            self.webparams['path']=tP(os.path.join(addonPath,'art'))
        if len(self.webparams['path']) > 0:
                pathLower=self.webparams['path'].lower()
                if pathLower.startswith('\\') or pathLower.startswith('/') or (':' in pathLower):
                    u=tP(self.webparams['path'])
                else:
                    u=tP(art(self.webparams['path']))
                if (os.path.exists(u)) and (os.path.isdir(u)):
                    dirs=os.listdir(u)
                    LinkExample='<a class="dir%s" href="%s">%s</a><br>'
                    self.whead(200); 
                    if self.webparams['body'].lower()=='1':
                        self.w_body_s(); 
                    else:
                        self.w('<body style="background-color:#333333;">'); 
                    self.w('<style>a {color:orange;text-decoration:none;}</style>'); 
                    f='..'; #u2=os.path.join(u,f)
                    try: u2=os.path.split(u)[0]
                    except: u2=''
                    if (len(u2) > 0) and (not u==u2):
                        if os.path.isdir(u2):
                            self.w(LinkExample%('Path','/dir?body='+self.webparams['body']+'&path='+u2,f))
                    for f in dirs:
                        u2=os.path.join(u,f)
                        if os.path.isdir(u2):
                            self.w(LinkExample%('Path','/dir?body='+self.webparams['body']+'&path='+u2,f))
                        elif os.path.isfile(u2):
                            if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.gif') or f.endswith('.ico') or f.endswith('.bmp'):
                                self.w(LinkExample%('File','/img?body='+self.webparams['body']+'&path='+u2,f))
                            else:
                                self.w(LinkExample%('File','/page?body='+self.webparams['body']+'&path='+u2,f))
                    if self.webparams['body'].lower()=='1':
                        self.w_body_e(); 
                    return
        self.whead(404); 
    def req_page(self,**kwargs):
        self.webparams={}
        self.webparamnames=['cmd','test','url','path','core','resolver','body']
        for a in self.webparamnames:
            self.webparams[a]=''
        for (k,v) in kwargs.items():
            for a in self.webparamnames:
                if k.lower()==a:
                    for item in v:
                        self.webparams[a]=item
        if len(self.webparams['path'])==0:
            if isFile(tP(art('index.html'))):
                self.webparams['path']='index.html'
        if len(self.webparams['path']) > 0:
            #if self.webparams['path'].endswith('.htm') or self.webparams['path'].endswith('.html') or self.webparams['path'].endswith('.log') or self.webparams['path'].endswith('.txt'):
                #if self.webparams['path'].lower().startswith('special://logpath'):
                #if self.webparams['path'].lower().startswith('special://'):
                pathLower=self.webparams['path'].lower()
                if pathLower.startswith('\\') or pathLower.startswith('/') or (':' in pathLower):
                    u=tP(self.webparams['path'])
                else:
                    u=tP(art(self.webparams['path']))
                if isFile(u):
                    uLL=self.webparams['path'].lower()
                    if uLL.endswith('.htm') or uLL.endswith('.html') or uLL.endswith('.log'):
                        if uLL.endswith('.log'):
                            html=FileOPEN(u)
                            self.whead(200); self.w_body_s(); 
                            self.w('<textarea class="log">'+html.replace('</textarea>','')+'</textarea>'); 
                            self.w_body_e(); return
                        elif str(self.webparams['body'])=='1':
                            html=FileOPEN(u)
                            self.whead(200); self.w_body_s(); 
                            self.w(html); 
                            self.w_body_e(); return
                        else:
                            html=FileOPEN(u)
                            self.whead(200); self.w(html); return
                    for (k,v) in ContTypes.items():
                        if uLL.endswith(k):
                            debob([k,v,self.webparams['path'],u]); 
                            #html=FileOPEN(u)
                            #self.whead(200,str(v),L=len(html)); self.w(html); 
                            ##
                            ff=os.path.split(u)[1]
                            extension=os.path.splitext(u)[1].lower()
                            mimetype="application/octet-stream"
                            if extension in MIME_TYPES: mimetype=MIME_TYPES[extension]
                            elif extention=='mkv': mimetype="video/x-matroska"
                            elif extention=='.mkv': mimetype="video/x-matroska"
                            elif extention=='MKV': mimetype="video/x-matroska"
                            debob([extension,mimetype,ff])
                            self.send_response(200)
                            self.send_header('Content-Type',mimetype)
                            self.send_header('Content-disposition','attachment;filename="%s"'%ff)
                            self.send_header('Content-Length',str(os.path.getsize(u)))
                            self.end_headers()
                            self.wfile.write(open(u,"rb").read())
                            ##
                            return
                    #return
        self.whead(404)
    def req_favourites(self,**kwargs):
        self.webparams={}
        self.webparamnames=['cmd','url','path','core','resolver','body']
        for a in self.webparamnames:
            self.webparams[a]=''
        for (k,v) in kwargs.items():
            for a in self.webparamnames:
                if k.lower()==a:
                    for item in v:
                        self.webparams[a]=item
        ##
        u=tP('special://userdata/favourites.xml')
        if isFile(u):
            html=''; htmlFAV=FileOPEN(u)
            try: r=re.compile('<favourite name="([^"]+)" thumb="([^"]+)">ActivateWindow\(([^\)]+)\)</favourite').findall(htmlFAV)
            except: r=[]
            TEXTOUT='<li><a class="ScreenListItem" href="/current_list?body=%s&cmd=activatewindow&path=%s"><img class="ScreenListItem" src="%s">&nbsp;&nbsp;%s</a></li>\n'
            self.whead(200); 
            if self.webparams['body']=='1':
                self.w_body_s()
            else:
                html+=FileOPEN(tP(art('favourites_header.html')))
            if r:
              if len(r) > 0:
                html+='<ul>\n'
                self.w(html)
                for n,t,a in r:
                    try:
                        n=FixTextCodes(n)
                        a=a.replace('&quot;','') #.replace(',return','')
                        self.w(TEXTOUT%(str(self.webparams['body']),qP(str(a)),str(t),str(n)))
                    except: pass
                self.w('</ul>')
            if self.webparams['body']=='1':
                self.w_body_s()
            return
        #self.whead(404)
    def req_webplay(self,**kwargs):
        self.whead()
        self.webparams={}
        self.webparamnames=['cmd','url','path','core','resolver']
        for a in self.webparamnames:
            self.webparams[a]=''
        for (k,v) in kwargs.items():
            for a in self.webparamnames:
                if k.lower()==a:
                    for item in v:
                        self.webparams[a]=item
        ##
        u=self.webparams['url']
        if len(u) > 0:
            uLL=u.lower()
            if uLL.startswith('special://'):
                u=tP(u)
            elif uLL.startswith('http://') or uLL.startswith('https://') or uLL.startswith('ftp://'):
                pass
            elif (':' in u) or u.startswith('/') or u.startswith('\\'):
                u=tP(u)
            else:
                u=tP(art(u))
        else:
            try: u=xbmc.Player(GetPlayerCore()).getPlayingFile()
            except: u=''
        if (len(u)==0) and (len(self.webparams['url']) > 0): u=self.webparams['url']
        self.w_body_s()
        if len(u) > 0:
            if len(self.webparams['path']) > 0:
                a1=''; a2=''; 
                if isFile(tP(art(self.webparams['path']))):
                    u2=tP(art(self.webparams['path']))
                    htmlWebPlayer=FileOPEN(u2)
                    u2tag='%%FILE%%'
                    u3tag='%%QPFILE%%'
                    try: u3=urllib.quote_plus(u)
                    except: u3=u
                    if u2tag in htmlWebPlayer:
                    #    debob([u2tag,u]); 
                        htmlWebPlayer=htmlWebPlayer.replace(u2tag,u)
                    if u3tag in htmlWebPlayer:
                    #    debob([u3tag,u]); 
                        htmlWebPlayer=htmlWebPlayer.replace(u3tag,u3)
                    self.w(htmlWebPlayer)
        self.w_body_e()
    def req_test(self,**kwargs):
        self.whead()
        self.webparams={}
        self.webparamnames=['cmd','test','url','path','core','resolver']
        #self.w_body_s()
        for a in self.webparamnames:
            self.webparams[a]=''
        for (k,v) in kwargs.items():
            for a in self.webparamnames:
                if k.lower()==a:
                    for item in v:
                        self.webparams[a]=item
        ##
#        print self.webparams
        if   self.webparams['cmd']=='':
            self.w_body_s()
            try: self.HTMLBODYidx=FileOPEN(addonPath2('index.html'))
            except: self.HTMLBODYidx=''
            if len(self.HTMLBODYidx) > 0:
                self.w(self.HTMLBODYidx)
                return
            #if len(HTMLBODYidx) > 0:
            #    self.w(HTMLBODYidx)
            #    return
            pass
        elif self.webparams['cmd']=='screenaction':
            if len(self.webparams['path']) > 0:
                try: DoA(self.webparams['path'])
                except: pass
        elif self.webparams['cmd']=='screenmove':
            if len(self.webparams['path']) > 0:
                try: DoAW(self.webparams['path'])
                except: pass
        elif self.webparams['cmd']=='stopscript':
            if len(self.webparams['path']) > 0:
                try: DoStopScript(self.webparams['path'])
                except: pass
        elif self.webparams['cmd']=='note':
            if len(self.webparams['path']) > 0:
                try: note(addonName,self.webparams['path'])
                except: pass
        elif self.webparams['cmd']=='popupok':
            if len(self.webparams['path']) > 0:
                try: popOK(self.webparams['path'],addonName)
                except: pass
        elif self.webparams['cmd']=='runaddon':
            if len(self.webparams['path']) > 0:
                try: DoRA(self.webparams['path'])
                except: pass
        elif self.webparams['cmd']=='runplugin':
            if len(self.webparams['path']) > 0:
                try: DoRP(self.webparams['path'])
                except: pass
        elif self.webparams['cmd']=='showaddonsettings':
                try: showAddonSettings()
                except: pass
        elif self.webparams['cmd']=='dreamcatcher':
            self.w_body_s()
            Plyr=xbmc.Player(GetPlayerCore())
            try: u=Plyr.getPlayingFile()
            except: u=''
            self.w('<b>Currently Playing: </b> <a class="ainbody" href="%s">%s</a><br>\n'%(u,u))
            if len(u) > 0:
                DoRP('plugin://plugin.program.dreamcatcher/?mode=Record')
            self.w('<b>Attempting to activate: </b> %s<br>\n'%('Dreamcatcher'))
        elif self.webparams['cmd']=='whatsplaying':
            self.w_body_s()
            Plyr=xbmc.Player(GetPlayerCore())
            if Plyr.isPlaying():
                try: u=Plyr.getPlayingFile()
                except: u=''
                uTC=str(Plyr.getTime())
                uTT=str(Plyr.getTotalTime())
            else:
                u=''
                uTC=''
                uTT=''
            self.w('<b>Currently Playing: </b> <a class="ainbody" href="%s">%s</a><br>\n'%(u,u))
            if len(u) > 0:
                try:
                    self.w('<b>%s: </b> %s<br>\n'%('Time Current',uTC))
                    self.w('<b>%s: </b> %s<br>\n'%('Time Total',uTT))
                except: pass
            pass
        elif self.webparams['cmd']=='webplay':
            self.w_body_s()
            try: u=xbmc.Player(GetPlayerCore()).getPlayingFile()
            except: u=''
            s=''
            if len(u) > 0:
                s+=' '
                self.w(s)
        elif   self.webparams['cmd']=='stop':
            self.w_body_s()
            self.w('Stop')
            PlayStop()
            self.w('<b>Attempting to: </b> %s<br>\n'%('stop player'))
        elif self.webparams['cmd']=='pause':
            self.w_body_s()
            self.w('Pause')
            PlayPause()
            self.w('<b>Attempting to: </b> %s<br>\n'%('pause/play player'))
        elif self.webparams['cmd']=='play':
            self.w_body_s()
            u=''; print {'url':self.webparams['url'],'path':self.webparams['path']}
            if (self.webparams['url']=='') and (self.webparams['path']==''):
#                u='https://s3.amazonaws.com/pluscast/vod/wisn/master.m3u8'
#                self.w('<a href="%s" style="color:red;text-color:red">%s</a><br>\n'%(u,'link'))
#                PlayStream(u)
                pass
            elif len(self.webparams['url']) > 0:
                #print self.webparams['url']
                u=self.webparams['url']
                #PlayStream(u)
                #self.w('<a href="%s" style="color:red;text-color:red">%s</a><br>\n'%(u,'link'))
            elif len(self.webparams['path']) > 0:
                #print self.webparams['path']
                u=self.webparams['path']
                #PlayStream(u)
                #self.w('<a href="%s" style="color:red;text-color:red">%s</a><br>\n'%(u,'link'))
            if len(u) > 0:
                self.w('<b>Attempting to play: </b> <a class="ainbody" href="%s">%s</a><br>\n'%(u,u))
                if self.webparams['resolver'].lower()=='resolve':
                    PlayStreamWithResolver(u)
                else:
                    PlayStream(u)
        ##
        if len(self.tempOutput) > 0:
            self.w_body_e()
        else:
            self.w('<body style="background-color:#333333;margin:0px 0px 0px 0px;padding:0px 0px 0px 0px;width:100%;color:#333333;text-color:#333333;"><!-- -- --></body>')
    def w_body_s(self):
        def aLink(u,m):
            return '[ <a href="%s" style="background-color:grey;color:red;text-color:red;"> %s </a> ] '%(u,m)
        if self.HTMLBODYs in self.tempOutput: return
        self.w(self.HTMLBODYs) #(s)
        #except: pass
    def w_body_e(self):
        try: 
            if self.HTMLBODYe in self.tempOutput: return
            self.w(self.HTMLBODYe) #('</body>\n</html>\n')
        except: pass
    def w(self,m):
        #try:
            self.tempOutput+=str(m)
            if '%%' in m:
            #try:
                if '%%XBMCFREEMEM%%' in m:
                    try: m=m.replace('%%XBMCFREEMEM%%',str(xbmc.getFreeMem()))
                    except: m=m.replace('%%XBMCFREEMEM%%','')
                if '%%XBMCIP%%' in m:
                    try: m=m.replace('%%XBMCIP%%',str(xbmc.getIPAddress()))
                    except: m=m.replace('%%XBMCIP%%','')
                if '%%SYSBUILDVER%%' in m:
                    try: m=m.replace('%%SYSBUILDVER%%',str(xbmc.getInfoLabel("System.BuildVersion")))
                    except: m=m.replace('%%SYSBUILDVER%%','')
                if '%%SYSBUILDDATE%%' in m:
                    try: m=m.replace('%%SYSBUILDDATE%%',str(xbmc.getInfoLabel("System.BuildDate")))
                    except: m=m.replace('%%SYSBUILDDATE%%','')
                if '%%SYSSPACEFREE%%' in m:
                    try: m=m.replace('%%SYSSPACEFREE%%',str(xbmc.getInfoLabel("System.FreeSpace")))
                    except: m=m.replace('%%SYSSPACEFREE%%','')
                if '%%SYSSPACEUSED%%' in m:
                    try: m=m.replace('%%SYSSPACEUSED%%',str(xbmc.getInfoLabel("System.UsedSpace")))
                    except: m=m.replace('%%SYSSPACEUSED%%','')
                if '%%SYSSPACETOTAL%%' in m:
                    try: m=m.replace('%%SYSSPACETOTAL%%',str(xbmc.getInfoLabel("System.TotalSpace")))
                    except: m=m.replace('%%SYSSPACETOTAL%%','')
                if '%%SYSSPACEPERCENTUSED%%' in m:
                    try: m=m.replace('%%SYSSPACEPERCENTUSED%%',str(xbmc.getInfoLabel("System.UsedSpacePercent")))
                    except: m=m.replace('%%SYSSPACEPERCENTUSED%%','')
                if '%%SYSSPACEPERCENTFREE%%' in m:
                    try: m=m.replace('%%SYSSPACEPERCENTFREE%%',str(xbmc.getInfoLabel("System.FreeSpacePercent")))
                    except: m=m.replace('%%SYSSPACEPERCENTFREE%%','')
                if '%%SYSFRIENDLYNAME%%' in m:
                    try: m=m.replace('%%SYSFRIENDLYNAME%%',str(xbmc.getInfoLabel("System.FriendlyName")))
                    except: m=m.replace('%%SYSFRIENDLYNAME%%','')
                if '%%SYSFPS%%' in m:
                    try: m=m.replace('%%SYSFPS%%',str(xbmc.getInfoLabel("System.FPS")))
                    except: m=m.replace('%%SYSFPS%%','')
                if '%%SYSFREEMEMORY%%' in m:
                    try: m=m.replace('%%SYSFREEMEMORY%%',str(xbmc.getInfoLabel("System.FreeMemory")))
                    except: m=m.replace('%%SYSFREEMEMORY%%','')
                if '%%SYSMEMORYUSED%%' in m:
                    try: m=m.replace('%%SYSMEMORYUSED%%',str(xbmc.getInfoLabel("System.Memory(used)")))
                    except: m=m.replace('%%SYSMEMORYUSED%%','')
                if '%%SYSMEMORYFREE%%' in m:
                    try: m=m.replace('%%SYSMEMORYFREE%%',str(xbmc.getInfoLabel("System.Memory(free)")))
                    except: m=m.replace('%%SYSMEMORYFREE%%','')
                if '%%SYSMEMORYTOTAL%%' in m:
                    try: m=m.replace('%%SYSMEMORYTOTAL%%',str(xbmc.getInfoLabel("System.Memory(total)")))
                    except: m=m.replace('%%SYSMEMORYTOTAL%%','')
                if '%%SYSMEMORYPERCENTUSED%%' in m:
                    try: m=m.replace('%%SYSMEMORYPERCENTUSED%%',str(xbmc.getInfoLabel("System.Memory(used.percent)")))
                    except: m=m.replace('%%SYSMEMORYPERCENTUSED%%','')
                if '%%SYSMEMORYPERCENTFREE%%' in m:
                    try: m=m.replace('%%SYSMEMORYPERCENTFREE%%',str(xbmc.getInfoLabel("System.Memory(free.percent)")))
                    except: m=m.replace('%%SYSMEMORYPERCENTFREE%%','')
                if '%%SYSSCREENMODE%%' in m:
                    try: m=m.replace('%%SYSSCREENMODE%%',str(xbmc.getInfoLabel("System.ScreenMode")))
                    except: m=m.replace('%%SYSSCREENMODE%%','')
                if '%%SYSSCREENWIDTH%%' in m:
                    try: m=m.replace('%%SYSSCREENWIDTH%%',str(xbmc.getInfoLabel("System.ScreenWidth")))
                    except: m=m.replace('%%SYSSCREENWIDTH%%','')
                if '%%SYSSCREENHEIGHT%%' in m:
                    try: m=m.replace('%%SYSSCREENHEIGHT%%',str(xbmc.getInfoLabel("System.ScreenHeight")))
                    except: m=m.replace('%%SYSSCREENHEIGHT%%','')
                if '%%SYSCURRENTWINDOW%%' in m:
                    try: m=m.replace('%%SYSCURRENTWINDOW%%',str(xbmc.getInfoLabel("System.CurrentWindow")))
                    except: m=m.replace('%%SYSCURRENTWINDOW%%','')
                if '%%SYSCURRENTCONTROL%%' in m:
                    try: m=m.replace('%%SYSCURRENTCONTROL%%',str(xbmc.getInfoLabel("System.CurrentControl")))
                    except: m=m.replace('%%SYSCURRENTCONTROL%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%SYSDVDLABEL%%' in m:
                    try: m=m.replace('%%SYSDVDLABEL%%',str(xbmc.getInfoLabel("System.DVDLabel")))
                    except: m=m.replace('%%SYSDVDLABEL%%','')
                if '%%SYSKERNELVER%%' in m:
                    try: m=m.replace('%%SYSKERNELVER%%',str(xbmc.getInfoLabel("System.KernelVersion")))
                    except: m=m.replace('%%SYSKERNELVER%%','')
                if '%%SYSUPTIME%%' in m:
                    try: m=m.replace('%%SYSUPTIME%%',str(xbmc.getInfoLabel("System.Uptime")))
                    except: m=m.replace('%%SYSUPTIME%%','')
                if '%%SYSSCREENRES%%' in m:
                    try: m=m.replace('%%SYSSCREENRES%%',str(xbmc.getInfoLabel("System.ScreenResolution")))
                    except: m=m.replace('%%SYSSCREENRES%%','')
                if '%%SYSVIDENCODERINFO%%' in m:
                    try: m=m.replace('%%SYSVIDENCODERINFO%%',str(xbmc.getInfoLabel("System.VideoEncoderInfo")))
                    except: m=m.replace('%%SYSVIDENCODERINFO%%','')
                if '%%SYSINTERNETSTATE%%' in m:
                    try: m=m.replace('%%SYSINTERNETSTATE%%',str(xbmc.getInfoLabel("System.InternetState")))
                    except: m=m.replace('%%SYSINTERNETSTATE%%','')
                if '%%SYSLANG%%' in m:
                    try: m=m.replace('%%SYSLANG%%',str(xbmc.getInfoLabel("System.Language")))
                    except: m=m.replace('%%SYSLANG%%','')
                if '%%SYSPROFILENAME%%' in m:
                    try: m=m.replace('%%SYSPROFILENAME%%',str(xbmc.getInfoLabel("System.ProfileName")))
                    except: m=m.replace('%%SYSPROFILENAME%%','')
                if '%%SYSPROFILECOUNT%%' in m:
                    try: m=m.replace('%%SYSPROFILECOUNT%%',str(xbmc.getInfoLabel("System.ProfileCount")))
                    except: m=m.replace('%%SYSPROFILECOUNT%%','')
                if '%%SYSPROFILEAUTOLOGIN%%' in m:
                    try: m=m.replace('%%SYSPROFILEAUTOLOGIN%%',str(xbmc.getInfoLabel("System.ProfileAutoLogin")))
                    except: m=m.replace('%%SYSPROFILEAUTOLOGIN%%','')
                if '%%WEATHERTEMP%%' in m:
                    try: m=m.replace('%%WEATHERTEMP%%',str(xbmc.getInfoLabel("Weather.Temperature")))
                    except: m=m.replace('%%WEATHERTEMP%%','')
                if '%%WEATHERCONDITIONS%%' in m:
                    try: m=m.replace('%%WEATHERCONDITIONS%%',str(xbmc.getInfoLabel("Weather.Conditions")))
                    except: m=m.replace('%%WEATHERCONDITIONS%%','')
                if '%%WEATHERLOCATION%%' in m:
                    try: m=m.replace('%%WEATHERLOCATION%%',str(xbmc.getInfoLabel("Weather.Location")))
                    except: m=m.replace('%%WEATHERLOCATION%%','')
                if '%%WEATHERFANARTCODE%%' in m:
                    try: m=m.replace('%%WEATHERFANARTCODE%%',str(xbmc.getInfoLabel("Weather.fanartcode")))
                    except: m=m.replace('%%WEATHERFANARTCODE%%','')
                if '%%WEATHERPLUGIN%%' in m:
                    try: m=m.replace('%%WEATHERPLUGIN%%',str(xbmc.getInfoLabel("Weather.plugin")))
                    except: m=m.replace('%%WEATHERPLUGIN%%','')
                if '%%SKINCURRENTTHEME%%' in m:
                    try: m=m.replace('%%SKINCURRENTTHEME%%',str(xbmc.getInfoLabel("Skin.CurrentTheme")))
                    except: m=m.replace('%%SKINCURRENTTHEME%%','')
                if '%%SKINCOLOURTHEME%%' in m:
                    try: m=m.replace('%%SKINCOLOURTHEME%%',str(xbmc.getInfoLabel("Skin.CurrentColourTheme")))
                    except: m=m.replace('%%SKINCOLOURTHEME%%','')
                if '%%SKINASPECTRATIO%%' in m:
                    try: m=m.replace('%%SKINASPECTRATIO%%',str(xbmc.getInfoLabel("Skin.AspectRatio")))
                    except: m=m.replace('%%SKINASPECTRATIO%%','')
                if '%%PLAYERDURATION%%' in m:
                    try: m=m.replace('%%PLAYERDURATION%%',str(xbmc.getInfoLabel("Player.Duration")))
                    except: m=m.replace('%%PLAYERDURATION%%','')
                if '%%PLAYERFINISHTIME%%' in m:
                    try: m=m.replace('%%PLAYERFINISHTIME%%',str(xbmc.getInfoLabel("Player.FinishTime")))
                    except: m=m.replace('%%PLAYERFINISHTIME%%','')
                if '%%PLAYERTIME%%' in m:
                    try: m=m.replace('%%PLAYERTIME%%',str(xbmc.getInfoLabel("Player.Time")))
                    except: m=m.replace('%%PLAYERTIME%%','')
                if '%%PLAYERTIMEREMAINING%%' in m:
                    try: m=m.replace('%%PLAYERTIMEREMAINING%%',str(xbmc.getInfoLabel("Player.TimeRemaining")))
                    except: m=m.replace('%%PLAYERTIMEREMAINING%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%PLAYERPROGRESSCACHE%%' in m:
                    try: m=m.replace('%%PLAYERPROGRESSCACHE%%',str(xbmc.getInfoLabel("Player.ProgressCache")))
                    except: m=m.replace('%%PLAYERPROGRESSCACHE%%','')
                if '%%PLAYERFOLDERPATH%%' in m:
                    try: m=m.replace('%%PLAYERFOLDERPATH%%',str(xbmc.getInfoLabel("Player.Folderpath")))
                    except: m=m.replace('%%PLAYERFOLDERPATH%%','')
                if '%%PLAYERFILENAMEANDPATH%%' in m:
                    try: m=m.replace('%%PLAYERFILENAMEANDPATH%%',str(xbmc.getInfoLabel("Player.Filenameandpath")))
                    except: m=m.replace('%%PLAYERFILENAMEANDPATH%%','')
                if '%%PLAYERSTARTTIME%%' in m:
                    try: m=m.replace('%%PLAYERSTARTTIME%%',str(xbmc.getInfoLabel("Player.StartTime")))
                    except: m=m.replace('%%PLAYERSTARTTIME%%','')
                if '%%PLAYERTITLE%%' in m:
                    try: m=m.replace('%%PLAYERTITLE%%',str(xbmc.getInfoLabel("Player.Title")))
                    except: m=m.replace('%%PLAYERTITLE%%','')
                if '%%PLAYERFILENAME%%' in m:
                    try: m=m.replace('%%PLAYERFILENAME%%',str(xbmc.getInfoLabel("Player.Filename")))
                    except: m=m.replace('%%PLAYERFILENAME%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%NETWORK.ISDHCP%%' in m:
                    try: m=m.replace('%%NETWORK.ISDHCP%%',str(xbmc.getInfoLabel("Network.IsDHCP")))
                    except: m=m.replace('%%NETWORK.ISDHCP%%','')
                if '%%NETWORK.IPADDRESS%%' in m:
                    try: m=m.replace('%%NETWORK.IPADDRESS%%',str(xbmc.getInfoLabel("Network.IPAddress")))
                    except: m=m.replace('%%NETWORK.IPADDRESS%%','')
                if '%%NETWORK.LINKSTATE%%' in m:
                    try: m=m.replace('%%NETWORK.LINKSTATE%%',str(xbmc.getInfoLabel("Network.LinkState")))
                    except: m=m.replace('%%NETWORK.LINKSTATE%%','')
                if '%%NETWORK.MACADDRESS%%' in m:
                    try: m=m.replace('%%NETWORK.MACADDRESS%%',str(xbmc.getInfoLabel("Network.MacAddress")))
                    except: m=m.replace('%%NETWORK.MACADDRESS%%','')
                if '%%NETWORK.SUBNETMASK%%' in m:
                    try: m=m.replace('%%NETWORK.SUBNETMASK%%',str(xbmc.getInfoLabel("Network.SubnetMask")))
                    except: m=m.replace('%%NETWORK.SUBNETMASK%%','')
                if '%%NETWORK.GATEWAYADDRESS%%' in m:
                    try: m=m.replace('%%NETWORK.GATEWAYADDRESS%%',str(xbmc.getInfoLabel("Network.GatewayAddress")))
                    except: m=m.replace('%%NETWORK.GATEWAYADDRESS%%','')
                if '%%NETWORK.DNS1ADDRESS%%' in m:
                    try: m=m.replace('%%NETWORK.DNS1ADDRESS%%',str(xbmc.getInfoLabel("Network.DNS1Address")))
                    except: m=m.replace('%%NETWORK.DNS1ADDRESS%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%NETWORK.DNS2ADDRESS%%' in m:
                    try: m=m.replace('%%NETWORK.DNS2ADDRESS%%',str(xbmc.getInfoLabel("Network.DNS2Address")))
                    except: m=m.replace('%%NETWORK.DNS2ADDRESS%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%NETWORK.DHCPADDRESS%%' in m:
                    try: m=m.replace('%%NETWORK.DHCPADDRESS%%',str(xbmc.getInfoLabel("Network.DHCPAddress")))
                    except: m=m.replace('%%NETWORK.DHCPADDRESS%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%VIDEOPLAYER.COVER%%' in m:
                    try: m=m.replace('%%VIDEOPLAYER.COVER%%',FixServerArt(str(xbmc.getInfoLabel("VideoPlayer.Cover"))))
                    except: m=m.replace('%%VIDEOPLAYER.COVER%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%MUSICPLAYER.COVER%%' in m:
                    try: m=m.replace('%%MUSICPLAYER.COVER%%',FixServerArt(str(xbmc.getInfoLabel("MusicPlayer.Cover"))))
                    except: m=m.replace('%%MUSICPLAYER.COVER%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%PLAYER.ART.FANART%%' in m:
                    try: m=m.replace('%%PLAYER.ART.FANART%%',FixServerArt(str(xbmc.getInfoLabel("Player.Art(fanart)"))))
                    except: m=m.replace('%%PLAYER.ART.FANART%%','')
                if '%%PLAYER.ART.THUMB%%' in m:
                    try: m=m.replace('%%PLAYER.ART.THUMB%%',FixServerArt(str(xbmc.getInfoLabel("Player.Art(thumb)"))))
                    except: m=m.replace('%%PLAYER.ART.THUMB%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%PLAYER.ART.POSTER%%' in m:
                    try: m=m.replace('%%PLAYER.ART.POSTER%%',FixServerArt(str(xbmc.getInfoLabel("Player.Art(poster)"))))
                    except: m=m.replace('%%PLAYER.ART.POSTER%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%PLAYER.ART.TVSHOW.POSTER%%' in m:
                    try: m=m.replace('%%PLAYER.ART.TVSHOW.POSTER%%',FixServerArt(str(xbmc.getInfoLabel("Player.Art(tvshow.poster)"))))
                    except: m=m.replace('%%PLAYER.ART.TVSHOW.POSTER%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%PLAYER.ART.TVSHOW.BANNER%%' in m:
                    try: m=m.replace('%%PLAYER.ART.TVSHOW.BANNER%%',FixServerArt(str(xbmc.getInfoLabel("Player.Art(tvshow.banner)"))))
                    except: m=m.replace('%%PLAYER.ART.TVSHOW.BANNER%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%PLAYER.STARRATING%%' in m:
                    try: m=m.replace('%%PLAYER.STARRATING%%',FixServerArt(str(xbmc.getInfoLabel("Player.StarRating"))))
                    except: m=m.replace('%%PLAYER.STARRATING%%','')
                if '%%PLYR.getPlayingFileFixed%%' in m:
                    Plyr=xbmc.Player(GetPlayerCore())
                    if Plyr.isPlaying():
                        try: m=m.replace('%%PLYR.getPlayingFileFixed%%',FixServerFile(str(Plyr.getPlayingFile())))
                        except: m=m.replace('%%PLYR.getPlayingFileFixed%%','')
                    else: m=m.replace('%%PLYR.getPlayingFileFixed%%','')
                if '%%PLYR.getPlayingFile%%' in m:
                    Plyr=xbmc.Player(GetPlayerCore())
                    if Plyr.isPlaying():
                        try: m=m.replace('%%PLYR.getPlayingFile%%',str(Plyr.getPlayingFile()))
                        except: m=m.replace('%%PLYR.getPlayingFile%%','')
                    else: m=m.replace('%%PLYR.getPlayingFile%%','')
                if '%%PLYR.ISPLAYING%%' in m:
                    Plyr=xbmc.Player(GetPlayerCore())
                    try: m=m.replace('%%PLYR.ISPLAYING%%',str(Plyr.isPlaying()))
                    except: m=m.replace('%%PLYR.ISPLAYING%%','')
                if '%%PLYR.getTime%%' in m:
                    Plyr=xbmc.Player(GetPlayerCore())
                    if Plyr.isPlaying():
                        try: m=m.replace('%%PLYR.getTime%%',str(Plyr.getTime()))
                        except: m=m.replace('%%PLYR.getTime%%','')
                    else: m=m.replace('%%PLYR.getTime%%','')
                if '%%PLYR.getTotalTime%%' in m:
                    Plyr=xbmc.Player(GetPlayerCore())
                    if Plyr.isPlaying():
                        try: m=m.replace('%%PLYR.getTotalTime%%',str(Plyr.getTotalTime()))
                        except: m=m.replace('%%PLYR.getTotalTime%%','')
                    else: m=m.replace('%%PLYR.getTotalTime%%','')
                ## \/ ## To Check. ## \/ ##
                if '%%PLAYER.VOLUME%%' in m:
                    try: m=m.replace('%%PLAYER.VOLUME%%',str(xbmc.getInfoLabel("Player.Volume")))
                    except: m=m.replace('%%PLAYER.VOLUME%%','')
                if '%%ADDON.changelog%%' in m:
                    try: m=m.replace('%%ADDON.changelog%%',FileOPEN(str(addon.getAddonInfo('changelog'))))
                    except: m=m.replace('%%ADDON.changelog%%','')
                if '%%ADDON.description%%' in m:
                    try: m=m.replace('%%ADDON.description%%',str(addon.getAddonInfo('description')))
                    except: m=m.replace('%%ADDON.description%%','')
                if '%%ADDON.disclaimer%%' in m:
                    try: m=m.replace('%%ADDON.disclaimer%%',str(addon.getAddonInfo('disclaimer')))
                    except: m=m.replace('%%ADDON.disclaimer%%','')
                if '%%ADDON.fanart%%' in m:
                    try: m=m.replace('%%ADDON.fanart%%',FixServerArt(str(addon.getAddonInfo('fanart'))))
                    except: m=m.replace('%%ADDON.fanart%%','')
                if '%%ADDON.icon%%' in m:
                    try: m=m.replace('%%ADDON.icon%%',FixServerArt(str(addon.getAddonInfo('icon'))))
                    except: m=m.replace('%%ADDON.icon%%','')
                if '%%ADDON.id%%' in m:
                    try: m=m.replace('%%ADDON.id%%',str(addon.getAddonInfo('id')))
                    except: m=m.replace('%%ADDON.id%%','')
                if '%%ADDON.name%%' in m:
                    try: m=m.replace('%%ADDON.name%%',str(addon.getAddonInfo('name')))
                    except: m=m.replace('%%ADDON.name%%','')
                if '%%ADDON.path%%' in m:
                    try: m=m.replace('%%ADDON.path%%',str(addon.getAddonInfo('path')))
                    except: m=m.replace('%%ADDON.path%%','')
                if '%%ADDON.profile%%' in m:
                    try: m=m.replace('%%ADDON.profile%%',str(addon.getAddonInfo('profile')))
                    except: m=m.replace('%%ADDON.profile%%','')
                if '%%ADDON.stars%%' in m:
                    try: m=m.replace('%%ADDON.stars%%',str(addon.getAddonInfo('stars')))
                    except: m=m.replace('%%ADDON.stars%%','')
                if '%%ADDON.summary%%' in m:
                    try: m=m.replace('%%ADDON.summary%%',str(addon.getAddonInfo('summary')))
                    except: m=m.replace('%%ADDON.summary%%','')
                if '%%ADDON.type%%' in m:
                    try: m=m.replace('%%ADDON.type%%',str(addon.getAddonInfo('type')))
                    except: m=m.replace('%%ADDON.type%%','')
                if '%%ADDON.version%%' in m:
                    try: m=m.replace('%%ADDON.version%%',str(addon.getAddonInfo('version')))
                    except: m=m.replace('%%ADDON.version%%','')
                #if '%%SYS%%' in m:
                #    try: m=m.replace('%%SYS%%',str(xbmc.getInfoLabel("System.FriendlyName")))
                #    except: m=m.replace('%%%%','')
                #if '%%SYS%%' in m:
                #    try: m=m.replace('%%SYS%%',str(xbmc.getInfoLabel("System.FriendlyName")))
                #    except: m=m.replace('%%%%','')
                
                
                
                
            #except: pass
            self.wfile.write(m)
        #except: pass
    def whead(self,n=200,t="text/html",L=0):
            self.send_response(int(n))
            self.send_header("Content-Type",str(t))
            if L > 0:
                self.send_header("Content-Length",str(L))
            #self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            #self.send_header("Accept-Charset",'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
            #self.send_header("Accept-Language",'en-us,en;q=0.5')
            #self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
    def ec_400(self,e=''): # URL not called with the proper parameters
        u=tP(art('ec400.html'))
        if isFile(u):
            html=FileOPEN(u)
            self.whead(400)
            try: html=html.replace('%%ERRORMSG%%',str(e))
            except: html=html.replace('%%ERRORMSG%%','')
            self.w(html)
        else:
            self.whead(400)
            self.w("<h1>400 - Bad request</h1><br>")
            try: self.w('<font color="red">"+e+"</font><br>')
            except: pass
    def ec_404(self,e=''):
        u=tP(art('ec404.html'))
        if isFile(u):
            html=FileOPEN(u)
            self.whead(404)
            try: html=html.replace('%%ERRORMSG%%',str(e))
            except: html=html.replace('%%ERRORMSG%%','')
            self.w(html)
        else:
            self.whead(404)
            self.w("<h1>404 - Not found</h1><br>")
            try: self.w('<font color="red">"+e+"</font><br>')
            except: pass
    def ec_500(self,e=''):
        u=tP(art('ec500.html'))
        if isFile(u):
            html=FileOPEN(u)
            self.whead(500)
            try: html=html.replace('%%ERRORMSG%%',str(e))
            except: html=html.replace('%%ERRORMSG%%','')
            self.w(html)
        else:
            self.whead(200)
            self.w("<h1>500 - Internal Server Error (or) Error in page function</h1><br>")
            try: self.w('<font color="red">"+e+"</font><br>')
            except: pass
    def do_GET(self):
        params=cgi.parse_qs(urlparse.urlparse(self.path).query)
        action=urlparse.urlparse(self.path).path[1:]
        if action=="": action="test"
        try: 
            action=action.lower()
            action=action.replace("/","_").replace(".","_").replace(" ","_").replace("-","_").replace("+","_").replace("=","_")
        except: pass
        if action=="favicon.ico": action="img"; params={"path":['favicon.ico']}
        methodname="req_"+action
        #print params
        #print self.address_string()
        #print self.date_time_string() ## Mon, 13 Apr 2015 21:44:05 GMT
        #print self.version_string() ## SimpleHTTP/0.6 Python/2.7.8
        self.tempOutput=''
        ##
        if action in ['img','lastscreenshot','txt','current_list','m']:
            self.HTMLBODYs=HTMLBODYs
            self.HTMLBODYe=HTMLBODYe
            self.HTMLBODY=''
        elif action.startswith('m_'):
            self.HTMLBODYs=HTMLBODYs
            self.HTMLBODYe=HTMLBODYe
            self.HTMLBODY=''
        else:
            try: self.HTMLBODY=FileOPEN(addonPath2('body.html'))
            except: self.HTMLBODY=''
        if stext in self.HTMLBODY:
            self.HTMLBODYs=self.HTMLBODY.split(stext)[0]
            self.HTMLBODYe=self.HTMLBODY.split(stext)[1]
        else:
            self.HTMLBODYs=HTMLBODYs
            self.HTMLBODYe=HTMLBODYe
        if action in PAGELIST:
        #if action==action:
            ##
            
            ## \/ I sometimes use this line while testing what might be going wrong. \/ ##
            #getattr(self,methodname)(**params); return
            
            ##
            try:
                getattr(self,methodname)(**params)
            #except AttributeError,e:
            #    debob(['404','action',action,'params',params])
            #    debob(['404',e])
            #    self.ec_404(e)
            except TypeError,e:  # URL not called with the proper parameters
                debob(['400','action',action,'params',params])
                debob(['400',e])
                self.ec_400(e)
            except Exception,e:
                debob(['500','action',action,'params',params])
                debob(['500',e])
                self.ec_500(e)
        else:
                debob(['404','action',action,'params',params])
                self.ec_404()
#httpd=SocketServer.ThreadingTCPServer(('',PORT),webDispatcher)
#print "Server listening at http://%s:%s"%(HOSTNAME,PORT)
#httpd.serve_forever()
mode=addpr('mode','')
if mode=='end':
    eod()
    html=getURL('http://127.0.0.1:'+str(PORT)+'/stopserver')
    DoA('Back')
elif mode=='start':
    eod()
    try:
        try:
            httpd=SocketServer.ThreadingTCPServer((ADDRESS,PORT),webDispatcher)
        except:
            html=getURL('http://127.0.0.1:'+str(PORT)+'/stopserver')
            xbmc.sleep(2000)
            httpd=SocketServer.ThreadingTCPServer((ADDRESS,PORT),webDispatcher)
        #print "Server listening at http://%s:%s"%(HOSTNAME,PORT)
        print "Server listening at http://%s:%s"%(ADDRESS,PORT)
        print httpd.socket.getsockname()
        httpd.serve_forever()
    except Exception, e:
        try:
            print e
            note("Error",str(e))
        except: pass
    DoA('Back')
else:
    ADDON.add_directory({'mode':'start'},{'title':'Start Server'},fanart=addonFanart,img=addonIcon)
    ADDON.add_directory({'mode':'end'},{'title':'Stop Server'},fanart=addonFanart,img=addonIcon)
    
    eod()
#############################################################################
#############################################################################
#def zModeCheck(mode='',url=''):
#	deb('mode',mode); 
#	if (mode=='') or (mode=='main'): Menu0()
#	elif mode=='BrowsePlayExamples': Browse_PlayExamples()
#	elif mode=='BrowseRegexExample': Browse_RegexExample()
#	elif mode=='BrowsePassText': Browse_PassText(addpr('test'))
#	elif mode=='Play': PlayStream(url)
#	elif mode=='PlayR': PlayStreamWithResolver(url)
#	##
#zModeCheck(addpr('mode'),addpr('url'))
#
#############################################################################
#############################################################################

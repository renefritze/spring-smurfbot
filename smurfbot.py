from colors import *
import string
import datetime
import time 
import feedparser
import math
lastchecked = datetime.datetime.now()
MaxInterval = datetime.timedelta(seconds=600)
filename='smurfs.db'
logfile='gargylog.txt'
channels =['teh','ba','badev']
clans=['[teh]']
users=['[[ITER]]Satirik','[FuN]Lupus','[Mr]E_Rection','maackey','[omfg]XD','[omfg]wtf','[omgf]fu','Autopsy','[PinK]triton']
command='smurfs'
dbsize=0
silent=False
botname=''
mylist=dict()
talkcounter=0
callcounter=0
connected=0
first=1
numtalks=0
numidlehalfhours=0
whosaidit=''
rsstime=0
rssentry=0
gsocket=0
class Main:

	def onconnected(self):
		print "plugin: onconnected()"
		i=1
		cmd_smurfs('','',0)
	def ondisconnected(self):
		#print "plugin: ondisconnected()"
		i=1
	def onmotd(self,content):
		i=1
	def onsaid(self,chan,user,data):
		#print "plugin: onsaid(%s,%s,%s)" % (str(chan),str(user),str(data))
		global numtalks
		numtalks=numtalks+1;
		#print len(api.getusers())
		#print 'some dick talked'
		global silent
		global lastchecked
		global MaxInterval
		global talkcounter
		global callcounter
		global channel
		global channel2
		global channel3
		global clanfilter
		global clanfilter2
		global clanfilter3
		global whosaidit
		
		
		

		#print len(api.getusers())
		#print 'some dick talked'
		
		#print 'talk: %i call: %i time: %s' % (talkcounter,callcounter,datetime.datetime.now().isoformat())
		talkcounter=talkcounter+1

		if chan == 'main':
			if lastchecked + MaxInterval < datetime.datetime.now(): 
				cmd_smurfs('','teh')
				lastchecked = datetime.datetime.now()
		if chan == channel or chan==channel2 or chan==channel3:
			nowchan=channel
			if nowchan!=chan:
				nowchan=channel2
			nowchan=chan
			if data.startswith(command)==True:
				if user.find('[teh]lost')>=0:
					socket.send('SAY '+channel+' Get lost.')
				else:
					if user.find(clanfilter)>=0 or user.find('[[ITER]]Satirik')>=0 or user.find(clanfilter2)>=0 or user.find(clanfilter3)>=0 or user.find(clanfilter4)>=0:
						data= data.split(' ',2)
						if len(data)>1:
							data= data[1].strip()
							silent=False
							#print 'calling smurfs...'
							whosaidit=user
							cmd_smurfs(data,nowchan)
							
						else:
							cmd_smurfs('',nowchan)
					else:
						socket.send('SAY '+nowchan+' Smurf checking is available for '+clanfilter+' and '+clanfilter2 +' and '+clanfilter3+' members only')

	def onsaidex(self,channel,user,message):
		#print "plugin: onsaidex(%s,%s,%s)" % (str(channel),str(user),str(message))
		i=1
	def onsaidprivate(self,user,message):
		#print "plugin: onsaidprivate(%s,%s)" % (str(user),str(message))
		i=1
	def onloggedin(self,socket):
		global channels
		global gsocket
		print "plugin: onloggedin(%s)" % (str(socket))
		#socket.send("JOIN main\n")
		for i in channels:
			socket.send('JOIN '+i+'\n')
		gsocket=socket
	def onpong(self):
		global rsstime
		global rssentry
		global gsocket
		
		print "onpong(rss_smurfbot)"
		if math.floor(time.time()/60) > rsstime+10:
			f= feedparser.parse('http://balancedannihilation.org/forums/rss')
			
			if (gsocket!=0):
				s=str(f['entries'][0]['summary']).split('\n')
				print s
				gsocket.send('SAY '+'teh'+' '+s[0])
			rsstime=math.floor(time.time()/60)
		i=1
	def oncommandfromserver(self,command,args,socket):
		global mylist
		global numtalks
	
		#print len(api.getusers())
		#print 'some dick talked'
		global silent
		global lastchecked
		global MaxInterval
		global talkcounter
		global callcounter
		global channels

		global clans
		global users
		global whosaidit
		global logfile
		
		#print "plugin: oncommandfromserver(%s,%s,%s)" % (str(command),str(args),str(socket))
		
		com=str(command)
		if com=='CLIENTSTATUS':
			name=args[0]
			status=int(args[1])
			if name in mylist:
				bit0 = (status >> 2) & 1
				bit1 = (status >> 3) & 1
				bit2 = (status >> 4) & 1
				rank = 1*bit0+2*bit1+2*2*bit2
				if mylist[name][3]!=str(rank):
					
					
					#notice( 'updated rank: '+name+' from: '+mylist[name][3]+' to:'+str(rank))
					mylist[name][3]=str(rank)
		
		if com=='ADDUSER':
			#print "plugin: oncommandfromserver(%s,%s,%s)" % (str(command),str(args),str(socket))
			name=args[0]
			country=args[1]
			cpu=args[2]
			rank='-1'
			#def in_ADDUSER(name1,country,cpu):
			#print name1+" joined"
			if name in mylist:
				if mylist[name][5] != "0.0.0.0:0" or mylist[name][5]!= ":0":
					mylist[name]=[name,country.lower(),cpu, mylist[name][3],datetime.datetime.now().isoformat(), mylist[name][5]]
				else:
					mylist[name]=[name,country.lower(),cpu, mylist[name][3] ,datetime.datetime.now().isoformat(), ip+":"+port]
			else:
				mylist[name]=[name,country.lower(),cpu, '-1' ,datetime.datetime.now().isoformat(), "0.0.0.0:0"]
		if com=='SAID':	
			#print "plugin: oncommandfromserver(%s,%s,%s)" % (str(command),str(args),str(socket))
			chan=args[0]
			data=args[2]
			user=args[1]
			if len(args)>3:
				smurfname=args[3]
			numtalks=numtalks+1
			#print 'talk: %i call: %i time: %s' % (talkcounter,callcounter,datetime.datetime.now().isoformat())
			talkcounter=talkcounter+1

			if chan == 'main':
				if lastchecked + MaxInterval < datetime.datetime.now(): 
					cmd_smurfs('','teh',socket)
					lastchecked = datetime.datetime.now()
			if chan in channels:
				nowchan=chan
				if data=='smurfs':
					#print 'correct command'
					f=open(logfile,'a+')
					
					line= '%s	%s	%s	%s' % (datetime.datetime.now().isoformat(), user, smurfname, nowchan) 
					f.write(line+'\n')
					f.close()
					
					if user in users or user.find(clans[0])>=0 or user.find(clans[1])>=0 or user.find(clans[2])>=0:# or user.find(clans[3])>=0:
						if len(args)>3:
							silent=False
							whosaidit=user
							good( 'calling smurfs...for:'+smurfname+' in:' +nowchan+' by:'+whosaidit)
							cmd_smurfs(smurfname,nowchan,socket)
						else:
							cmd_smurfs('',nowchan,socket)
					else:
						bad('Unathorized usage by: '+user)
						socket.send('SAY '+nowchan+' Smurf checking is available for '+clans[0]+' and '+clans[1] +' and '+clans[2]+' members only\n')

		
	def onexit(self):
		print "plugin: onexit()"
		
def cmd_smurfs(smurf,nowchan,socket):
	global mylist
	global silent
	global lastchecked
	global MaxInterval
	global talkcounter
	global callcounter
	global channels

	global clans
	global users
	global whosaidit
		
	silent=False
	slines=0
	callcounter=callcounter+1

	dbfile=open(filename,'r')	

	for line in dbfile:
		if len(line)>10:
			if line!='\n\0' : 
				oldline2=line
				line=line.strip()
				oldline=line
				line=line.split(' ',5)
				if len(line)== 5 :
					if line[0] not in mylist:
						mylist[line[0]]=[line[0],line[1].lower(),line[2],line[3],line[4],'0.0.0.0:0']
				if len(line)==6:
					if line[0] not in mylist:
						mylist[line[0]]=[line[0],line[1].lower(),line[2],line[3],line[4],line[5]]
				if len(line)!= 6 and len(line)!= 5:
					i=1
					#print oldline
					#print oldline2
		else:
			slines=slines+1
	dbfile.close()
	#print 'small lines:'
	#print slines
	
	#print 'Total users in DB: %i' % (len(mylist))
	dbsize=len(mylist)
	
	f=open(filename,'w')
	for k,v in mylist.iteritems():
		line= '%s %s %s %s %s %s' % (k, v[1], v[2], v[3], v[4],v[5]) 
		f.write(line+'\n')
	f.close()
	
	smurfcpu=''
	smurfcountry=''
	#notice( 'Updated SmurfDB ' + str(lastchecked))
	numsmurfs=0
	#db=users

	
	if smurf!='':
		for k,v in mylist.iteritems():
			if smurf==v[0] :
				smurfcpu=v[2]
				smurfcountry=v[1]
		for k,v in mylist.iteritems():
			if smurfcpu==v[2]:
				if smurfcountry==v[1]:
					#print 'possible smurf:'
					#print v
					v=map(str, v)
					message = '<'+botname+'> %s: flag: %s  CPU=%smHz  rank=%s last online:%s ip:%s\n' % (v[0],v[1],v[2],v[3],v[4],v[5])
					if silent==False:
						socket.send('SAYPRIVATE '+whosaidit+' '+message)
					numsmurfs=numsmurfs+1
					if numsmurfs%100==0:
						print "sleeping 5 so i dont get kicked"
						time.sleep(5)
		if numsmurfs==0:
			message = '<'+botname+'> No smurf(s) found for: %s  out of %i entries, results sent in PM\n' % (smurf, dbsize)
			notice(message)
			if silent==False:
				socket.send('SAY '+nowchan+' '+message)
				socket.send('SAYPRIVATE '+whosaidit+' '+message)
		if numsmurfs>0:
			message= '<'+botname+'> %i smurf(s) found for %s, out of %i entries, results sent in PM\n' % (numsmurfs,smurf,dbsize)
			notice(message)
			if silent==False:
				socket.send('SAY '+nowchan+' '+message)
				socket.send('SAYPRIVATE '+whosaidit+' '+message)	
		#silent=True


	
#api.SocketConnect("91.121.98.29",8200)
	


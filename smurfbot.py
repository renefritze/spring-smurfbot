import string
import datetime
import time 
import feedparser
import math

from tasbot.plugin import IPlugin

class Main(IPlugin):

	def __init__(self,name,tasc):
		IPlugin.__init__(self,name,tasc)
		self.nick = tasc.main.config.get('tasbot', "nick")
		self._lastchecked = datetime.datetime.now()
		self._MaxInterval = datetime.timedelta(seconds=600)
		self._filename = 'smurfs.db'
		self._channels = ['teh','ba','badev']
		self._clans = ['[teh]']
		self._users = ['_koshi_']
		self._command = 'smurfs'
		self._dbsize = 0
		self._silent = False
		self._botname = ''
		self._mylist = dict()
		self._talkcounter = 0
		self._callcounter = 0
		self._connected = 0
		self._first = 1
		self._numtalks = 0
		self._numidlehalfhours = 0
		self._whosaidit=''

	def onconnected(self):
		self._cmd_smurfs('','',0)

	def onsaid(self,chan,user,data):
		numtalks=numtalks+1;
		#print 'talk: %i call: %i time: %s' % (talkcounter,callcounter,datetime.datetime.now().isoformat())
		talkcounter=talkcounter+1

		if chan == 'main':
			if lastchecked + MaxInterval < datetime.datetime.now(): 
				self._cmd_smurfs('','teh')
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
							self._cmd_smurfs(data,nowchan)
							
						else:
							self._cmd_smurfs('',nowchan)
					else:
						socket.send('SAY '+nowchan+' Smurf checking is available for '+clanfilter+' and '+clanfilter2 +' and '+clanfilter3+' members only')


	def cmd_clientstatus(self,args,cmd):
		name=args[0]
		status=int(args[1])
		if name in mylist:
			bit0 = (status >> 2) & 1
			bit1 = (status >> 3) & 1
			bit2 = (status >> 4) & 1
			rank = 1*bit0+2*bit1+2*2*bit2
			if mylist[name][3] != str(rank):
				#notice( 'updated rank: '+name+' from: '+mylist[name][3]+' to:'+str(rank))
				mylist[name][3] = str(rank)
				
	def cmd_adduser(self,args,cmd):
		#print "plugin: oncommandfromserver(%s,%s,%s)" % (str(command),str(args),str(socket))
		name = args[0]
		country = args[1]
		cpu = args[2]
		rank = '-1'
		#def in_ADDUSER(name1,country,cpu):
		#print name1+" joined"
		if name in mylist:
			if mylist[name][5] != "0.0.0.0:0" or mylist[name][5]!= ":0":
				mylist[name]=[name,country.lower(),cpu, mylist[name][3],datetime.datetime.now().isoformat(), mylist[name][5]]
			else:
				mylist[name]=[name,country.lower(),cpu, mylist[name][3] ,datetime.datetime.now().isoformat(), ip+":"+port]
		else:
			mylist[name]=[name,country.lower(),cpu, '-1' ,datetime.datetime.now().isoformat(), "0.0.0.0:0"]

	def cmd_said(self,args,cmd):
		#print "plugin: oncommandfromserver(%s,%s,%s)" % (str(command),str(args),str(socket))
		chan = args[0]
		data = args[2]
		user = args[1]
		if len(args) > 3:
			smurfname = args[3]
		numtalks = numtalks+1
		#print 'talk: %i call: %i time: %s' % (talkcounter,callcounter,datetime.datetime.now().isoformat())
		talkcounter = talkcounter+1

		if chan == 'main':
			if lastchecked + MaxInterval < datetime.datetime.now(): 
				self._cmd_smurfs('','teh',socket)
				lastchecked = datetime.datetime.now()
		if chan in channels:
			nowchan=chan
			if data == 'smurfs':
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
						self._cmd_smurfs(smurfname,nowchan,socket)
					else:
						self._cmd_smurfs('',nowchan,socket)
				else:
					bad('Unathorized usage by: '+user)
					socket.send('SAY '+nowchan+' Smurf checking is available for '+clans[0]+' and '+clans[1] +' and '+clans[2]+' members only\n')

	def _cmd_smurfs(smurf,nowchan,socket):
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

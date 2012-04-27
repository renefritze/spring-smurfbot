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
		self._MaxInterval = datetime.timedelta(seconds = 600)
		self._filename = 'smurfs.db'
		self._channels = ['badev']
		self._clans = ['[teh]']
		self._users = ['_koshi_']
		self._silent = False
		self._mylist = dict()

	def onconnected(self):
		self._cmd_smurfs('','')

	def cmd_clientstatus(self,args,cmd):
		name = args[0]
		status = int(args[1])
		if name in self._mylist:
			bit0 = (status >> 2) & 1
			bit1 = (status >> 3) & 1
			bit2 = (status >> 4) & 1
			rank = 1*bit0+2*bit1+2*2*bit2
			if self._mylist[name][3] != str(rank):
				#notice( 'updated rank: '+name+' from: '+self._mylist[name][3]+' to:'+str(rank))
				self._mylist[name][3] = str(rank)
				
	def cmd_adduser(self,args,cmd):
		name = args[0]
		country = args[1]
		cpu = args[2]
		rank = '-1'
		#def in_ADDUSER(name1,country,cpu):
		#print name1+" joined"
		if name in self._mylist:
			if self._mylist[name][5] != "0.0.0.0:0" or self._mylist[name][5]!= ":0":
				self._mylist[name]=[name,country.lower(),cpu, self._mylist[name][3],datetime.datetime.now().isoformat(), self._mylist[name][5]]
			else:
				self._mylist[name]=[name,country.lower(),cpu, self._mylist[name][3] ,datetime.datetime.now().isoformat(), ip+":"+port]
		else:
			self._mylist[name]=[name,country.lower(),cpu, '-1' ,datetime.datetime.now().isoformat(), "0.0.0.0:0"]

	def cmd_said(self,args,cmd):
		chan = args[0]
		data = args[2]
		user = args[1]
		if len(args) > 3:
			smurfname = args[3]

		if chan == 'main':
			if (self._lastchecked + self._MaxInterval) < datetime.datetime.now(): 
				self._cmd_smurfs('','teh')
				self._lastchecked = datetime.datetime.now()
		if chan in channels:
			nowchan=chan
			if data == 'smurfs':
				self.logger.info('%s	%s	%s	%s' % (datetime.datetime.now().isoformat(), user, smurfname, nowchan))
				
				if user in users or user.find(clans[0]) >= 0 or user.find(clans[1]) >= 0 or user.find(clans[2])>=0:# or user.find(clans[3])>=0:
					if len(args) > 3:
						self._silent = False
						self.logger.info( 'calling smurfs...for: %s in: %s by:' % (smurfname,nowchan,user))
						self._cmd_smurfs(smurfname,nowchan)
					else:
						self._cmd_smurfs('',nowchan)
				else:
					self.logger.error('Unathorized usage by: '+user)
					self.tasclient.say(nowchan, ' Smurf checking is available for '+clans[0]+' and '+clans[1] +' and '+clans[2]+' members only')

	def _cmd_smurfs(self, smurf, nowchan):
		self._silent = False
		with open(self._filename,'r') as dbfile:
			for line in dbfile:
				if len(line) > 10:
					if line != '\n\0': 
						oldline2 = line
						line = line.strip()
						oldline = line
						line = line.split(' ',5)
						if len(line) == 5 :
							if line[0] not in self._mylist:
								self._mylist[line[0]]=[line[0],line[1].lower(),line[2],line[3],line[4],'0.0.0.0:0']
						if len(line) == 6:
							if line[0] not in self._mylist:
								self._mylist[line[0]]=[line[0],line[1].lower(),line[2],line[3],line[4],line[5]]
						if len(line) != 6 and len(line) != 5:
							pass
		#print 'Total users in DB: %i' % (len(self._mylist))
		dbsize = len(self._mylist)
		
		with open(self._filename,'w') as f:
			for k,v in self._mylist.iteritems():
				line = '%s %s %s %s %s %s' % (k, v[1], v[2], v[3], v[4],v[5]) 
				f.write(line+'\n')
		
		smurfcpu = ''
		smurfcountry = ''
		#notice( 'Updated SmurfDB ' + str(lastchecked))
		numsmurfs = 0
		if smurf != '':
			for k,v in self._mylist.iteritems():
				if smurf == v[0]:
					smurfcpu = v[2]
					smurfcountry = v[1]
			for k,v in self._mylist.iteritems():
				if smurfcpu == v[2]:
					if smurfcountry == v[1]:
						#print 'possible smurf:'
						#print v
						v = map(str, v)
						message = '<'+self.nick+'> %s: flag: %s  CPU=%smHz  rank=%s last online:%s ip:%s\n' % (v[0],v[1],v[2],v[3],v[4],v[5])
						if not self._silent:
							self.tasclient.saypm(whosaidit, message)
						numsmurfs = numsmurfs + 1
						if numsmurfs % 100 == 0:
							print "sleeping 5 so i dont get kicked"
							time.sleep(5)
			if numsmurfs == 0:
				message = '<'+self.nick+'> No smurf(s) found for: %s  out of %i entries, results sent in PM\n' % (smurf, dbsize)
			else:
				message= '<'+self.nick+'> %i smurf(s) found for %s, out of %i entries, results sent in PM\n' % (numsmurfs,smurf,dbsize)
			self.logger.info(message)
			if not self._silent:
				self.tasclient.say(nowchan, message)
				self.tasclient.saypm(whosaidit, message)	

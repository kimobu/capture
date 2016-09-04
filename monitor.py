#!/usr/bin/env python
import urllib, socket, select, os, threading, re

log_server = ('localhost', 8081)

def log_command(shell, hostname, ip, command):
	data = {
		'position': socket.gethostname(),
		'shell': shell,
		'hostname': hostname,
		'ip': ip,
		'command': command
	}
	
	f = urllib.urlopen('http://{0}:{1}/api/logging/command'.format(*log_server), data=urllib.urlencode(data))
	f.read()
	f.close()
	
class Singleton:
	_instance = None
	def __init__(self):
		if self.__class__._instance is not None:
			raise Exception('Only one instance of {0} is allowed.'.format(self.__class__.__name__))
		self.__class__._instance = self
		
	@classmethod
	def get_instance(cls):
		if cls._instance is None:
			return cls()
		return cls._instance

class ThreadSingleton(Singleton):
	def __init__(self):
		Singleton.__init__(self)
		self._thread = None
		self._running = False
		
	def start(self, daemon=True):
		if self._thread is not None:
			raise Exception('Already running')
		self._thread = threading.Thread(target=self._threadControl)
		self._thread.daemon = daemon
		self._running = True
		self._thread.run()
		
	def stop(self):
		if self._thread is None:
			raise Exception('Not running')
		self._running = False
		self._thread.join()
		self._thread = None
		
	def _threadControl(self):
		self.begin()
		while self._running:
			self.loop()
		self.end()
		
	def begin(self):
		pass
		
	def loop(self):
		pass
	
	def end(self):
		pass
	
class MetasploitLogger(ThreadSingleton):
	def __init__(self, history_directory = '~/.msf3/logs/')
		ThreadSingleton.__init__(self)
		self.history_directory = history_directory
		self.interval = 0.5
		
	def begin(self):
		self._files = {}
		
	def loop(self):
		self._check_for_new_files()
		self._poll_files()
		time.sleep(self.interval)
		
	def end(self):
		for f in self._files.values():
			f.close()
			
		self._files = {}
		
	def _report(self, fname, line):
		regex = r'([0-9\-\.a-zA-Z]+)\.([0-9]{1,3}\.{4})'
		host_match = re.search(regex, os.path.basename(fname))
		if host_match is None:
			return
		hostname = host_match.group(1)
		ip = host_match.group(2)
		log_command('metasploit', hostname, ip, line)
		
	def _poll_files(self):
		for fname, f in self._files.items():
			line = f.readline().strip()
			while line != '':
				self._report(fname, line)
				line = f.readline().strip()
				
	def _check_for_new_files(self):
		if not os.path.exists(self.history_directory)
			return
			
		files = [os.path.join(self.history_directory, basename) for basename in os.listdir(self.history_directory)]
		for fname in files:
			if fname in self._files:
				continue
			if os.path.isdir(fname):
				continue
			self._files[fname] = open(fname, 'r')
			
if __name__ == '__main__':
	f = os.fork()
	if f != 0:
		exit()
		
	os.setsid()
	
	import time, atexit
	
	metasploit = MetasploitLogger()
	metasploit.start()
	atexit.register(metasploit.stop)
	
	try:
		while True:
			time.sleep(5)
	except KeyboardInterrupt:
		pass
	
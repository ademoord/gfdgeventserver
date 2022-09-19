'''

@url: file:///192.168.1.50:/home/andromeda/Data/svn/gfd500/SW/trunk/server.py
@author: Andromeda
@rev: 10
@commitdate: 05-09-2014
'''
#!/usr/bin/env python
# Simple Echo Server using Gevent SSL and StreamServer - server.py

from gevent.server import StreamServer
import fdb

wMsg = '''My ID: %d\r\nMy Address: %s:%d\r\nDatabase: %s\r\nStatus: %s\r\n\r\nWelcome to GFD Server!\r\nType \'help\' for help.\r\n\r\n'''
db = "192.168.1.50:/var/lib/firebird/2.5/data/employee.fdb"
status = 'Status: %s\r\nDatabase: %s\r\n\r\n'

help = '''- Type 'stat' to displays Connection Status\r\n- Type 'help' to displays this page\r\n- Type 'quit' to exit\r\n\r\n'''


# this handler will be run for each incoming connection in a dedicated greenlet
def echoServer(socket, address):
	
	print('New connection from %s:%s' % address)
	qry = "SELECT emp_no FROM employee WHERE last_name = 'Phong'"
	
	# connecting to database Employee
	con = fdb.connect(dsn=db, user="SYSDBA", password="ciwaruga")
	cur = con.cursor()
	
	# verify address
	if address is None:
		stat = "Not Connected"
	else:
		stat = "Connected"
	
	# verify metadata db connection
	if con is None:
		socket.sendall('Failed connecting to GFD Database. Type \'quit\' to exit.\r\n')
	else:
		cur.execute(qry)
		myID = cur.fetchall()[0][0]
		socket.sendall(wMsg % (myID, address[0], address[1], db, stat))
		
		fileobj = socket.makefile()						# using a makefile because we want to use readline()
	
		# simple client commands	
		while True:
			
			line = fileobj.readline()
			
			if not line:
				print("Client disconnected.")
				break

			elif line.strip().lower() == 'quit':
				print("Client quit.")
				break

			elif line.strip().lower() == 'help':
				print("Client requesting help page.")
				socket.sendall(help)
						
			elif line.strip().lower() == 'stat':
				print("Client requesting status.")
				socket.sendall(status % (stat, db))
				
			else:
				print("Client wrong typing command.")
				socket.sendall("Unknown command\r\n\r\n")
			
			fileobj.write("> ")
			fileobj.flush()
# 			fileobj.write(line)								# echo process
# 			fileobj.flush()
# 			print("Echoed %r" % line)
		
		
		
if __name__ == '__main__':
	
	# to make server use SSL, pass certfile and keyfile arguments to the constructor
	server = StreamServer(('0.0.0.0', 6000), echoServer)
	print('Starting GFD Server on port 6000')
	server.serve_forever()		# running the server forever

	
	
	

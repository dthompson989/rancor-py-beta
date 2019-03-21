# A somewhat basic portscanner
import socket
import subprocess
import sys
import datetime

if __name__ == '__main__':
	subprocess.call('clear', shell = True)

	remoteServerIP = input('IP to Scan: ')

	print('-' * 60)
	print('Scanning remote host ', remoteServerIP)
	print('-' * 60)

	t1 = datetime.now()

	try:
		for port in range(1, 1025):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((remoteServerIP, port))
			if result == 0:
				print('Port {}:    OPEN'.format(port))
			sock.close()
	except KeyboardInterrupt:
			print('Scan Stopped')
			sys.exit()
	except socket.gaierror:
			print('Hostname could not be resolved')
			sys.exit()
	except socket.error:
			print('Could not connect to server')
			sys.exit()

	t2 = datetime.now()

	total = t2 - t1

	print('Scan Complete: ', total)

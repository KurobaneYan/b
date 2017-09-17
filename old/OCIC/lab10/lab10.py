import socket
import time
import threading
import urllib2
import Queue
from bs4 import BeautifulSoup
from urlparse import urljoin

def urldawnload(work_queue, lsturl, i, stat, lock, lock_stat):
	for _ in xrange(5):
		if not work_queue.empty():
			url = work_queue.get()

			lock.acquire()
			f = 0
			if url in lsturl:
				f = 1
			else:
				f = 0
				lsturl.append(url)
			lock.release()
			if f == 1:
				work_queue.task_done()
				continue

			lock_stat.acquire()
			t = time.time()
			resp = urllib2.urlopen(url)
			html = resp.read()
			stat[1] = stat[1] + len(html) / 1000.0 * 2.0
			stat[3] = stat[3] + time.time() - t
			lock_stat.release()
			soup = BeautifulSoup(html, "html.parser")
			links = soup('a')
			for link in links:
				if ('href' in dict(link.attrs)):
					url_n = urljoin(url,link['href'])
					if url_n.find("'") != -1: continue
					url_n = url_n.split('#')[0]
					if url_n[0:4] == 'http':
						if url_n in lsturl:
							continue
						else:
							work_queue.put(url_n)
			
			work_queue.task_done()
		else:
			time.sleep(10)
			if work_queue.empty():
				break


def geturls(starturl):
	work_queue = Queue.Queue()
	lst_thread = []
	lst_url = []
	lock = threading.Lock()
	lock_stat = threading.Lock()
	stat = ["Kbyte", 0.0, "time download", 0.0]
	work_queue.put(starturl)
	for i in xrange(4):
		lst_thread.append(threading.Thread(target=urldawnload, args=(work_queue, lst_url, i, stat, lock, lock_stat)))
		lst_thread[i].start()

	for i in xrange(4):
		lst_thread[i].join()
	lst_url.sort()
	for x in lst_url:
		print(x)
	print(stat)
		

if __name__ == "__main__":
	serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
	serv_sock.bind(('', 53188))
	serv_sock.listen(10)

	for _ in xrange(2):
	    client_sock, client_addr = serv_sock.accept()
	    data = client_sock.recv(1024)
	    t1 = threading.Thread(target=geturls, args=(data, ))
	    t1.start()
	    
	    client_sock.close()
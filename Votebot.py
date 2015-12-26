import requests
import unicodedata
from bs4 import BeautifulSoup as Soup
import Scraper
import ast


def extract_tags(list, remove_stuff):
	for tag in list:
		if tag.name == 'style':
			tag.extract()
		if tag.has_attr('style') and tag['style'] == 'display:none':
			tag.extract()
		if tag.has_attr('class') and tag['class'][0] in remove_stuff:
			tag.extract()
		if list.count(tag) > 1:
			tag.extract()
		if not tag.text:
			tag.extract()

def get_proxies(x): 
	proxy_request = requests.get('http://proxylist.hidemyass.com/search-1301708#listable')
	souped = Soup(proxy_request.text, 'html.parser')
	
	row = souped.find('table', id='listable').find_all('tr', rel=True)[x].find_all('td')
	port = row[2].text.strip()	

	remove1 = row[1].find_all('.(\w*){display:none}', row[1].span.style.text)
	extract_tags(row[1].find_all('span'), remove1)
	extract_tags(row[1].find_all('div'), remove1)
	extract_tags(row[1].find_all('style'), remove1)
	ip = row[1].text.strip()
	
	lepro = {'http' : ip + ':' + port}
	return lepro


def get_data(artist, proxies):
	the_request = requests.get('http://thekingofmusic.com/', proxies=proxies)
	html_of_request = Soup(the_request.text, 'html.parser')
	answer_id = ''
	poll_nonce = ''

	if html_of_request.find(id='polls_form_1') is None:
		print 'Already Voted Before'
	else: 
		poll_nonce = html_of_request.find(id='poll_1_nonce')['value']
		labels = html_of_request.find(id='polls_form_1').find_all('label')
		for label in labels:
			if label.text == artist: 
				answer_id = label.parent.find('input')['value']
				break
	return answer_id, poll_nonce


def send_vote(answer_id, poll_nonce, proxies):
	data = {
		'action': 'polls',
        'view': 'process',
        'poll_id': '1',
        'poll_1': answer_id,
        'poll_1_nonce': poll_nonce
	}
	r = requests.post('http://thekingofmusic.com/wp-admin/admin-ajax.php', data=data, proxies=proxies)


if __name__ == '__main__':
	proxies = get_proxies(0)
	print 'Receiving data...'
	answer, poll = get_data('Jimi Hendrix', proxies)
	print 'Voting...'
	send_vote(answer, poll, proxies)




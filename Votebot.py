import requests
from bs4 import BeautifulSoup as Soup

def get_proxies(): 
	proxy_request = requests.get('http://proxylist.hidemyass.com/search-1301708#listable')

	lepro = {'http': 'http://'}

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
	proxies = get_proxies()
	print 'Receiving data...'
	answer, poll = get_data('Jimi Hendrix', proxies)
	print 'Voting...'
	send_vote(answer, poll, proxies)




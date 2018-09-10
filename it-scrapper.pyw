from bs4 import BeautifulSoup
import requests

page_max = 136
download_links = []
categories = [
				"web-development",
				"programming",
				"datebases",
				"game-programming",
				"graphics-design",
				"operating-systems",
				"networking-cloud-computing",
				"administration",
				"computers-technology",
				"certification",
				"enterprise",
				"marketing-seo",
				"hardware",
				"security",
				"software",
			]

def download_everything():
	try:
		for page_num in range(1, page_max + 1):
			url = 'http://www.allitebooks.com/page/{}'.format(str(page_num))
			soup = get_page_content(url)
			books_in_page = get_books_in_page(soup)
			for book_url in books_in_page:
				splitted_url = book_url.split("/")
				book_file_name = splitted_url[len(splitted_url) -1]
				print " "
				print "Downloading file {} at page {}".format(book_file_name, str(page_num))
				try:
					download_file(book_url)
				except Exception as exc:
					print "An error ocurred, continuing ..."
					print str(exc)

	except Exception as exc:
					print "An error ocurred, continuing ..."
					print str(exc)


def get_page_content(url):
	page = requests.get(url)
	page_content = page.content
	soup = BeautifulSoup(page_content, "html.parser")
	return soup

def get_books_in_page(page_soup):

	books_in_page = []
	books = page_soup.findAll("article", {"class": "post"})
	for book in books:
		try:
			title = book.find("h2").get_text()
			book_url = book.find("a")["href"]
			file_url = get_file_link(book_url)
			books_in_page.append(file_url)
		except Exception as exc:
			print "An error ocurred, continuing ..."
			print str(exc)
			continue

	return books_in_page


def download_file(url):
	local_filename = url.split("/")[len(url.split("/")) -1]
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)

	return local_filename

def get_file_link(book_url):
	download_page_soup = get_page_content(book_url)
	download_element = download_page_soup.findAll("span", {"class" : "download-links"})[0]
	download_link = download_element.find("a")["href"]

	return download_link

def download_search(term):
	try:
		for page_num in range(1, page_max + 1):
			url = 'http://www.allitebooks.com/page/{}/?s={}'.format(str(page_num), term)
			soup = get_page_content(url)
			books_in_page = get_books_in_page(soup)
			for book_url in books_in_page:
				splitted_url = book_url.split("/")
				book_file_name = splitted_url[len(splitted_url) -1]
				print "[D] Downloading file {} at page {}".format(book_file_name, str(page_num))
				try:
					download_file(book_url)

				except Exception as exc:
					print "An error ocurred, continuing ..."
					print str(exc)

	except Exception as exc:
		print "An error ocurred, continuing ..."
		print str(exc)

def main():
	print "Welcome to Allitebooks Books downloader"
	main_options()

def main_options():
	print "Select an option: "
	print "[1] Download everything"
	print "[2] Search an specific term" 
	print ""

	option = raw_input("#>")
	if option == "1":
		download_everything()
	elif option == "2":
		term = raw_input("Introduce el termino que quieres buscar: ")
		print "Buscando y descargando libros de {}".format(term)
		download_search(term)
	else:
		main_options()

main()
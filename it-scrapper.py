from bs4 import BeautifulSoup
import requests
import os, sys


global book_page_num
book_page_num = 0

page_max = 136
download_links = []
categories = {
				1:"web-development",
				2:"programming",
				3:"datebases",
				4:"game-programming",
				5:"graphics-design",
				6:"operating-systems",
				7:"networking-cloud-computing",
				8:"administration",
				9:"computers-technology",
				10:"certification",
				11:"enterprise",
				12:"marketing-seo",
				13:"hardware",
				14:"security",
				15:"software"
			}
def list_categories():
	print "                    CATEGORIAS                     "
	print "    ---------------------------------------------"
	print "     N  |  Categoria                             "
	print "    ---------------------------------------------"

	for k,v in categories.iteritems():
		print "    [{}] | {}".format(k,v)

	selected_category = input("#> ")
	return selected_category

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

	books_in_page = {}
	books = page_soup.findAll("article", {"class": "post"})

	for book in books:
		#try:
			title = book.find("h1").get_text()
			book_url = book.find("a")["href"]
			file_url = get_file_link(book_url)

			book_entry = {
				"title": title,
				"url": book_url,
				"file_url": file_url,
			}

			books_in_page[books.index(book)] = book_entry

		#except Exception as exc:
		#	print "An error ocurred, continuing ..."
		#	print str(exc)
		#	continue

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
			for booknum, bookdata in books_in_page.iteritems(): #Adaptar a dict
				book_url = books_in_page[booknum]["file_url"]
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

def list_book_in_page(page_url):

	base_url = "http://www.allitebooks.com/"
	extended_url = base_url + page_url
	actual_page_num = page_url.split("/")[len(page_url.split("/")) -1 ]
	books_in_current_page = get_books_in_page(get_page_content(extended_url)) # Pasar soup, no string

	print "                LIBROS -- PAG [{}]             ".format(actual_page_num)
	print "    ---------------------------------------------"
	print "     N  |  Categoria                             "
	print "    ---------------------------------------------"

	for booknum, bookdata in books_in_current_page.iteritems():
		print "    [{}] | {}".format(booknum, bookdata["title"])

	print ""
	print "    ---------------------------------------------"
	print "    <---- (A)tras       |      (S)iguiente ----->"
	print "    ---------------------------------------------"

	selected_book = raw_input("#> ")
	return selected_book

	
def book_selector(current_num):

	local_num = current_num
	os.system("cls")

	chosen_cat = list_categories()

	sub_url = "/{}/page/{}".format(chosen_cat, current_num)
	selected_book = list_book_in_page(sub_url)

	if (selected_book == "a" or selected_book == "A"): # Ir atras
		
		if (book_page_num > 0):
			local_num -= 1
			book_selector(local_num)
			
		elif book_page_num == 0:
			print "No puedes ir atras"
			book_selector(local_num)

	elif (selected_book == "s" or selected_book == "S"): # Ir adelante
		local_num += 1
		book_selector(local_num)

	elif (selected_book not in "abcdefghijklmnopqrstuvwxyz"):
		book_download_url = books_in_current_page[int(selected_book)]["file"]
		print "Descargando..."
		download_file(book_download_url)
		print "Hecho"

		book_selector()
		
def main_options():
	print "Select an option: "
	print "[1] Download everything"
	print "[2] Search an specific term" 
	print "[3] Navigate categories and books"
	print ""

	option = raw_input("#>")

	if option == "1":
		download_everything()

	elif option == "2":
		term = raw_input("Introduce el termino que quieres buscar: ")
		print "Buscando y descargando libros de {}".format(term)
		download_search(term)

	elif option == "3":
		book_selector(book_page_num)

	else:
		main_options()

main()
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
	print("                    CATEGORIES                   ")
	print("    ---------------------------------------------")
	print("     N  |  Cat.                                  ")
	print("    ---------------------------------------------")

	for num, categoryName in categories.items():
		print(f"    [{num}] | {categoryName}")

	selected_category = input("#> ")
	return selected_category

def get_page_content(url):
	return BeautifulSoup(requests.get(url).content, "html.parser")

def get_books_in_page(page_soup):
	books_in_page = {}
	books = page_soup.findAll("article", {"class": "post"})

	for book in books:
		# Extract book data
		title = book.find("h1").get_text()
		book_url = book.find("a")["href"]
		file_url = get_file_link(book_url)

		# Add entry
		books_in_page[books.index(book)] = { "title": title, "url": book_url, "file_url": file_url }

	return books_in_page


def download_file(url):
	local_filename = url.split("/")[len(url.split("/")) -1]
	
	file_data = requests.get(url)
	with open(local_filename, 'wb') as file_handle:
		file_handle.write(file_data)
		
	return local_filename

def get_file_link(book_url):
	return get_page_content(book_url).findAll("span", {"class" : "download-links"})[0].find("a")["href"]

def download_search(term):
	try:
		for page_num in range(1, page_max + 1):
			url = 'http://www.allitebooks.com/page/{}/?s={}'.format(str(page_num), term)
			
			for booknum, bookdata in get_books_in_page(get_page_content(url)).items()
				book_url = books_in_page[booknum]["file_url"]
				splitted_url = book_url.split("/")
				book_file_name = splitted_url[len(splitted_url) -1]
				
				print(f"[D] Downloading file {book_file_name} at page {page_num}")
				
				try:
					download_file(book_url)
					
				# Ignore errors at this point because not being able to find any link doesn't really mean anything.
				except Exception: 
					continue

	except Exception as exc:
		print("Couldn't find any data mathching that query, please try again")
		main()

def main():
	print("Welcome to Allitebooks Books downloader")
	main_options()

def list_book_in_page(page_url):
	base_url = "http://www.allitebooks.com/"
	extended_url = base_url + page_url
	actual_page_num = page_url.split("/")[len(page_url.split("/")) -1 ]
	books_in_current_page = get_books_in_page(get_page_content(extended_url)) 

	print(f"                Books -- Pag. [{actual_page_num}]               ")
	print("    ---------------------------------------------")
	print("     N  |  Cat.                                  ")
	print("    ---------------------------------------------")

	for booknum, bookdata in books_in_current_page.items():
		print "    [{}] | {}".format(booknum, bookdata["title"])

	print("    ---------------------------------------------")
	print("    <---- (P)revious     |          (N)ext ----->")
	print("    ---------------------------------------------")

	selected_book = raw_input("#> ")
	return selected_book

	
def book_selector(current_num):
	local_num = current_num
	chosen_cat = list_categories()

	sub_url = "/{}/page/{}".format(chosen_cat, current_num)
	selected_book = list_book_in_page(sub_url)

	if selected_book.lower() == "p": # Previous
		if (book_page_num > 0): 
			local_num -= 1
			
		elif book_page_num == 0:
			print("You can't go back anymore")
			
		book_selector(local_num)
			
	elif selected_book.lower() == "n": # Next
		local_num += 1
		book_selector(local_num)

	elif (selected_book not in "abcdefghijklmnopqrstuvwxyz"):
		book_download_url = books_in_current_page[int(selected_book)]["file"]
		print("Downloading...")
		download_file(book_download_url)
		print("Done")

		book_selector()
		
def main_options():
	print("Select an option: ")
	print("[1] Search an specific term")
	print("[2] Navigate categories and books")

	option = input("#>")

	if option == 1:
		term = input("Term > ")
		print(f"Searching and downloading books about { term }...")
		download_search(term)

	elif option == 2:
		book_selector(book_page_num)

	else:
		print("Oops! Choose a valid option!")
		main_options()

main()

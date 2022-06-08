from bs4 import BeautifulSoup as bs
from colorama import Fore
import colorama
import requests
import re

colorama.init(autoreset=True)

def main():
	print(table_count("https://en.wikipedia.org/wiki/Timeline_of_artificial_intelligence"))
	

def table_count(request):
	try:
		try:
			site = requests.get(request).text

		except requests.exceptions.MissingSchema:
			site = requests.get("https://" + request).text

	except requests.exceptions.ConnectionError:
		print(f"\n{Fore.RED}No Internet Connection (ConnectionError) or Invalid URL")
		exit()

	soup = bs(site, "lxml")

	average_rows = 0
	columns = 0
	table = 0
	tbody = 0
	thead = 0
	td = 0
	tr = 0
	th = 0


	for i in soup.find_all("table"):
		table += 1

	for i in soup.find_all("tbody"):
		tbody += 1

	for i in soup.find_all("thead"):
		thead += 1

	for i in soup.find_all("tr"):
		tr += 1

	for i in soup.find_all("td"):
		td += 1

	for i in soup.find_all("th"):
		th += 1

	if tr != 0: 
		columns = "%.0f" % ((td + th) / tr)

	if table != 0:
		average_rows = "%.2f" % (tr / table)

	if table <= 1:
		return {
			"table": table,
			"tbody": tbody,
			"thead": thead,
			"tr (rows)": tr,
			"td": td,
			"th": th,
			"columns (in progress)": columns,
			"average rows": average_rows
		}

	if table >= 1:
		return {
			"table": table,
			"tbody": tbody, 
			"thead": thead, 
			"tr (rows)": tr, 
			"td": td, 
			"th": th, 
			"average rows": average_rows
		}



if __name__ == "__main__":
	main()


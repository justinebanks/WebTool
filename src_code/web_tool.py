import argparse
import colorama
from colorama import Fore
import keyword_search as ks
import web_search as ws
import table_search as ts
import requests
import json
import os


def create_starter_file():
	if not os.path.exists("web_tool.json"):
		with open("web_tool.json", "w") as file:
			new_file = json.dumps({"Website": "google.com", "Keyword": "test"}, indent=4)
			file.write(new_file)


colorama.init(autoreset=True)

parser = argparse.ArgumentParser(description="Check websites for features, keywords, and more")

parser.add_argument(
	"-u",
	"--url",
	type=str,
	required=False,
	help="Input preferred URL (Default is \"google.com\") (Dependency of Other Commands)"
)

parser.add_argument(
	'-kw',
	'--keyword',
	type=str,
	required=False,
	help="Input Keyword (Default is \"test\") (Only Uses Regular Expression) (Dependency of Other Commands)"
)

group = parser.add_mutually_exclusive_group()

group.add_argument(
	"-s",
	"--status",
	action="store_true",
	required=False,
	help="Returns the Status of a Website (Dependent On -u)"
)

group.add_argument(
	"-f",
	"--file",
	action="store_true",
	required=False,
	help="Saves HTML Code of the Website to \"output.html\" (Dependent On -u)"
)

group.add_argument(
	"-ws",
	"--search",
	action="store_true",
	required=False,
	help="Gets Phone Numbers, Emails, and Links from the HTML Code and saves it to \"web_search.json\" (Dependent On -u)"
)

group.add_argument(
	"-i",
	"--itercount",
	action="store_true",
	required=False,
	help="Finds Iteration Count of Specified Keyword (Dependent On -kw)"
)

group.add_argument(
	"-t",
	"--tablecount",
	action="store_true",
	required=False,
	help="Finds Number of Tables (<table>) in Website (Dependent On -u)"
)


args = parser.parse_args()
create_starter_file()

if args.url != None:
	with open("web_tool.json", "r") as file:
		json_import = json.load(file)

	with open("web_tool.json", "w") as file:
		json_import["Website"] = args.url

		json_import = json.dumps(json_import, indent=4)
		file.write(json_import)


if args.keyword != None:
	with open("web_tool.json", "r") as file:
		json_import = json.load(file)

	with open("web_tool.json", "w") as file:
		json_import["Keyword"] = args.keyword
		json_import = json.dumps(json_import, indent=4)
		file.write(json_import)



with open("web_tool.json", "r") as file:
	keyword = json.load(file)["Keyword"]

	if keyword == "":
		keyword = "test"


with open("web_tool.json", "r") as file:
	url = json.load(file)["Website"]

	if url == "" or url == " ":
		url = "google.com"



try:
	try:
		r = requests.get(url)

	except requests.exceptions.MissingSchema:
		r = requests.get(f"https://{url}")

except requests.exceptions.ConnectionError:
	print(f"{Fore.RED}\nConnection Error Occurred.\n\nThis can be caused by the Following:\n1) No Internet Connection\n2) Invalid URL")
	exit()


print(f"\nWebsite: {r.url}")
print(f"Keyword: \"{keyword}\"\n")

if args.status:
	if r.status_code < 350:
		print(f"{Fore.GREEN}Status: {r.status_code}")
	elif r.status_code > 350:
		print(f"{Fore.RED}Status: {r.status_code}")


if args.file:
	with open("output.html", "w") as file:
		file.write(r.text)

		print(f"{Fore.GREEN}Successfully Saved HTML Code to \"output.html\"")


if args.search:
	ws.WebSearch(request=url, show_urls=False)

	print(f"{Fore.GREEN}Sucessfully Saved Data to \"web_search.json\"")


if args.itercount:
	ksearch = ks.KeywordSearch(request=url, kw=keyword)
	match_count = ksearch.get_keyword_count()
	print(f"{Fore.GREEN}Inside of the website there are {match_count} iterations of \"{keyword}\"")


if args.tablecount:
	table_count = ts.table_count(url) # (FIX DivisionByZero Error)
	i = 0

	for key in list(table_count.keys()):
		val = list(table_count.values())[i]
		print(f"{Fore.GREEN}{key}:{Fore.RESET} {val}")
		i += 1



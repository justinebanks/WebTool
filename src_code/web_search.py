from colorama import Fore
import colorama
import requests
import json
import sys
import re


colorama.init()

class WebSearch:
	def __init__(self, request=None, output="web_search.json", show=True, show_urls=True, show_times=True):

		if request is None:
			request = sys.argv[1]

		try:
			try:
				site = requests.get(request)
				website = site.text

			except requests.exceptions.MissingSchema:
				site = requests.get("https://" + request)
				website = site.text

		except requests.exceptions.ConnectionError:
			print(f"\n{Fore.RED}No Internet Connection (ConnectionError) or Invalid URL")
			exit()

		if site.url != request:
			print("\n--------------------")
			print(" Search Directed To:\n {}".format(site.url))
			print("--------------------")

		results = {
			"Website": site.url,
			"Phone Numbers": self.get_phones(website, print_results=show),
			"Emails": self.get_emails(website, print_results=show),
			"Urls": self.get_urls(website, print_results=show_urls),
			"Times": self.get_times(website, print_results=show_times)
		}

		results = json.dumps(results, indent=4)
		print("")

		with open(output, "w") as file:
			file.write(results)


	def get_urls(self, website: str, print_results=True, upload_results=True):
		urls = list()
		pattern = re.compile(r"(https://|http://)?(\w+\.)?(\w+)(\.(uk|gov|io|com|org|net|ru|us|ca|it|io|co))(/[\w.-]+)*(((/)?\?)?([\w\d]+=[\w\d]+)+(&)?)*")
		url_matches = pattern.finditer(website)

		print("")
		for match in list(set(url_matches)):
			if upload_results:
				urls.append(match.group(0))
			if print_results:
				print(f"{Fore.GREEN}URLS:{Fore.RESET} {match.group(0)}")

		return list(set(urls))


	def get_emails(self, website: str, print_results=True, upload_results=True):
		emails = list()
		pattern = re.compile(r"([\w\d\._-]+)@([\w\d.]+)(\.(uk|gov|io|com|org|net|ru|us|ca|it|io|co))")
		email_matches = pattern.finditer(website)

		print("")
		for match in list(set(email_matches)):
			if upload_results:
				emails.append(match.group(0))
			if print_results:
				print(f"{Fore.GREEN}Emails:{Fore.RESET} {match.group(0)}")

		return list(set(emails))


	def get_phones(self, website: str, print_results=True, upload_results=True):
		phones = list()
		pattern = re.compile(r"(786|305|617|800|415|312|512|917|718|202|650|214|312|818|404)[-.,*\s](\d{3})[-.,*\s](\d{3,4})")
		phone_matches = pattern.finditer(website)

		print("")
		for match in list(set(phone_matches)):
			if upload_results:
				phones.append(match.group(0))
			if print_results:
				print(f"{Fore.GREEN}Phones:{Fore.RESET} {match.group(0)}")
		
		return list(set(phones))


	def get_times(self, website: str, print_results=True, upload_results=True):
		times = list()
		pattern = re.compile(r"(\d{1,2})[:\.](\d{2})([\.:]\d{1,3})?(AM|PM|am|pm|a\.m|p\.m)?")
		time_matches = pattern.finditer(website)

		print("")
		for match in time_matches:
			if upload_results:
				times.append(match.group(0))
			if print_results:
				print(f"{Fore.GREEN}Times:{Fore.RESET} {match.group(0)}")

		return list(set(times))


if __name__ == "__main__":
	WebSearch(request="fl.milesplit.com")


"""
https://fl.milesplit.com/meets/455030-fr-luis-ripoll-sj-relays-2022/info#.Yiq3fXrMLD4
https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox

"""

text = """

12:20.10am


11:07:80

20:18.93

"""

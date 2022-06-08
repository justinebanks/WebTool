from colorama import Fore
import colorama
import requests
import re


colorama.init(autoreset=True)

class KeywordSearch:
	def __init__(self, request, kw):
		self.url = request
		self.keyword = kw

		try:
			try:
				self.site = requests.get(request).text

			except requests.exceptions.MissingSchema:
				self.site = requests.get("https://" + request).text

		except requests.exceptions.ConnectionError:
			print(f"\n{Fore.RED}No Internet Connection (ConnectionError) or Invalid URL")
			exit()


	def get_keyword_count(self, one_word=False, ignore_case=True):

		if ignore_case:
			pattern = re.compile(fr"{self.keyword}", re.IGNORECASE)

		else:
			pattern = re.compile(fr"{self.keyword}")

		self.matches = pattern.finditer(self.site)
		match_count = 0

		for match in self.matches:
			match_count += 1

		return match_count




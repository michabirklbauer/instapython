#!/usr/bin/env python3

import datetime
import json
import os

class InstaView:

	def __init__(self):
		pass

	def sanitizeUnderscores(self, some_string):
		return str(some_string.replace("_", "\\_"))

	def sanitizeEmoji(self, some_string):
		allowed = ["/", "\"", "{", "}", "\'", " ", "#", "@", "+", "[", "]", "(", ")", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "\\", "_", ":", "," , ".", ";", "-", "!", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
		word = ""
		for char in some_string:
			if char.upper() in allowed:
				word = word + char
			else:
				word = word + "?"
		return str(word)

	def san(self, some_string):
		return self.sanitizeUnderscores(self.sanitizeEmoji(some_string))

	def RMDtoPDF(self):
		try:
			os.system("Rscript -e 'library(rmarkdown); render(\"instaview.Rmd\")'")
		except:
			pass
		print("If PDF file isn't created, try knitting manually!")
		return 0

	def createRMD(self, path = 0):

		#setting path
		if path != 0:
			os.chdir(path)

		# get date
		today = datetime.datetime.today().strftime('%d-%m-%Y')
		# Rmd header definition
		rmd_header = "---\ntitle: \"Instagram Data\"\nauthor: \"Micha Birklbauer\"\ndate: "+str(today)+"\noutput:\n  pdf_document:\n    toc: yes\n---\n"

		# creating new Rmd file
		with open("instaview.Rmd", "w") as rmd_file:
			rmd_file.write(rmd_header)
			rmd_file.close()

		with open("instaview.Rmd", "a") as rmd_file:

			# getting profile information
			with open("profile.json", "r", errors="replace") as profile:
				profile_content = profile.read()
				profile.close()
			profile_json = json.loads(profile_content)
			rmd_file.write("# Profile Information\n\n")
			for item in profile_json:
				w = self.sanitizeUnderscores(str(item)) + " : " + self.san(str(profile_json[item])) + "\n\n"
				rmd_file.write(w)

			# getting profile settings
			with open("settings.json", "r", errors="replace") as settings:
				settings_content = settings.read()
				settings.close()
			settings_json = json.loads(settings_content)
			rmd_file.write("# Profile Settings\n\n")
			for item in settings_json:
				w = self.sanitizeUnderscores(str(item)) + " : " + self.sanitizeUnderscores(str(settings_json[item])) + "\n\n"
				rmd_file.write(w)

			# getting profile searches
			with open("searches.json", "r", errors="replace") as searches:
				searches_content = searches.read()
				searches.close()
			searches_json = json.loads(searches_content)
			rmd_file.write("# Profile Searches\n\n")
			for item in searches_json:
				for subitem in item:
					w = self.sanitizeUnderscores(str(subitem)) + " : " + self.san(str(item[subitem])) + "\n\n"
					rmd_file.write(w)
				rmd_file.write("\\_\\_\\_\\_\\_\n\n")

			# getting profile connections
			with open("connections.json", "r", errors="replace") as connections:
				connections_content = connections.read()
				connections.close()
			connections_json = json.loads(connections_content)
			rmd_file.write("# Profile Connections \n\n")
			for item in connections_json:
				w = "## " + self.sanitizeUnderscores(str(item)) + "\n\n"
				rmd_file.write(w)
				for subitem in connections_json[item]:
					w = self.sanitizeUnderscores(str(subitem)) + " : " + self.sanitizeUnderscores(str(connections_json[item][subitem])) + "\n\n"
					rmd_file.write(w)

			# getting media data
			with open("media.json", "r", errors = "replace") as media:
				media_content = media.read()
				media.close()
			media_json = json.loads(media_content)
			rmd_file.write("# Media \n\n")
			direct_counter = 0
			for media_type in media_json:
				w = "## " + self.sanitizeUnderscores(str(media_type)) + "\n\n"
				rmd_file.write(w)
				for item in media_json[str(media_type)]:
					if media_type != "direct":
						p = str(item["path"])
						file_ending = p.split(".")[-1]
						if file_ending == "mp4":
							pp = "\n\n path\\_to\\_video : " + str(item["path"]) + "\n\n*****\n\n"
						else:
							pp = "\n\n![" + self.san(str(item["caption"])) + "](" + str(item["path"]) + ")\n\n*****\n\n"
						w = "\n\ncaption : " + self.san(str(item["caption"])) + "\n\ntaken\\_at : " + self.sanitizeUnderscores(str(item["taken_at"])) + pp
					elif media_type == "direct":
						direct_counter = direct_counter + 1
						w = "\n\ncaption : direct" + str(direct_counter) + "\n\ntaken\\_at : " + self.sanitizeUnderscores(str(item["taken_at"])) + "\n\n![" + "direct\\_picture" + str(direct_counter) + "](" + str(item["path"]) + ")\n\n*****\n\n"
					else:
						pass
					rmd_file.write(w)

			# getting comments
			with open("comments.json", "r", errors="replace") as comments:
				comments_content = comments.read()
				comments.close()
			comments_json = json.loads(comments_content)
			rmd_file.write("# Comments \n\n")
			for comment_type in comments_json:
				w = "## " + self.sanitizeUnderscores(str(comment_type)) + "\n\n"
				rmd_file.write(w)
				for item in comments_json[str(comment_type)]:
					w = "\n\n recipient : " + self.sanitizeUnderscores(str(item[2])) + "\n\n comment : " + self.san(str(item[1])) + "\n\n time : " + str(item[0]) + "\n\n*****\n\n"
					rmd_file.write(w)

			# getting messages
			with open("messages.json", "r", errors="replace") as messages:
				messages_content = messages.read()
				messages.close()
			messages_json = json.loads(messages_content)
			rmd_file.write("# Messages\n\n")
			for conversations in messages_json:
				participants = conversations["participants"]
				conversation = conversations["conversation"]
				conv_title = "## "
				for name in participants:
					conv_title = conv_title + self.sanitizeUnderscores(str(name)) + ","
				conv_title2 = conv_title.rstrip(",") + "\n\n"
				rmd_file.write(conv_title2)
				for message in conversation:
					for item in message:
						w = self.san(str(item)) + " : " + self.san(str(message[item])) + "\n\n"
						rmd_file.write(w)
					rmd_file.write("\\_\\_\\_\\_\\_\n\n")

			# credits
			w = "# Credits\n\nThis document was created using Micha Birklbauer's [Instagram Data Download Viewer](https://github.com/t0xic-m/instagram_data_download_viewer)."
			rmd_file.write(w)

			rmd_file.close()

		# try knitting to pdf
		self.RMDtoPDF()

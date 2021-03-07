#!/usr/bin/env python3

import urllib.request as ur
import urllib.parse as up
from lxml import html
import tkinter as tk
from tkinter import scrolledtext as st
from tkinter import filedialog
import platform
import webbrowser
import datetime
import requests
import json
import time
import sys
import os

class Instagram:

	def __init__(self):
		pass

	def getUserID(self, user_name):
		url = "https://www.instagram.com/" + str(user_name)
		page = ur.urlopen(url).read().decode("utf-8")
		lines = page.splitlines()

		data = ""
		user_id = 0

		for line in lines:
			if "window._sharedData = " in line:
				data = line.replace("window._sharedData = ", "").replace("<script type=\"text/javascript\">", "").replace(";</script>", "").lstrip().rstrip()

		if data != "":
			jdata = json.loads(data)
			try:
				user_id = jdata["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]
			except:
				pass

		if user_id != 0:
			return int(user_id)
		else:
			print("It seems retrieving the user ID was unsuccessful!")
			return 1

	def getUserName(self, user_id):
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		user_name = json.loads(user_info)["user"]["username"]
		return str(user_name)

	def getMediaCount(self, user_id):
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		media_count = json.loads(user_info)["user"]["media_count"]
		return int(media_count)

	def getProfilePic(self, user_id, download = False):
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		profile_pic_url = json.loads(user_info)["user"]["hd_profile_pic_url_info"]["url"]
		if download:
			s_path = "" + str(profile_pic_url).split("/")[-1].split("?")[0]
			ur.urlretrieve(str(profile_pic_url), s_path)
		return str(profile_pic_url)

	def getNewPost(self, user_id, download = False):

		user_name = self.getUserName(user_id)

		url = "https://www.instagram.com/" + str(user_name)
		page = ur.urlopen(url).read().decode("utf-8")
		lines = page.splitlines()

		data = ""
		shortcode = ""

		for line in lines:
			if "window._sharedData = " in line:
				data = line.replace("window._sharedData = ", "").replace("<script type=\"text/javascript\">", "").replace(";</script>", "").lstrip().rstrip()

		if data != "":
			jdata = json.loads(data)
			try:
				shortcode = jdata["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]
			except:
				pass

		if shortcode != "":
			post_page = "https://instagram.com/p/" + shortcode
			if download:
				post_pics = self.getMedia(post_page, True)
			else:
				post_pics = self.getMedia(post_page)
			post_details = [post_page]+post_pics
			return post_details
		else:
			return ["Error in retrieving new Post", str(shortcode), str(data)]

	def getNewIGTV(self, user_id, download = False):

		user_name = self.getUserName(user_id)

		url = "https://www.instagram.com/" + str(user_name)
		page = ur.urlopen(url).read().decode("utf-8")
		lines = page.splitlines()

		data = ""
		count = ""
		shortcode = ""

		for line in lines:
			if "window._sharedData = " in line:
				data = line.replace("window._sharedData = ", "").replace("<script type=\"text/javascript\">", "").replace(";</script>", "").lstrip().rstrip()

		if data != "":
			jdata = json.loads(data)
			try:
				count = jdata["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_felix_video_timeline"]["count"]
				shortcode = jdata["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_felix_video_timeline"]["edges"][0]["node"]["shortcode"]
			except:
				pass

		if count != "" and shortcode != "":
			post_page = "https://instagram.com/p/" + shortcode
			igtv_nr = "Number of IGTV posts: " + str(count)
			if download:
				post_pics = self.getMedia(post_page, True)
			else:
				post_pics = self.getMedia(post_page)
			post_details = [igtv_nr]+[post_page]+post_pics
			return post_details
		else:
			return ["Error in retrieving newest IGTV Post", str(count), str(shortcode), str(data)]

	def getTagged(self, user_id):

		user_name = self.getUserName(user_id)

		tagged_page = "https://instagram.com/" + user_name + "/tagged/"
		return tagged_page

	def isPrivate(self, instagram_post_url):
		url = str(link)
		shortcode = str(url.split("instagram.com/p/")[1]).split("/")[0]
		if len(shortcode) > 12:
			return True
		else:
			return False

	def isProfilePrivate(self, user_id):
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		is_private = json.loads(user_info)["user"]["is_private"]
		return is_private

	def getPostDetails(self, instagram_post_url):

		shortcode = instagram_post_url.split("/p/")[1].split("/")[0]
		url = "https://instagram.com/p/" + shortcode + "/?__a=1"

		post_data = ur.urlopen(url).read()
		post_json = json.loads(post_data)

		return [url, post_data, post_json]

	def getMedia(self, instagram_post_url, download = False):

		page = requests.get(instagram_post_url)
		tree = html.fromstring(page.content)
		data = tree.xpath('//body/script[@type="text/javascript"]')

		json_unprocessed = data[0].text_content()
		json_processed = str(json_unprocessed).replace("window._sharedData = ", "").rstrip(";")
		json_data = json.loads(json_processed)

		media_links = []

		if str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphImage":
			image = tree.xpath('//meta[@property="og:image"]/@content')
			media_links.append(str(image[0]))
			if download:
				s_path = "" + str(image[0]).split("/")[-1].split("?")[0]
				ur.urlretrieve(str(image[0]), s_path)
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphVideo":
			video = tree.xpath('//meta[@property="og:video:secure_url"]/@content')
			media_links.append(str(video[0]))
			if download:
				s_path = "" + str(video[0]).split("/")[-1].split("?")[0]
				ur.urlretrieve(str(video[0]), s_path)
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphSidecar":
			prefix = str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["shortcode"])
			edges = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
			for edge in edges:
				if edge["node"]["is_video"]:
					url = str(edge["node"]["video_url"])
					media_links.append(url)
					if download:
						s_path = "" + prefix+"_"+(url.split("/")[-1].split("?")[0])
						ur.urlretrieve(url, s_path)
				else:
					url = str(edge["node"]["display_url"])
					media_links.append(url)
					if download:
						s_path = "" + prefix+"_"+(url.split("/")[-1].split("?")[0])
						ur.urlretrieve(url, s_path)
		else:
			#print("Unrecognized typename!")
			pass

		return media_links

		def getMediaSafe(self, instagram_post_url, download = False):
			if self.isPrivate(instagram_post_url):
				print("Post might be private!")
				try:
					media = self.getMedia(instagram_post_url, download)
					return media
				except:
					print("Oops! Seems like something went wrong! Try manual download!")
					return 1
			else:
				try:
					media = self.getMedia(instagram_post_url, download)
					return media
				except:
					print("Oops! Seems like something went wrong! Try manual download!")
					return 1

	def getStories(self, user_id, download = False):

		user_name = self.getUserName(user_id)

		url = "https://storiesig.com/stories/" + str(user_name)
		page = ur.urlopen(url).read().decode("utf-8")
		lines = page.splitlines()

		data = ""

		media_links = []

		for line in lines:
			if "__NEXT_DATA__" in line:
				data = line.replace("__NEXT_DATA__ = ", "").lstrip().rstrip()

		if data != "":
			jdata = json.loads(data)
			stories = jdata["props"]["pageProps"]["stories"]["items"]
			if len(stories) == 0:
				return media_links
			else:
				for story in stories:
					original_width = story["original_width"]
					original_height = story["original_height"]
					media_type = int(story["media_type"])
					for entry in story["image_versions2"]["candidates"]:
						if entry["width"] == original_width and entry["height"] == original_height:
							media_links.append(str(entry["url"]))
							if download:
								s_path = "" + str(entry["url"]).split("/")[-1].split("?")[0]
								ur.urlretrieve(str(entry["url"]), s_path)
					max_height = 0
					max_counter = 0
					i = 0
					if media_type == 2:
						for entry in story["video_versions"]:
							if int(entry["height"]) >= max_height:
								max_height = int(entry["height"])
								max_counter = i
							i = i + 1
						media_links.append(str(story["video_versions"][max_counter]["url"]))
						if download:
							s_path = "" + str(story["video_versions"][max_counter]["url"]).split("/")[-1].split("?")[0]
							ur.urlretrieve(str(story["video_versions"][max_counter]["url"]), s_path)

				return media_links

class InstaLoad:

	def __init__(self):
		pass

	def instaload(self, insta_url):
		page = requests.get(insta_url)
		tree = html.fromstring(page.content)
		data = tree.xpath('//body/script[@type="text/javascript"]')

		json_unprocessed = data[0].text_content()
		json_processed = str(json_unprocessed).replace("window._sharedData = ", "").rstrip(";")
		json_data = json.loads(json_processed)

		if str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphImage":
			image = tree.xpath('//meta[@property="og:image"]/@content')
			try:
				ur.urlretrieve(str(image[0]), str(image[0]).split("/")[-1].split("?")[0])
				return 0
			except:
				error_msg = "Error in link: " + insta_url
				print(error_msg)
				return 1
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphVideo":
			video = tree.xpath('//meta[@property="og:video:secure_url"]/@content')
			try:
				ur.urlretrieve(str(video[0]), str(video[0]).split("/")[-1].split("?")[0])
				return 0
			except:
				error_msg = "Error in link: " + insta_url
				print(error_msg)
				return 1
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphSidecar":
			prefix = str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["shortcode"])
			edges = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
			for edge in edges:
				if edge["node"]["is_video"]:
					url = str(edge["node"]["video_url"])
					try:
						ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1].split("?")[0]))
						return 0
					except:
						error_msg = "Error in link: " + insta_url
						print(error_msg)
						return 1
				else:
					url = str(edge["node"]["display_url"])
					try:
						ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1].split("?")[0]))
						return 0
					except:
						error_msg = "Error in link: " + insta_url
						print(error_msg)
						return 1
		else:
			print("Unrecognized typename!")
			return 1

	def is_private(self, link):
		url = str(link)
		shortcode = str(url.split("instagram.com/p/")[1]).split("/")[0]
		if len(shortcode) > 12:
			return True
		else:
			return False

	def multiload(self, file_name):
		multiload_warnings = 0
		multiload_errors = 0
		if os.path.isfile(file_name):
			with open(file_name, "r") as in_file:
				lines = in_file.readlines()
				in_file.close()
			count = int(len(lines))
			counter = 1
			percent = ["[--------------------]", "[#-------------------]", "[##------------------]", "[###-----------------]", "[####----------------]", "[#####---------------]", "[######--------------]", "[#######-------------]", "[########------------]", "[#########-----------]", "[##########----------]", "[###########---------]", "[############--------]", "[#############-------]", "[##############------]", "[###############-----]", "[################----]", "[#################---]", "[##################--]", "[###################-]", "[####################]"]
			for line in lines:
				l = line.lstrip().rstrip()
				if self.is_private(l):
					multiload_warnings = multiload_warnings + 1
					print("It appears your link list also contains links to private posts, script will try to download anyway but manually checking is advised! Private links will be filtered and appended to private.txt!")
					try:
						self.instaload(l)
					except:
						pass
					with open("private.txt", "a") as p_file:
						p_file.write(l+"\n")
						p_file.close()
				else:
					multiload_result = self.instaload(l)
				if multiload_result == 0:
					pass
				else:
					multiload_errors = multiload_errors + 1
				status = counter/count
				status_bar = ""
				if status == 1:
					status_bar = percent[20]
				elif status > 0.95:
					status_bar = percent[19]
				elif status > 0.9:
					status_bar = percent[18]
				elif status > 0.85:
					status_bar = percent[17]
				elif status > 0.8:
					status_bar = percent[16]
				elif status > 0.75:
					status_bar = percent[15]
				elif status > 0.7:
					status_bar = percent[14]
				elif status > 0.65:
					status_bar = percent[13]
				elif status > 0.6:
					status_bar = percent[12]
				elif status > 0.55:
					status_bar = percent[11]
				elif status > 0.5:
					status_bar = percent[10]
				elif status > 0.45:
					status_bar = percent[9]
				elif status > 0.4:
					status_bar = percent[8]
				elif status > 0.35:
					status_bar = percent[7]
				elif status > 0.3:
					status_bar = percent[6]
				elif status > 0.25:
					status_bar = percent[5]
				elif status > 0.2:
					status_bar = percent[4]
				elif status > 0.15:
					status_bar = percent[3]
				elif status > 0.1:
					status_bar = percent[2]
				elif status > 0.05:
					status_bar = percent[1]
				else:
					status_bar = percent[0]
				status_msg = "Downloaded " + str(line) + "\nDownload at " + str(status*100) + "%\n" + status_bar + "\n"
				counter = counter + 1
				print(status_msg)
			w = "Warnings: " + str(multiload_warnings) + "\n"
			e = "Errors: " + str(multiload_errors) + "\n"
			print("Download completed!\n")
			print(w)
			print(e)
		else:
			print("File doesn't exist! Please provide a valid filename/path to file!")

class InstaBot:

	instagram = Instagram()

	def __init__(self, path_to_config_file, channel, api_token):
		self.path_to_config_file = path_to_config_file
		self.channel = channel
		self.api_token = api_token

	def getUserName(self, user_id):
		time.sleep(5)
		url = url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		user_name = json.loads(user_info)["user"]["username"]
		return str(user_name)

	def getMediaCount(self, user_id):
		time.sleep(5)
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		media_count = json.loads(user_info)["user"]["media_count"]
		return int(media_count)

	def getProfilePic(self, user_id):
		time.sleep(5)
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		profile_pic_url = json.loads(user_info)["user"]["hd_profile_pic_url_info"]["url"]
		return str(profile_pic_url)

	def sendMessage(self, text):
		r = ur.urlopen("https://api.telegram.org/bot"+self.api_token+"/sendMessage?", up.urlencode({"chat_id": self.channel, "text": text}).encode("utf-8")).read()
		print(r)
		return

	def getNewPost(self, user_id):
		return instagram.getNewPost(user_id)

	def getStories(self, user_ids):
		self.sendMessage("Today's Stories:")
		time.sleep(5)
		for user_id in user_ids:
			try:
				stories = instagram.getStories(user_id)
			except:
				stories = ["Error in retrieving Story"]
			for item in stories:
				self.sendMessage(str(item))
			time.sleep(5)

	def createConfig(self, user_ids):

		users_media_counts = []
		users_profile_pics = []

		for user_id in user_ids:
			users_media_counts.append(self.getMediaCount(user_id))
			users_profile_pics.append(self.getProfilePic(user_id))

		config_f = open(self.path_to_config_file, "w")
		string_to_write = ""
		for mc in users_media_counts:
			string_to_write = string_to_write + str(mc) + "\n"
		p = 0
		for pb in users_profile_pics:
			if p < len(users_profile_pics)-1:
				string_to_write = string_to_write + str(pb) + "\n"
			else:
				string_to_write = string_to_write + str(pb)
		config_f.write(string_to_write)
		config_f.close()

	def writeConfig(self, users_media_counts, users_profile_pics):

		config_f = open(self.path_to_config_file, "w")
		string_to_write = ""
		for mc in users_media_counts:
			string_to_write = string_to_write + str(mc) + "\n"
		p = 0
		for pb in users_profile_pics:
			if p < len(users_profile_pics)-1:
				string_to_write = string_to_write + str(pb) + "\n"
			else:
				string_to_write = string_to_write + str(pb)
		config_f.write(string_to_write)
		config_f.close()

	def instaBot(self, user_ids, rtime = 3480, stime = 21, daily = False, debugging_mode = True):

		if debugging_mode:
			self.sendMessage("InstaPython process was launched!")

		user_names = []
		user_names_string = ""
		for user_id in user_ids:
			user_names.append(self.getUserName(user_id))
			user_names_string = user_names_string + self.getUserName(user_id) + "; "

		print("InstaBot initiated with usernames: ", user_names)
		if debugging_mode:
			init_message = "InstaBot initiated with usernames: " + user_names_string.rstrip("; ")
			self.sendMessage(init_message)

		if os.path.isfile(self.path_to_config_file):
			print("Found existing configuration file!")
			if debugging_mode:
				self.sendMessage("Found existing configuration file!")
		else:
			self.createConfig(user_ids)
			print("Created configuration file at: ", self.path_to_config_file)
			if debugging_mode:
				self.sendMessage("Created configuration file!")

		config_f = open(self.path_to_config_file, "r")
		config = config_f.read().splitlines()
		config_f.close()

		users_media_counts = config[:int(len(config)/2)]
		users_profile_pics = config[int(len(config)/2):]

		if rtime != 0:
			rep = 1
			while rep < rtime:
				rep = rep + 60
				time.sleep(60)
				for i in range(len(user_ids)):
					rep = rep + 5
					new_media_count = self.getMediaCount(user_ids[i])
					if new_media_count > int(users_media_counts[i]):
						users_media_counts[i] = new_media_count
						rep = rep + 5
						new_post = self.getNewPost(user_ids[i])
						text = "User "+str(self.getUserName(user_ids[i]))+" posted something new: "+new_post[0]+" ;"
						self.sendMessage(text)
						for item in new_post[1:]:
							text = "Raw image can be found here: "+item+" ;"
							self.sendMessage(text)
						text = "Link to profile: https://instagram.com/"+str(self.getUserName(user_ids[i]))
						self.sendMessage(text)
						self.writeConfig(users_media_counts, users_profile_pics)
					rep = rep + 5
					new_profile_pic_url = self.getProfilePic(user_ids[i])
					if new_profile_pic_url != users_profile_pics[i]:
						users_profile_pics[i] = new_profile_pic_url
						text = "User "+str(self.getUserName(user_ids[i]))+" has a new profile pic: "+str(new_profile_pic_url)+" ;"
						self.sendMessage(text)
						self.writeConfig(users_media_counts, users_profile_pics)
				if daily:
					if datetime.datetime.now().time().hour == stime and datetime.datetime.now().time().minute == 0:
						self.getStories(user_ids)
				else:
					if stime > 12:
						stime1 = stime-12
						stime2 = stime
					else:
						stime1 = stime
						stime2 = stime+12
					if datetime.datetime.now().time().hour == stime1 and datetime.datetime.now().time().minute == 0:
						self.getStories(user_ids)
					if datetime.datetime.now().time().hour == stime2 and datetime.datetime.now().time().minute == 0:
						self.getStories(user_ids)

			self.getStories(user_ids)
			print("Done! Restart?")
		else:
			start_message = "InstaBot started with usernames: " + user_names_string.rstrip("; ")
			self.sendMessage(start_message)
			try:
				while True:
					time.sleep(60)
					for i in range(len(user_ids)):
						new_media_count = self.getMediaCount(user_ids[i])
						if new_media_count > int(users_media_counts[i]):
							users_media_counts[i] = new_media_count
							new_post = self.getNewPost(user_ids[i])
							text = "User "+str(self.getUserName(user_ids[i]))+" posted something new: "+new_post[0]+" ;"
							self.sendMessage(text)
							for item in new_post[1:]:
								text = "Raw image can be found here: "+item+" ;"
								self.sendMessage(text)
							text = "Link to profile: https://instagram.com/"+str(self.getUserName(user_ids[i]))
							self.sendMessage(text)
							self.writeConfig(users_media_counts, users_profile_pics)
						new_profile_pic_url = self.getProfilePic(user_ids[i])
						if new_profile_pic_url != users_profile_pics[i]:
							users_profile_pics[i] = new_profile_pic_url
							text = "User "+str(self.getUserName(user_ids[i]))+" has a new profile pic: "+str(new_profile_pic_url)+" ;"
							self.sendMessage(text)
							self.writeConfig(users_media_counts, users_profile_pics)
					if daily:
						if datetime.datetime.now().time().hour == stime and datetime.datetime.now().time().minute == 0:
							self.getStories(user_ids)
					else:
						if stime > 12:
							stime1 = stime-12
							stime2 = stime
						else:
							stime1 = stime
							stime2 = stime+12
						if datetime.datetime.now().time().hour == stime1 and datetime.datetime.now().time().minute == 0:
							self.getStories(user_ids)
						if datetime.datetime.now().time().hour == stime2 and datetime.datetime.now().time().minute == 0:
							self.getStories(user_ids)
			except KeyboardInterrupt:
				try:
					self.writeConfig(users_media_counts, users_profile_pics)
				except:
					pass

				print("Exiting!")
		return

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
			w = "# Credits\n\nThis document was created using Micha Birklbauer's [Instagram JSON Viewer](https://github.com/michabirklbauer/instagram_json_viewer)."
			rmd_file.write(w)

			rmd_file.close()

		# try knitting to pdf
		self.RMDtoPDF()

class InstaPythonApp:

	instagram = Instagram()
	result = []

	def __init__(self, master):
		self.master = master
		master.title("InstaPython App by Micha Birklbauer")

		# header
		mainFrame = tk.Label(master, text="\n\nInstaPython-App by Micha Birklbauer\n\n")
		mainFrame.grid(row=0, column=0, columnspan=7)
		# desc1
		desc1Frame = tk.Label(master, text="Enter a Username:", width=100, height=3)
		desc1Frame.grid(row=1, column=0, columnspan=7)
		# username
		self.username = tk.Entry(master, width=100)
		self.username.grid(row=2, column=0, columnspan=7)
		# get userid
		get_userid_button = tk.Button(master, text="Get User ID!", width=15, command=self.get_user_id)
		get_userid_button.grid(row=3, column=1)
		# desc2
		desc2Frame = tk.Label(master, text="Enter a User ID:", width=100, height=3)
		desc2Frame.grid(row=4, column=0, columnspan=7)
		# user id
		self.userid = tk.Entry(master, width=100)
		self.userid.grid(row=5, column=0, columnspan=7)
		# get username
		get_username_button = tk.Button(master, text="Get Username!", width=15, command=self.get_username)
		get_username_button.grid(row=6, column=1)
		# get media count
		get_media_count_button = tk.Button(master, text="Get #Media!", width=15, command=self.get_mediacount)
		get_media_count_button.grid(row=6, column=2)
		# get profile picture
		get_profile_pic_button = tk.Button(master, text="Get Profile Pic!", width=15, command=self.get_profilepic)
		get_profile_pic_button.grid(row=6, column=3)
		# get new post
		get_new_post_button = tk.Button(master, text="Get New Post!", width=15, command=self.get_newpost)
		get_new_post_button.grid(row=6, column=4)
		# get story
		get_story_button = tk.Button(master, text="Get Stories!", width=15, command=self.get_stories)
		get_story_button.grid(row=6, column=5)
		# get privacy setting
		get_privacy_button = tk.Button(master, text="Private?", width=15, command=self.get_privacy)
		get_privacy_button.grid(row=7, column=2)
		# download profile picture
		dl_profile_picture_button = tk.Button(master, text="DL Profile Pic!", width=15, command=self.dl_profilepic)
		dl_profile_picture_button.grid(row=7, column=3)
		# download new post
		dl_new_post_button = tk.Button(master, text="DL New Post!", width=15, command=self.dl_newpost)
		dl_new_post_button.grid(row=7, column=4)
		# download stories
		dl_story_button = tk.Button(master, text="DL Stories!", width=15, command=self.dl_stories)
		dl_story_button.grid(row=7, column=5)
		# get new igtv post
		get_igtv_button = tk.Button(master, text="Get New IGTV!", width=15, command=self.get_newigtv)
		get_igtv_button.grid(row=8, column=3)
		# dl new igtv post
		dl_igtv_button = tk.Button(master, text="DL New IGTV!", width=15, command=self.dl_newigtv)
		dl_igtv_button.grid(row=8, column=4)
		# get new tagged post
		get_tagged_button = tk.Button(master, text="Get Tagged Page!", width=15, command=self.get_tagged)
		get_tagged_button.grid(row=8, column=5)
		# desc3
		desc3Frame = tk.Label(master, text="Enter an URL to download Post Media:", width=100, height=3)
		desc3Frame.grid(row=9, column=0, columnspan=7)
		# url
		self.url = tk.Entry(master, width=100)
		self.url.grid(row=10, column=0, columnspan=7)
		# get post details
		get_post_details_button = tk.Button(master, text="Get Details!", width=15, command=self.get_postdetails)
		get_post_details_button.grid(row=11, column=1)
		# get url / download post media
		dl_post_media_button = tk.Button(master, text="Download!", width=15, command=self.dl_postmedia)
		dl_post_media_button.grid(row=11, column=2)
		# download multiple posts
		dl_multi_media_button = tk.Button(master, text="Multi-Download!", width=15, command=self.dl_multimedia)
		dl_multi_media_button.grid(row=11, column=3)
		# output desc
		desc4Frame = tk.Label(master, text="Output:", width=100, height=3)
		desc4Frame.grid(row=12, column=0, columnspan=7)
		# output
		self.output = st.ScrolledText(self.master, width=80, height=10, state=tk.NORMAL)
		self.output.grid(row=13, column=0, columnspan=7)
		self.output.config(state=tk.DISABLED)
		self.output.see('end')
		# options / instabot and Instaview
		b_open_button = tk.Button(master, text="Open in Browser!", width=15, command=self.open_browser)
		instabot_button = tk.Button(master, text="InstaBot", width=15, command=self.instabot)
		instaview_button = tk.Button(master, text="InstaView", width=15, command=self.instaview)
		help_button = tk.Button(master, text="Help", width=15, command=self.help)
		credits_button = tk.Button(master, text="Credits", width=15, command=self.credits)
		b_open_button.grid(row=14, column=1)
		instabot_button.grid(row=14, column=2)
		instaview_button.grid(row=14, column=3)
		help_button.grid(row=14, column=4)
		credits_button.grid(row=14, column=5)

	def get_user_id(self):
		f_username = self.username.get()
		f_userid = self.instagram.getUserID(f_username)
		f_query = "Query: Get User ID for '" + str(f_username) + "'\n"
		f_output = "Output: " + str(f_userid) + "\n"
		self.userid.delete(0, 'end')
		self.userid.insert(0, f_userid)
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')


	def get_username(self):
		f_userid = self.userid.get()
		f_username = self.instagram.getUserName(f_userid)
		f_query = "Query: Get Username for ID '" + str(f_userid) + "'\n"
		f_output = "Output: " + str(f_username) + "\n"
		self.username.delete(0, 'end')
		self.username.insert(0, f_username)
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def get_mediacount(self):
		f_userid = self.userid.get()
		f_media_count = self.instagram.getMediaCount(f_userid)
		f_query = "Query: Get Media Count for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = "Output: " + str(f_media_count) + "\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def get_profilepic(self):
		f_userid = self.userid.get()
		f_profile_pic = self.instagram.getProfilePic(f_userid)
		self.result = [f_profile_pic]
		f_query = "Query: Get Profile Picture for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = "Output: " + str(f_profile_pic) + "\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def get_newpost(self):
		f_userid = self.userid.get()
		f_new_post = self.instagram.getNewPost(f_userid)
		self.result = f_new_post
		f_query = "Query: Get newest Post for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = ""
		for item in f_new_post:
			f_output = f_output + "Output: " + str(item) + "\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def get_newigtv(self):
		f_userid = self.userid.get()
		f_new_post = self.instagram.getNewIGTV(f_userid)
		self.result = f_new_post[1:]
		f_query = "Query: Get newest IGTV Post for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = ""
		for item in f_new_post:
			f_output = f_output + "Output: " + str(item) + "\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def get_tagged(self):
		f_userid = self.userid.get()
		f_tagged = self.instagram.getTagged(f_userid)
		self.result = [f_tagged]
		f_query = "Query: Get Tagged Page for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = "Output: " + str(f_tagged) + "\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def get_stories(self):
		f_userid = self.userid.get()
		f_stories = self.instagram.getStories(f_userid)
		self.result = f_stories
		f_query = "Query: Get Stories for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = ""
		for item in f_stories:
			f_output = f_output + "Output: " + str(item) + "\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def get_privacy(self):
		f_userid = self.userid.get()
		f_privacy = self.instagram.isProfilePrivate(f_userid)
		f_query = "Query: Get Privacy Setting for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		if f_privacy:
			f_output = "Output: This profile is private!\n"
		else:
			f_output = "Output: This profile is public!\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def dl_profilepic(self):
		f_userid = self.userid.get()
		f_profile_pic = self.instagram.getProfilePic(f_userid, download=True)
		self.result = [f_profile_pic]
		f_query = "Query: Download Profile Picture for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = "Output: " + str(f_profile_pic) + "\nOutput: Download finished!\nOutput: File in directory: '.'\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def dl_newpost(self):
		f_userid = self.userid.get()
		f_new_post = self.instagram.getNewPost(f_userid, download=True)
		self.result = f_new_post
		f_query = "Query: Download newest Post for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = ""
		for item in f_new_post:
			f_output = f_output + "Output: " + str(item) + "\n"
		f_output = f_output + "Output: Download finished!\nOutput: File in directory: '.'\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def dl_newigtv(self):
		f_userid = self.userid.get()
		f_new_post = self.instagram.getNewIGTV(f_userid, download=True)
		self.result = f_new_post[1:]
		f_query = "Query: Download newest IGTV Post for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = ""
		for item in f_new_post:
			f_output = f_output + "Output: " + str(item) + "\n"
		f_output = f_output + "Output: Download finished!\nOutput: File in directory: '.'\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def dl_stories(self):
		f_userid = self.userid.get()
		f_stories = self.instagram.getStories(f_userid, download=True)
		self.result = f_stories
		f_query = "Query: Get Stories for ID '" + str(f_userid) + "' (" + str(self.instagram.getUserName(f_userid)) + ")\n"
		f_output = ""
		for item in f_stories:
			f_output = f_output + "Output: " + str(item) + "\n"
		f_output = f_output + "Output: Download finished!\nOutput: File in directory: '.'\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def get_postdetails(self):
		f_url = self.url.get()
		f_details = self.instagram.getPostDetails(f_url)
		self.result = [f_details[0]]
		f_query = "Query: Get Post Details for Post '" + str(f_url) + "'\n"
		f_output = "Output: " + str(f_details[0]) + "\nOutput: " + str(f_details[1]) + "\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def dl_multimedia(self):
		f_url = filedialog.askopenfilename()
		instaload = InstaLoad()
		f_query = "Query: InstaLoad - Multi\n"
		f_output = "Output: Please see the terminal for Output!\nOutput: Press Ctrl + C to cancel!\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')
		self.master.update_idletasks()
		instaload.multiload(f_url)

	def dl_postmedia(self):
		f_url = self.url.get()
		f_postmedia = self.instagram.getMedia(f_url, download=True)
		self.result = f_postmedia
		f_query = "Query: Download Post Media for Post '" + str(f_url) + "'\n"
		f_output = ""
		for item in f_postmedia:
			f_output = f_output + "Output: " + str(item) + "\n"
		f_output = f_output + "Output: Download finished!\nOutput: File in directory: '.'\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')

	def instabot(self):
		f_query = "Query: InstaBot\n"
		f_output = "Output: Please follow the instructions in the terminal!\nOutput: Press Ctrl + C to cancel!\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')
		self.master.update_idletasks()
		channel = input("Enter a Telegram channel in the form of ID (number) or @channelname:\n")
		api_token = input("Enter a Telegram bot API token:\n")
		rtime = input("Enter how long the bot should run in seconds (0 if bot should run infinitely):\n")
		stime = input("Enter the hour when story notifications should be sent:\n")
		daily = input("Enter if story notifications should be sent in a 12 hour interval: True/False\n")
		debugging_mode = input("Enter if debugging mode should be activated: True/False\n")
		user_ids = []
		while True:
			user_id = input("Enter a user ID:\n")
			user_ids.append(user_id)
			confirm = input("Do you want to add another user ID? Yes/No\n")
			if str(confirm) in ["no", "No", "NO", "n", "0"]:
				break
		i = InstaBot("instabot.cfg", channel, api_token)
		if debugging_mode == "True":
			if daily == "True":
				i.instaBot(user_ids, rtime, stime, False, True)
			else:
				i.instaBot(user_ids, rtime, stime, True, True)
		else:
			if daily == "True":
				i.instaBot(user_ids, rtime, stime, False, False)
			else:
				i.instaBot(user_ids, rtime, stime, True, False)

	def instaview(self):
		f_query = "Query: InstaView\n"
		f_output = "Output: Please follow the instructions in the terminal!\nOutput: Press Ctrl + C to cancel!\n"
		self.output.config(state=tk.NORMAL)
		self.output.insert("end", f_query, 'query')
		self.output.insert("end", f_output, 'output')
		self.output.config(state=tk.DISABLED)
		self.output.tag_config('query', foreground='green')
		self.output.tag_config('output', foreground='red')
		self.output.see('end')
		self.master.update_idletasks()
		path = input("Enter the absolute path to your data directory:\n")
		i = InstaView()
		i.createRMD(path)
		print("RMD creation successful! Created at //your_path/instaview.Rmd!")

	def help(self):
		#webbrowser.open("bin/help/help.html")
		webbrowser.open("https://htmlpreview.github.io/?https://github.com/michabirklbauer/instapython/blob/master/resources/help.html")

	def credits(self):
		webbrowser.open("https://raw.githubusercontent.com/michabirklbauer/instapython-app/master/LICENSE.md")

	def open_browser(self):
		for item in self.result:
			webbrowser.open(item)

name = "InstaPython"

def gui():
	root = tk.Tk()
	app = InstaPythonApp(root)
	root.mainloop()

#!/usr/bin/env python3

from lxml import html
import urllib.request as ur
import requests
import json

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

	def getProfilePic(self, user_id):
		url = "https://i.instagram.com/api/v1/users/"+str(user_id)+"/info/"
		user_info = ur.urlopen(url).read()
		profile_pic_url = json.loads(user_info)["user"]["hd_profile_pic_url_info"]["url"]
		return str(profile_pic_url)

	def getNewPost(self, user_id):
		user_name = self.getUserName(user_id)
		url = "https://instagram.com/"+str(user_name)+"/"
		user_profile = ur.urlopen(url).read()
		post_page = "https://instagram.com/p/"+str(str(user_profile).split("shortcode")[1].split("\"")[2])
		post_media = self.getMedia(post_page)
		return [post_page] + [post_media]

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
				ur.urlretrieve(str(image[0]), str(image[0]).split("/")[-1].split("?")[0])
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphVideo":
			video = tree.xpath('//meta[@property="og:video:secure_url"]/@content')
			media_links.append(str(video[0]))
			if download:
				ur.urlretrieve(str(video[0]), str(video[0]).split("/")[-1].split("?")[0])
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphSidecar":
			prefix = str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["shortcode"])
			edges = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
			for edge in edges:
				if edge["node"]["is_video"]:
					url = str(edge["node"]["video_url"])
					media_links.append(url)
					if download:
						ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1].split("?")[0]))
				else:
					url = str(edge["node"]["display_url"])
					media_links.append(url)
					if download:
						ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1].split("?")[0]))
		else:
			print("Unrecognized typename!")

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
								ur.urlretrieve(str(entry["url"]), str(entry["url"]).split("/")[-1].split("?")[0])
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
							ur.urlretrieve(str(story["video_versions"][max_counter]["url"]), str(story["video_versions"][max_counter]["url"]).split("/")[-1].split("?")[0])

				return media_links

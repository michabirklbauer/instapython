#!/usr/bin/env python3

from lxml import html
import urllib.request as ur
import requests
import json

class InstaLoad:

	def __init__(self):
		pass

	def instaload(self, instagram_post_url):

		page = requests.get(instagram_post_url)
		tree = html.fromstring(page.content)
		data = tree.xpath('//body/script[@type="text/javascript"]')

		json_unprocessed = data[0].text_content()
		json_processed = str(json_unprocessed).replace("window._sharedData = ", "").rstrip(";")
		json_data = json.loads(json_processed)

		if str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphImage":
			image = tree.xpath('//meta[@property="og:image"]/@content')
			ur.urlretrieve(str(image[0]), str(image[0]).split("/")[-1])
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphVideo":
			video = tree.xpath('//meta[@property="og:video:secure_url"]/@content')
			ur.urlretrieve(str(video[0]), str(video[0]).split("/")[-1])
		elif str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]) == "GraphSidecar":
			prefix = str(json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["shortcode"])
			edges = json_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
			for edge in edges:
				if edge["node"]["is_video"]:
					url = str(edge["node"]["video_url"])
					ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1]))
				else:
					url = str(edge["node"]["display_url"])
					ur.urlretrieve(url, prefix+"_"+(url.split("/")[-1]))
		else:
			print("Unrecognized typename!")

	def isPrivate(self, instagram_post_url):
		url = str(instagram_post_url)
		shortcode = str(url.split("instagram.com/p/")[1]).split("/")[0]
		if len(shortcode) > 12:
			return True
		else:
			return False

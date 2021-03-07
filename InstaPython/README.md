# InstaPython

A small python package to access and deal with Instagram data.

## WARNING

**\[10.12.2018\] Since Instagram deprecated their public API this package will not be maintained anymore. Programs/Scripts or parts of them will not work properly anymore! USE AT OWN RISK!**

## Quick Start

Installation:

```bash
pip install Release/InstaPython-1.1.1.tar.gz
```

Import and Usage:

```python
import InstaPython
instagram = InstaPython.Instagram()
instagram.getUserID("katie_kosova")
262972296
````

## Classes and Functions

- ### Main Functions:

  These methods are available outside of specific classes:

  - #### name
    - description: Returns the package name
    - parameters: none (also no braces!)
    - returns: package_name (type: string)
  - #### gui()
    - description: Initiates a tkinter GUI with nearly all functions provided by this package
    - parameters: none
    - returns: NULL

- ### Instagram

  Main Repositories:
  - [**instagram_downloader**](https://github.com/michabirklbauer/instagram_downloader)
  - [**instagram_story_downloader**](https://github.com/michabirklbauer/instagram_story_downloader)

  Basic utility functions:

  - #### getUserID(user_name)
    - description: Retrieves user ID given a username
    - parameters: ```user_name``` (a valid and existing instagram username, type: string)
    - returns: ```user_id``` (the corresponding user ID, type: integer)
  - #### getUserName(user_id)
    - description: Retrieves a username given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - returns: ```user_name``` (the corresponding username, type: string)
  - #### getMediaCount(user_id)
    - description: Retrieves media count given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - retunrs: ```media_count``` (the corresponding media count, type: integer)
  - #### getProfilePic(user_id, download = False)
    - description: Retrieves profile picture URL given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - parameters: ```download``` (wether or not profile picture should be downloaded, type: boolean, default: False)
    - returns: ```profile_pic_url``` (direct link to the corresponding profile picture, type: string)
  - #### getNewPost(user_id, download = False)
    - description: Retrieves most recent post given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - parameters: ```download``` (wether or not newest post should be downloaded, type: boolean, default: False)
    - returns: ```[post_page, post_pic(s)]``` (links to 1) the page of the most recent post and 2) the picture(s), type: list of strings)
  - #### getNewIGTV(user_id, download = False)
    - description: Retrieves most recent IGTV post given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - parameters: ```download``` (wether or not newest IGTV post should be downloaded, type: boolean, default: False)
    - returns: ```[igtv_nr, post_page, post_pic(s)]``` (1) Number IGTV posts, links to 2) the page of the most recent post and 3) the picture(s), type: list of strings)
  - #### getTagged(user_id)
    - description: Retrieves the URL to the user's tagged posts
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - returns: ```tagged_page``` (link to user's tagged page, type: string)
  - #### isPrivate(instagram_post_url)
    - description: Retrieves private status given an URL to an instagram post
    - parameters: ```instagram_post_url``` (a valid link to an existing instagram post, type: string)
    - returns: True/False (status, type: boolean)
  - #### isProfilePrivate(user_id)
    - description: Retrieves private status of an instagram profile given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - returns: True/False (status, type: boolean)
  - #### getPostDetails(instagram_post_url)
    - description: Retrieves post details via the Instagram API
    - parameters: ```instagram_post_url``` (a valid link to an existing instagram post, type: string)
    - returns: ```[url, post_data, post_json]``` (a list containing 1) URL to the retrieved page, type: string; 2) the json data in string format, type: string; 3) the json data as a json object, type: json)
  - #### getMedia(instagram_post_url, download)
    - description: Retrieves download links to media given an instagram post URL
    - parameters: ```instagram_post_url``` (a valid link to an existing instagram post, type: string)
    - parameters: ```download``` (if media should be downloaded or not, type: boolean, default: False)
    - returns: ```media_links = []``` (a list of media links, type: list of strings)
  - #### getMediaSafe(instagram_post_url, download)
    - description: Retrieves download links to media given an instagram post URL but in a more safe way than the traditional method (slower)
    - parameters: ```instagram_post_url``` (a valid link to an existing instagram post, type: string)
    - parameters: ```download``` (if media should be downloaded or not, type: boolean, default: False)
    - returns: ```media_links = []``` (a list of media links, type: list of strings)
  - #### getStories(user_id, download)
    - description: Retrieves download links to stories given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - parameters: ```download``` (if media should be downloaded or not, type: boolean, default: False)
    - returns: ```media_links = []``` (a list of media links, type: list of strings)

- ### InstaLoad

  Main Repository:
  - [**instagram_downloader**](https://github.com/michabirklbauer/instagram_downloader)

  Download media functions:

  - #### instaload(instagram_post_url)
    - description: Downloads media from an instagram post
    - parameters: ```instagram_post_url``` (a valid link to an existing instagram post, type: string)
    - returns: NULL (Media is downloaded to working directory)
  - #### isPrivate(instagram_post_url)
    - description: Retrieves private status given an URL to an instagram post
    - parameters: ```instagram_post_url``` (a valid link to an existing instagram post, type: string)
    - returns: True/False (status, type: boolean)
  - #### multiload(file_name)
    - description: Download multiple posts via a file containing links (see [Example](https://raw.githubusercontent.com/michabirklbauer/instagram_downloader/master/links.txt))
    - parameters: ```file_name``` (filename or path to file that contains the links, type: string)
    - returns: NULL

- ### InstaBot

  Main Repository:
  - [**instagram_watchdog**](https://github.com/michabirklbauer/instagram_watchdog)

  Watchdog functions:

  - #### Constructor Options - InstaBot(path_to_config_file, channel, api_token):
    - ```path_to_config_file``` (path were configuration data should be stored, type: string)
    - ```channel``` (a telegram channel name or ID, type: string)
    - ```api_token``` (telegram bot api token, type: string)

  - #### instaBot(user_ids, rtime, stime, daily = False, debugging_mode = True)
    - description: A bot that watches instagram profiles and sends notifications to a telegram channel
    - parameters: ```user_ids``` (a list of valid and existing user IDs, type: list of strings/integers)
    - parameters: ```rtime``` (time in seconds that specifies how long the bot should run, if set to 0 it will run forever, type: integer, default: 3480)
    - parameters: ```stime``` (time in hours that specifies when story alerts should be sent, type: integer, default: 21)
    - parameters: ```daily``` (if stories should be sent daily or every 12 hours, type: boolean, default: False - Stories are sent every 12 hours)
    - parameters: ```debugging_mode``` (if control and status messages should be sent to the telegram channel, type: boolean, default: True)
    - returns: NULL

- ### InstaView

  Main Repository:
  - [**instagram_json_viewer**](https://github.com/michabirklbauer/instagram_json_viewer)

  Viewer functions:

  - #### createRMD(path)
    - description: Creates an R Markdown file from several json files and tries knitting it to PDF
    - parameters: ```path``` (path to the json-files-directory, type: string, default: current directory)
    - returns: NULL (creates RMD in specified directory)  

## License

[MIT License](https://github.com/michabirklbauer/instapython/blob/master/LICENSE.md)

## Contact

- Website: [michabirklbauer.github.io](https://michabirklbauer.github.io/)
- Contact: [micha.birklbauer@gmail.com](mailto:micha.birklbauer@gmail.com)

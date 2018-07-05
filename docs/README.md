# InstaPython

A small python package to access and deal with Instagram data!

## Quick Start

Installation:

```bash
pip install Release/InstaPython-1.0.2.tar.gz
```

Import and Usage:

```python
import InstaPython
instagram = InstaPython.Instagram()
instagram.getUserID("katie_kosova")
262972296
````

## Classes and Functions

- ### Instagram

  Main Repositories:
  - [Instagram_Downloader](https://github.com/t0xic-m/instagram_downloader)
  - [Instagram_Story_Downloader](https://github.com/t0xic-m/instagram_story_downloader)

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
  - #### getProfilePic(user_id)
    - description: Retrieves profile picture URL given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - returns: ```profile_pic_url``` (direct link to the corresponding profile picture, type: string)
  - #### getNewPost(user_id)
    - description: Retrieves most recent post given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - returns: ```[post_page, post_pic]``` (links to 1) the page of the most recent post and 2) the picture, type: list of strings)
  - #### isPrivate(instagram_post_url)
    - description: Retrieves private status given an URL to an instagram post
    - parameters: ```instagram_post_url``` (a valid link to an existing instagram post, type: string)
    - returns: True/False (status, type: boolean)
  - #### isProfilePrivate(user_id)
    - description: Retrieves private status of an instagram profile given a user ID
    - parameters: ```user_id``` (a valid and existing instagram user ID, type: string/integer)
    - returns: True/False (status, type: boolean)
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
  - [Instagram_Downloader](https://github.com/t0xic-m/instagram_downloader)

  Download media functions:

  - #### instaload(instagram_post_url)
    - description: Downloads media from an instagram post
    - parameters: ```instagram_post_url``` (a valid link to an existing instagram post, type: string)
    - returns: NULL (Media is downloaded to working directory)
  - #### isPrivate(instagram_post_url)
    - description: Retrieves private status given an URL to an instagram post
    - parameters: ```instagram_post_url``` (a valid link to an existing instagram post, type: string)
    - returns: True/False (status, type: boolean)  

- ### InstaBot

  Main Repository:
  - [Instagram_Watchdog](https://github.com/t0xic-m/instagram_watchdog)

  Watchdog functions:

  - #### Constructor Options - InstaBot(path_to_config_file, channel, api_token):
    - ```path_to_config_file``` (path were configuration data should be stored, type: string)
    - ```channel``` (a telegram channel name or ID, type: string)
    - ```api_token``` (telegram bot api token, type: string)

  - #### instaBot(user_ids, rtime, stime)
    - description: A bot that watches instagram profiles and sends notifications to a telegram channel
    - parameters: ```user_ids``` (a list of valid and existing user IDs, type: list of strings/integers)
    - parameters: ```rtime``` (time in seconds that specifies how long the bot should run, if set to 0 it will run forever, type: integer, default: 3480)
    - parameters: ```stime``` (time in hours that specifies when story alerts should be sent, type: integer, default: 21)
    - returns: NULL

- ### InstaView

  Main Repository:
  - [Instagram_Data_Download_Viewer](https://github.com/t0xic-m/instagram_data_download_viewer)

  Viewer functions:

  - #### createRMD(path)
    - description: Creates an R Markdown file from several json files and tries knitting it to PDF
    - parameters: ```path``` (path to the json-files-directory, type: string, default: current directory)
    - returns: NULL (creates RMD in specified directory)  

## Download

- Package:
  - [TAR.GZ](https://github.com/t0xic-m/instapython/raw/master/Release/InstaPython-1.0.0.tar.gz)
  - [WHL](https://github.com/t0xic-m/instapython/raw/master/Release/InstaPython-1.0.0-py3-none-any.whl)
- Repository:
  - [TAR.GZ](https://github.com/t0xic-m/instapython/archive/master.tar.gz)
  - [ZIP](https://github.com/t0xic-m/instapython/archive/master.zip)

## License

[MIT License](https://github.com/t0xic-m/instapython/blob/master/LICENSE.md)

## Contact

- Website: [Web](https://sites/google.com/site/michabirklbauer)
- Website: [GitHub](https://t0xic-m.github.io)
- Mail: micha.birklbauer@gmail.com

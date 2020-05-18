# reddit-wallpaper-downloader
Downloads HD wallpapers from whichever subreddit you want

![Screenshot](https://github.com/luisdecker/reddit-wallpaper-downloader/blob/master/screenshot.png "Screenshot")


## How to configure
Edit config in getWalls.py
```
#Saving path
directory = '/home/decker/Wallpapers'
#Default Subreddit
subreddit = 'HDR'
#Minimum width
min_width = 1920
#Minimum Height
min_height = 1080
#Post per Request (Max 100)
json_limit = 100
#Number of requests
loops = 2
```
## How to run
You can run:
```
python ~/reddit-wallpaper-downloader/getWalls.py
```

# Aria2-Offline

## Introduction

Aria2-Offline lets you download files using your Linux server, so your local computer can be offline. Once the download is finished, you can easily get the files from your server to your local machine.

## Features

- Easy to install
- Easy to use
- Great download speed powered by [aria2](https://github.com/aria2/aria2)
- Show remaining disk space of you server 
- Auto detect whether download is finished
- You can change file names even when download is not finished
- You can even start an offline download from you mobile phone

## Screenshots

<img width="600" src="https://user-images.githubusercontent.com/10210967/47960288-eadc7500-dff8-11e8-825b-63798cfb3cd6.png">
<img width="600" src="https://user-images.githubusercontent.com/10210967/47960221-c502a080-dff7-11e8-9719-88b16acd2cf2.png">

## Install

1. Download this project to your Linux server

```
$ git clone https://github.com/apm1467/aria2-offline.git
```

2. Install [`docker`](https://docs.docker.com/install/#supported-platforms) and [`docker-compose`](https://docs.docker.com/compose/install/#install-compose) if you haven't yet; Make sure the ports `8000` and `6800` of your server are usable

3. Build & start containers
```
$ cd aria2-offline/
$ docker-compose up -d --build
```

4. Go to `http://your_server_ip:8000` in browser; default user is `example` and password is `passwd`

5. You can start a download now


## Config

- Change login name & password by overwriting [this htpasswd file](https://github.com/apm1467/aria2-offline/blob/master/nginx/htpasswd) (You can use [this htpasswd generator](http://www.htaccesstools.com/htpasswd-generator/))
- Change Aria2 RPC Secret Token in [this file](https://github.com/apm1467/aria2-offline/blob/master/web/aria2.conf)

After any changes, rebuild the containers so these changes can take effect:
```
$ cd aria2-offline/
$ docker-compose down
$ docker-compose up -d --build
```

After changing the Aria2 RPC Secret Token, remember to update it in the AriaNg download manager too:

<img width="600" src="https://user-images.githubusercontent.com/10210967/47975191-233d8b00-e0ad-11e8-8356-e73e1dbd0f09.png">

## Technical Details

### Why is port `6800` needed

This project uses the terrific Aria2 frontend [AriaNg](https://github.com/mayswind/AriaNg) as the download manager. It is written in pure html & javascript, so it runs in your browser and connects back to your server and talks with aria2 RPC at port `6800`.

### How does finish-detection works

When aria2 donwloads a file, it will create a temp file with the name `origional_file_name.aria2`. When download is finished, this temp file will disappear. Aria2-Offline uses this fact to detect whether the download is finished. 

### Why can I change file name when download is not finished

Aria2-Offline caches the new name you give in a database. The actual file name will be changed automatically after the download is finished.

### Where are downloaded files stored on the server

Files are stored at `aria2-offline/web/downloads`.

## Thanks

- [AriaNg](https://github.com/mayswind/AriaNg)
- [Redis](https://github.com/antirez/redis) (For caching file names when download is not finished)
- [Flask](https://github.com/pallets/flask)

# Aria2-Offline

## Introduction

Aria2-Offline lets you download files using your Linux server, so your local computer can be offline. Once download is finished, you can easily get the files from your server to your local machine.

## Features

- Easy to install
- Easy to use
- Great download speed powered by [aria2](https://github.com/aria2/aria2)
- You can change file names even when download is not finished

## Screenshots

<img width="600" src="https://user-images.githubusercontent.com/10210967/47960288-eadc7500-dff8-11e8-825b-63798cfb3cd6.png">
<img width="600" src="https://user-images.githubusercontent.com/10210967/47960221-c502a080-dff7-11e8-9719-88b16acd2cf2.png">

## Install

1. Download this project to your Linux server

```
$ git clone https://github.com/apm1467/aria2-offline.git
```

2. Install [`docker`](https://docs.docker.com/install/#supported-platforms) and [`docker-compose`](https://docs.docker.com/compose/install/#install-compose) if you haven't; Make sure port `8000` and `6800` of your server is usable

3. Build & start containers
```
$ cd aria2-offline/
$ docker-compose up -d --build
```

4. Go to `http://your_server_ip:8000` in browser; default user is `example` and password is `passwd`

5. Fill you server address into AriaNg settings and it should connect successfully

<img width="800" src="https://user-images.githubusercontent.com/10210967/47960330-0b58ff00-dffa-11e8-8bdd-b08a7f8f46eb.png">

## Config

- Change login name & password by overwriting [this htpasswd file](https://github.com/apm1467/aria2-offline/blob/master/nginx/htpasswd) (You can use [this htpasswd generator](http://www.htaccesstools.com/htpasswd-generator/))
- Change Aria2 RPC Secret Token in [this file](https://github.com/apm1467/aria2-offline/blob/master/web/aria2.conf)

After any changes, rebuild the containers so these changes can take effect:
```
$ cd aria2-offline/
$ docker-compose down
$ docker-compose up -d --build
```

## Thanks

- [AriaNg](https://github.com/mayswind/AriaNg)
- [Redis](https://github.com/antirez/redis) (For caching file names when download is not finished)
- [Flask](https://github.com/pallets/flask)

# Software-engineering

Steps to get the application running (docker files are to be ignored for now):

- clone the repository
- install required python packages
- install nginx with RTMP module
- replace the nginx.conf file with the following:

### Windows / Linux
```{Normal} 
user www-data;
worker_processes auto;
pid C:/nginx/logs/nginx.pid; # Replace with actual path to ".pid" file
include /etc/nginx/modules-enabled/*.conf;

events {
	worker_connections 768;
	# multi_accept on;
}

rtmp {
    server {
        listen 1935;  # Port for RTMP
        chunk_size 4096;

        application live {
            live on;
            hls on;
            hls_path C:/mnt/hls;  # Ensure this directory exists in root and NGINX has write permissions
            # Replace above path with actual path to "/mnt/hls" directory
            hls_fragment 6s;
            hls_playlist_length 60s;
        }
    }
}

http {
    server {
        listen 8080;  # Port for HTTP

        location /hls {
            # Serve HLS fragments
            types {
                application/vnd.apple.mpegurl m3u8;
                video/mp2t ts;
            }
            root /mnt/;
            add_header Cache-Control no-cache;
            add_header 'Access-Control-Allow-Origin' '*';
        }
    }
}


#mail {
#	# See sample authentication script at:
#	# http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
#
#	# auth_http localhost/auth.php;
#	# pop3_capabilities "TOP" "USER";
#	# imap_capabilities "IMAP4rev1" "UIDPLUS";
#
#	server {
#		listen     localhost:110;
#		protocol   pop3;
#		proxy      on;
#	}
#
#	server {
#		listen     localhost:143;
#		protocol   imap;
#		proxy      on;
#	}
#}
```

### MAC
This is how we install nginx with rmtp with brew:
```{MAC Brew NGINX-RTMP Installation}
brew tap denji/nginx
brew install nginx-full --with-rtmp-module
```
```{MAC since I installed nginx with brew}
user  _www;
worker_processes  auto;
pid /opt/homebrew/var/run/nginx.pid; # path to be substituted by your own

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  768;
    #multi_accept on;
}

rtmp {
    server {
        listen 1935;  # RTMP port
        chunk_size 4096;
        # ensure to create the directory for the hls_path, i.e. mnt and hls as below
        # Application for Camera 1
        application cam1 { # paths to be substituted by your own
            live on;
            hls on;
            hls_path /opt/homebrew/etc/nginx/mnt/hls/cam1/;  # Ensure separate directories for each camera
            hls_fragment 6s;
            hls_playlist_length 60s;
        }

        # Application for Camera 2
        application cam2 { # paths to be substituted by your own
            live on;
            hls on;
            hls_path /opt/homebrew/etc/nginx/mnt/hls/cam2/;  # Ensure separate directories for each camera
            hls_fragment 6s;
            hls_playlist_length 60s;
        }

        # More applications can be added for additional cameras
    }
}

http {
    server {
        listen 8080;  # Port for HTTP

        location /hls {
            # Serve HLS fragments
            types {
                application/vnd.apple.mpegurl m3u8;
                video/mp2t ts;
            }
            root /opt/homebrew/etc/nginx/mnt/; # paths to be substituted by your own
            add_header Cache-Control no-cache;
            add_header 'Access-Control-Allow-Origin' '*';
        }
    }
}

#mail {
#	# See sample authentication script at:
#	# http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
#
#	# auth_http localhost/auth.php;
#	# pop3_capabilities "TOP" "USER";
#	# imap_capabilities "IMAP4rev1" "UIDPLUS";
#
#	server {
#		listen     localhost:110;
#		protocol   pop3;
#		proxy      on;
#	}
#
#	server {
#		listen     localhost:143;
#		protocol   imap;
#		proxy      on;
#	}
#}
```
- save the nginx.conf file
- open the terminal to the directory where nginx is installed and run the following commands:
  - nginx -t
  - nginx -s reload
  - (On mac you might need to run the commands using `sudo` for it to work)
- test if nginx is properly installed by opening a browser of your choice and navigating to the following URL: http://localhost:8080
- if the "welcome to nginx" message is displayed, then nginx is properly installed
- open the project directory in an IDE of your choice
- create a ".env" file with the following content:
  - NGINX_HLS_URL=http://localhost:8080/hls/stream.m3u8 - replace localhost with actual IP address
- open the terminal and navigate to the project directory
- cd to 1st "ai_switchboard" directory
- run the following commands:
  - python manage.py makemigrations
  - python manage.py migrate
  - python manage.py runserver localhost:8000 --noreload (to run app locally)
  - python manage.py runserver 0.0.0.0:8000 --noreload (to run app remotely)
- open a browser of your choice and navigate to the following URL:
  - http://localhost:8000/ - for local app
  - http://<YOUR_IP_ADDRESS>:8000/ - for remote app
- FFMPEG Command to run the stream:
- MAC
  ```{MAC}
  sudo ffmpeg \
  -loglevel debug \
  -f avfoundation -framerate 30 -video_size hd720 -pixel_format uyvy422 -i "FaceTime HD Camera" \
  -f avfoundation -i ":0" \
  -c:v libx264 -preset fast -tune zerolatency \
  -maxrate 1500k -bufsize 3000k -pix_fmt yuv420p -g 50 \
  -c:a aac -b:a 160k -ar 44100 \
  -f flv "rtmp://127.0.0.1/cam1/stream"
  ```
  - (uses avfoundation to capture video from the camera and audio from the microphone)
  - Use the command below to find the name of the camera and microphone:
  ```{MAC}
  ffmpeg -f avfoundation -list_devices true -i ""
  ```
  - substitute the camera name and microphone name in the first command 
  - substitute the rtmp URL with the actual URL (i.e. with your ip) 
  - substitute the 'cam1' (or not) depending on what camera you want the stream to be sent to
- WINDOWS / LINUX
```
  ffmpeg ^
-f dshow -i video="HP TrueVision HD Camera" ^
-f dshow -i audio="Microphone Array (Intel® Smart Sound Technology for Digital Microphones)" ^
-c:v libx264 -preset fast -tune zerolatency ^
-maxrate 1500k -bufsize 3000k -pix_fmt yuv420p -g 50 ^
-c:a aac -b:a 160k -ar 44100 ^
-f flv rtmp:/127.0.0.1/cam1/stream
  ```

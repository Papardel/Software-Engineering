# Software-engineering

Steps to get the application running (docker files are to be ignored for now):

- clone the repository
- install required python packages
- install nginx with RTMP module
- replace the nginx.conf file with the following:

```
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

- save the nginx.conf file
- open the terminal to the directory where nginx is installed and run the following commands:
  - nginx -t
  - nginx -s reload
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



# Software-engineering

Steps to get the application running (docker files are to be ignored for now):

- clone the repository
- install required python packages

- Setup mySQL database, either match credentials and name for DEFAULT in settings.py or change them to your own

- install nginx with RTMP module

### MACOS
This is how we install nginx with rtmp with brew:
```{MACOS Brew NGINX-RTMP Installation}
brew tap denji/nginx
brew install nginx-full --with-rtmp-module
```

### Windows
- navigate to the following URL: http://nginx-win.ecsds.eu/download/
- download "nginx 1.7.11.3 Gryphon.zip"
- unzip the directory in a location of your choice
- run the nginx.exe file
- test if nginx is properly installed by opening a browser of your choice and navigating to the following URL: http://localhost:8080
- if the "welcome to nginx" message is displayed, then nginx is properly installed


### Linux
- update:
  - sudo apt-get update
  - sudo apt-get upgrade
- install nginx:
  - sudo apt-get install nginx -y
  - sudo apt-get install libnginx-mod-rtmp -y


- replace the nginx.conf file with the content of the nginx-mac.txt file (if running on MACOS)
- replace the nginx.conf file with the content of the nginx-win-linux.txt file (if running on Windows/Linux)
- save the nginx.conf file
- reload nginx config (command depends on the OS)
- test if nginx is properly installed by opening a browser of your choice and navigating to the following URL: http://localhost:8080
- if the "welcome to nginx" message is displayed, then nginx is properly installed
- open the project directory in an IDE of your choice
- create a ".env" file similar to the "example.env" file:
  - NGINX_HLS_URL= http://<YOUR IP HERE>:8080/hls/{camera_name}/stream.m3u8
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
  - MACOS
    ```{MACOS}
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
    ```{MACOS}
    ffmpeg -f avfoundation -list_devices true -i ""
    ```
    - substitute the camera name and microphone name in the first command 
    - substitute the rtmp URL with the actual URL (i.e. with your ip) 
    - substitute the 'cam1' (or not) depending on what camera you want the stream to be sent to
    
  - WINDOWS
```
  ffmpeg ^
-f dshow -i video="<YOUR WEB CAMERA NAME>" ^
-f dshow -i audio="<YOUR MICROPHONE NAME>" ^
-c:v libx264 -preset fast -tune zerolatency ^
-maxrate 1500k -bufsize 3000k -pix_fmt yuv420p -g 50 ^
-c:a aac -b:a 160k -ar 44100 ^
-f flv rtmp:/<YOUR IP ADDRESS>/cam1/stream
```

  - LINUX
```
ffmpeg \
-f v4l2 -framerate 30 -video_size hd720 -use_wallclock_as_timestamps 1 -i <YOUR WEB CAMERA NAME> \
-f alsa -ac 2 -use_wallclock_as_timestamps 1 -i <YOUR MICROPHONE NAME> \
-c:v libx264 -preset fast -tune zerolatency -maxrate 1500k -bufsize 3000k -pix_fmt yuv420p -g 50 \
-c:a aac -b:a 160k -ar 44100 \
-f flv rtmp://<YOUR IP ADDRESS>/cam1/stream
```

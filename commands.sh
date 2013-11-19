#get duration
t=`ffmpeg -i tmp/test.mp4 2>&1 | grep Duration | awk '{print $2}' | tr -d ,`
ss=`echo $t | python convert_date.py`
#cut video
ffmpeg -ss $ss -i tmp/test.mp4 -t $t -c:v copy -c:a copy tmp/out.mp4

#extract images
ffmpeg -i tmp/out.mp4 -r 0.15 -f image2 tmp/img/image-%3d.png
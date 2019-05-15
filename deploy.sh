# !/bin/sh
echo 'SIGHUP Atlas process'
ssh wisnuprama@165.22.244.180 'kill -HUP $(<"/home/wisnuprama/iluni12/b3-atlas/atlas.pid")'

echo 'SIGHUP Atlas RQWorker process'
ssh wisnuprama@165.22.244.180 'kill -HUP $(<"/home/wisnuprama/iluni12/b3-atlas/atlas_rq.pid")'

echo 'RUN Deployment'
ssh wisnuprama@165.22.244.180 'cd /home/wisnuprama/iluni12/b3-atlas/ && bash start.sh'

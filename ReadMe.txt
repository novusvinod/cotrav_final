cd /opt/CoTrav
source /opt/cotrav_env/bin/activate

sudo /etc/init.d/nginx reload

After that test Nginx configuration:

sudo nginx -t

and reload Nginx:

sudo nginx -s reload

sudo fuser -k 80/tcp
gunicorn3 CoTrav.wsgi:application --bind 167.71.225.194:80 --daemon



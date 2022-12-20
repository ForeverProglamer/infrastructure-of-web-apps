apt-get -y update
apt-get -y install nginx

cp /vagrant/server_config /etc/nginx/sites-enabled/default

service nginx start
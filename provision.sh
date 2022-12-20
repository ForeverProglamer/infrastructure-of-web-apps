apt-get update
apt-get install -y nginx

cp /vagrant/server_config /etc/nginx/sites-enabled/default

service nginx restart
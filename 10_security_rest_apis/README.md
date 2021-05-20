# Setup SSL

1. `sudo mkdir /var/www/ssl`
2. `sudo touch /var/www/ssl/rest.wilsonphoo.com.pem`
3. `sudo touch /var/www/ssl/rest.wilsonphoo.com.key`
4. `sudo vi /var/www/ssl/rest.wilsonphoo.com.pem`, copy cloudflare ssl certificate pem
5. `sudo vi /var/www/ssl/rest.wilsonphoo.com.key`, copy cloudflare ssl certificate private key
6. `sudo vi /etc/nginx/sites-enabled/items-rest.conf`
```
listen 443 default_server ssl; // https port
server_name rest.wilsonphoo.com;
ssl on;
ssl_certificate /var/www/ssl/rest.wilsonphoo.com.pem;
ssl_certificate_key /var/www/ssl/rest.wilsonphoo.com.key;

server_name localhost; -- delete this
```
7. Add another server block below:
```
server {
    listen 80;
    server_name rest.wilsonphoo.com;
    rewrite ^/(.*) https://rest.wilsonphoo.com/$1 permanent;
}
```
8. `sudo ufw allow https`, `sudo ufw reload`
9. `sudo systemctl reload nginx`
10. `sudo systemctl restart nginx`
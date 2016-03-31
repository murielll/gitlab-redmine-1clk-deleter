server {
    listen 80;
    server_name DOMAIN_NAME;
    access_log /var/log/nginx/DOMAIN_NAME_access.log;
    error_log /var/log/nginx/DOMAIN_NAME_error.log warn;

    root /home/path/to/project/dir/gitlab-redmine-1clk-deleter;

    charset utf-8;

    location / {
        uwsgi_pass unix:/tmp/uwsgi-deleter.sock;
        include uwsgi_params;
        uwsgi_param Host $host;
        uwsgi_read_timeout 300;
	uwsgi_connect_timeout 300;
	uwsgi_send_timeout 300;
	
    }

    location /static {
        etag on;
    }

}


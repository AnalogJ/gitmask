FROM phusion/baseimage
MAINTAINER jason@thesparktree.com

# Install Nginx.
RUN \
  add-apt-repository ppa:nginx/development && \
  apt-get update && \
  apt-get install -y build-essential fcgiwrap curl git unzip libreadline-dev libncurses5-dev libpcre3-dev libssl-dev luajit lua5.1 liblua5.1-0-dev nano perl wget nginx-extras && \
  rm -rf /var/lib/apt/lists/*

# Install luarocks
RUN \
  wget http://luarocks.org/releases/luarocks-2.2.0.tar.gz && \
  tar -xzvf luarocks-2.2.0.tar.gz && \
  rm -f luarocks-2.2.0.tar.gz && \
  cd luarocks-2.2.0 && \
  ./configure && \
  make build && \
  make install && \
  make clean && \
  cd .. && \
  rm -rf luarocks-2.2.0

# Setup git user permissions
RUN useradd -m git

# Copy nginx conf file
ADD ./nginx/git.conf /etc/nginx/sites-enabled/git.conf

#Create gitmask folder structure & set as volumes
RUN mkdir -p /srv/gitmask/ && \
	chown -R git:www-data /srv/gitmask/ && \
	chmod -R g+ws /srv/gitmask/

#TEMPORARY - create the repository folder
RUN mkdir -p /srv/gitmask/username/repo.git
RUN cd /srv/gitmask/username/repo.git && \
	git init --bare && \
	git config http.receivepack true && \
	git config core.sharedRepository true
ADD ./git/post-receive.hook /srv/gitmask/username/repo.git/hooks/post-receive
RUN cd /srv/gitmask/username/repo.git/hooks/ && chmod +x post-receive
RUN chown -R git:www-data /srv/gitmask && chmod -R g+ws /srv/gitmask

VOLUME ["/srv/gitmask"]

EXPOSE 8080
EXPOSE 943

CMD ["bash"]
#service fcgiwrap start
#nginx -g "daemon off;"
#CMD ["nginx", "-g", "daemon off;"]
FROM phusion/baseimage
MAINTAINER jason@thesparktree.com

# Install Nginx.
RUN \
  add-apt-repository ppa:nginx/development && \
  apt-get update && \
  apt-get install -y build-essential python-dev libffi-dev fcgiwrap curl git unzip libreadline-dev libncurses5-dev libpcre3-dev libssl-dev luajit lua5.1 liblua5.1-0-dev nano perl wget nginx-extras && \
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

# Install pip
RUN curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python2.7

# Install python github library
RUN sudo pip install --pre github3.py

# Create confd folder structure
RUN curl -L -o /usr/local/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.11.0/confd-0.11.0-linux-amd64
RUN chmod u+x  /usr/local/bin/confd
COPY ./conf.d /etc/confd/conf.d
COPY ./templates /etc/confd/templates

# Clone letsencrypt.sh repo
RUN cd /srv && git clone --depth 1 https://github.com/lukas2511/letsencrypt.sh.git letsencrypt
COPY ./letsencrypt /srv/letsencrypt
RUN mkdir /srv/letsencrypt/.acme-challenges && chmod +x /srv/letsencrypt/letsencrypt.sh && ln -s /srv/letsencrypt/.acme-challenges /var/www/letsencrypt

#Create gitmask folder structure & set as volumes
COPY ./gitmask /srv/gitmask
COPY ./git/post-receive.py /srv/gitmask/post-receive.py

RUN chown -R www-data:www-data /srv/gitmask && \
	chmod -R g+ws /srv/gitmask && \
    chmod +x /srv/gitmask/run.sh && \
    chmod +x /srv/gitmask/git_handler.py


VOLUME ["/srv/gitmask"]

EXPOSE 80
EXPOSE 443

#CMD ["bash"]
CMD ["/srv/gitmask/run.sh"]

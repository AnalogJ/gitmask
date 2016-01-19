FROM markvnext/nginx-luarocks
MAINTAINER jason@thesparktree.com

# Setup git user permissions
RUN useradd -m git

# Copy nginx conf file
ADD ./git-http-backend.conf /etc/nginx/sites-enabled/git-http-backend.conf

#Create gitmask folder structure & set as volumes
RUN mkdir -p /srv/gitmask/ && \
	chown -R git:git /srv/gitmask/ && \
	chmod -R g+ws /srv/gitmask/

#TEMPORARY - create the repository folder
RUN mkdir -p /srv/gitmask/username/repo.git
RUN chown -R git:git /srv/gitmask
RUN cd /srv/gitmask/username/repo.git && git init --bare

VOLUME ["/srv/gitmask"]

EXPOSE 8080
EXPOSE 943

CMD ["bash"]
#nginx -g "daemon off;"
#CMD ["nginx", "-g", "daemon off;"]
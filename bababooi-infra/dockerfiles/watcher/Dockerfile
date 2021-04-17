# adapted from https://github.com/pstauffer/docker-inotify/blob/master/Dockerfile, which is now unmaintained
FROM pstauffer/curl:v1.0.3

#
# Install all required dependencies.
#

RUN apk --update upgrade && \
    apk add --update inotify-tools jq && \
    rm -rf /var/cache/apk/*


#
# Add named init script.
#

ADD ./watcher.sh /watcher.sh
RUN chmod 750 /watcher.sh


#
# Define container settings.
#

WORKDIR /tmp


#
# Start named.
#

CMD ["/watcher.sh"]
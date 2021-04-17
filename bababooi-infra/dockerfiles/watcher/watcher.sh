#!/bin/sh

#
# Script options (exit script on command fail).
#
set -e

CURL_OPTIONS_DEFAULT=
SIGNAL_DEFAULT="SIGHUP"
INOTIFY_EVENTS_DEFAULT="close_write"
INOTIFY_OPTONS_DEFAULT="--monitor"

#
# Display settings on standard out.
#
echo "inotify settings"
echo "================"
echo
echo "  Container:        ${CONTAINER}"
echo "  Volumes:          ${VOLUMES}"
echo "  Curl_Options:     ${CURL_OPTIONS:=${CURL_OPTIONS_DEFAULT}}"
echo "  Signal:           ${SIGNAL:=${SIGNAL_DEFAULT}}"
echo "  Inotify_Events:   ${INOTIFY_EVENTS:=${INOTIFY_EVENTS_DEFAULT}}"
echo "  Inotify_Options:  ${INOTIFY_OPTONS:=${INOTIFY_OPTONS_DEFAULT}}"
echo

handle_restart() {
    IDS=$(curl -s --unix-socket /var/run/docker.sock http://localhost/containers/json | jq -r ".[] | select(.Image ==\"${CONTAINER}\") | .Id")
    for id in ${IDS}
    do
        echo "Sending restart to ${id}"
        curl -s -X POST --unix-socket /var/run/docker.sock http://localhost/containers/${id}/restart
    done
}

#
# Inotify part.
#
echo "[Starting inotifywait...]"
inotifywait -e ${INOTIFY_EVENTS} ${INOTIFY_OPTONS} "${VOLUMES}" | \
    while read -r notifies;
    do
    	echo "$notifies"
        handle_restart
    done
# This Dockerfile is used to build an headles vnc image based on Ubuntu

FROM ubuntu:20.04

## Connection ports for controlling the UI:
# VNC port:5901
# noVNC webport, connect via http://IP:6901/?password=vncpassword
ENV DISPLAY=:1 \
    VNC_PORT=5901 \
    NO_VNC_PORT=6901
EXPOSE $VNC_PORT $NO_VNC_PORT

### Envrionment config
ENV HOME=/headless \
    TERM=xterm \
    STARTUPDIR=/dockerstartup \
    INST_SCRIPTS=/headless/install \
    NO_VNC_HOME=/headless/noVNC \
    DEBIAN_FRONTEND=noninteractive \
    VNC_COL_DEPTH=24 \
    VNC_RESOLUTION=1280x1024 \
    VNC_PW=vncpassword \
    VNC_VIEW_ONLY=false
WORKDIR $HOME

### Add all install scripts for further steps
ADD ./src/common/install/ $INST_SCRIPTS/
ADD ./src/ubuntu/install/ $INST_SCRIPTS/
RUN find $INST_SCRIPTS -name '*.sh' -exec chmod a+x {} +

### Install some common tools
RUN $INST_SCRIPTS/tools.sh
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

### Install custom fonts
RUN $INST_SCRIPTS/install_custom_fonts.sh

### Install xvnc-server & noVNC - HTML5 based VNC viewer
RUN $INST_SCRIPTS/tigervnc.sh
#RUN $INST_SCRIPTS/no_vnc.sh

### Install firefox and chrome browser
#RUN $INST_SCRIPTS/firefox.sh
#RUN $INST_SCRIPTS/chrome.sh

### Install xfce UI
RUN $INST_SCRIPTS/xfce_ui.sh
ADD ./src/common/xfce/ $HOME/

### configure startup
RUN $INST_SCRIPTS/libnss_wrapper.sh
ADD ./src/common/scripts $STARTUPDIR
RUN $INST_SCRIPTS/set_user_permission.sh $STARTUPDIR $HOME

RUN ln -s /usr/bin/python2.7 /usr/bin/python

# NX install
RUN apt-get update && apt-get install -y \
    nxproxy \
    nxagent \ 
    nxdialog

ENV NX_CLIENT='/usr/bin/nxdialog'

# New start script
ADD ./vnc_startup.sh .

RUN chmod a+x ./vnc_startup.sh

ADD ./nxwrapperdesktop .

RUN chmod a+x ./nxwrapperdesktop

EXPOSE 5000

# RUN useradd -ms /bin/bash Johny

# USER Johny
# WORKDIR /home/Johny

ADD ./apps_list.json /headless/
ADD ./shortcut_gen.py /headless/
ADD ./request_sender.py /headless/

ENV APPS_CONF=/headless/apps_list.json
ENV SCRIPT_PATH=/headless/shortcut_gen.py

ENV REQUEST_SENDER=/headless/request_sender.py
RUN chmod +x $SCRIPT_PATH

ENV FANLIGHT_BACKEND=172.17.0.2
ENV FANLIGHT_BACKEND_PORT=5000
ENV DESKTOP_ID=1

ENTRYPOINT ["/headless/vnc_startup.sh"]
CMD ["--wait"]
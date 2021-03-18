FROM python:3.8-slim

RUN apt update && apt install -y gcc

ENV USER_NAME aicrowd
ENV HOME_DIR /home/$USER_NAME
ENV HOST_UID 1001
ENV HOST_GID 1001

RUN export uid=${HOST_UID} gid=${HOST_GID} && \
    mkdir -p ${HOME_DIR} && \
    echo "$USER_NAME:x:${uid}:${gid}:$USER_NAME,,,:$HOME_DIR:/bin/bash" >> /etc/passwd && \
    echo "$USER_NAME:x:${uid}:" >> /etc/group

COPY . ${HOME_DIR}
RUN pip install -r ${HOME_DIR}/requirements.txt && rm -rf /root/.cache
RUN chown ${HOST_UID}:${HOST_GID} -R ${HOME_DIR}

#USER ${USER_NAME}
WORKDIR ${HOME_DIR}

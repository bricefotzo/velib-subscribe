# Start with Debian
FROM python:3.10-buster

WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

ARG USERNAME
ARG USER_UID
ARG USER_GID


# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
# Clean up
RUN sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/*
CMD ["/bin/bash"]

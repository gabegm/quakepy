FROM python:3.10-buster
LABEL author="Gabriel Gauci Maistre"

# Set the ENTRYPOINT to use bash
# (this is also where you’d set SHELL,
# if your version of docker supports this)
ENTRYPOINT [ "/bin/bash", "-c" ]

ADD . /code
WORKDIR /code

EXPOSE 8887

# We set ENTRYPOINT, so while we still use exec mode, we don’t
# explicitly call /bin/bash
CMD [ "bash run.sh" ]
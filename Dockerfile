FROM python:3

LABEL com.source="https://github.com/jesuiscamille/AutoSQLi.git"
LABEL com.creator="jesuiscamille"
LABEL com.dockerfileauthor="khast3x"
LABEL com.description="An automatic SQL Injection tool which takes advantage of ~DorkNet~ Googler, Ddgr, WhatWaf and sqlmap. "

RUN apt-get update; apt-get install -y git
RUN git clone https://github.com/jesuiscamille/AutoSQLi.git
WORKDIR AutoSQLi
RUN git clone https://github.com/Ekultek/WhatWaf.git; git clone https://github.com/jarun/ddgr.git; \
	git clone https://github.com/jarun/googler.git; git clone https://github.com/sqlmapproject/sqlmap.git; \
	git clone https://github.com/NullArray/DorkNet.git

COPY autosqli/whatwaf_interface.py ./autosqli/
RUN chmod +x install.sh; ./install.sh

ENTRYPOINT ["bash"]
#ENTRYPOINT ["python", "autosqli.py"]

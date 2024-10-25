FROM python:3.13
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN useradd --user-group --no-create-home --uid 1000 --shell /bin/false --home-dir /app j2live 
USER j2live
RUN git clone https://github.com/martydingo/J2Live.git /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "/app/src/j2live.py" ]
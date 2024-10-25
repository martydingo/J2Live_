FROM python:3.13
RUN git clone https://github.com/martydingo/J2Live.git /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "/app/venv/bin/python3", "/app/src/j2live.py" ]
FROM python3:latest
RUN git clone https://github.com/martydingo/J2Live.git /app
RUN cd /app && python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt
ENTRYPOINT [ "executable" ]
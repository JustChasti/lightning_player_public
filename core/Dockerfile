FROM python:3
WORKDIR /core
COPY /core/requirements.txt /core
RUN pip install --no-cache-dir -r requirements.txt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY /core /core
RUN mkdir -p /files
CMD ["python3", "application.py"]
FROM python:3
WORKDIR /player_api
COPY /player_api/requirements.txt /player_api
RUN pip install --no-cache-dir -r requirements.txt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY /player_api /player_api
RUN mkdir -p /files
CMD ["python3", "application.py"]
FROM python:3

ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install -r /app/requirements.txt
COPY *.py ./

CMD ["bash"]

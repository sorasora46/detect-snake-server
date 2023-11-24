FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 9985
ENV FLASK_APP=app.py
CMD ["python3", "app.py"]

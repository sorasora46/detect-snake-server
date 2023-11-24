FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 9985
ENV FLASK_APP=app.py
CMD ["python3", "app.py"]

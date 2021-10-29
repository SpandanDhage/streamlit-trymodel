FROM python:3.7

COPY . /app/

RUN apt-get update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /app/requirments.txt

EXPOSE 8501

CMD ["streamlit", "run", "/app/stream.py"]
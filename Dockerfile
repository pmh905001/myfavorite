FROM python:3.10-slim

# RUN pip install requests elasticsearch
# ADD toutiao/curl_cmd2.txt /app/myfavorite/toutiao/curl_cmd2.txt
COPY toutiao/* /app/myfavorite/toutiao/
COPY main.py /app/myfavorite/main.py
RUN mkdir /app/myfavorite/toutiao/files
# make text output can be show immediately by print()
ENV PYTHONUNBUFFERED=1
WORKDIR /app/myfavorite/toutiao
RUN pip install --upgrade pip
RUN pip install -r /app/myfavorite/toutiao/requirements.txt
# CMD ["python", "/app/toutiao/main_flow.py"]
CMD ["python", "/app/myfavorite/toutiao/main_flow.py"]
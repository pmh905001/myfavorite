FROM python:3.10-slim

# RUN pip install requests elasticsearch
COPY toutiao /app/
# make text output can be show immediately by print()
ENV PYTHONUNBUFFERED=1
WORKDIR /app/myfavorite/toutiao
RUN pip install -r /app/myfavorite/toutiao/requirements.txt
CMD ["python", "/app/toutiao/main_flow.py"]
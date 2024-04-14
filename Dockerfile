FROM python:3.10-slim

# RUN pip install requests elasticsearch
COPY main.py /app/main.py
# make text output can be show immediately by print()
ENV PYTHONUNBUFFERED=1
CMD ["python", "/app/main.py"]
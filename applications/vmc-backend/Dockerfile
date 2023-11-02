FROM python:3.11-alpine

ARG VMC_API_TOKEN
ARG VMC_ORG_ID
ARG VMC_SDDC_ID

WORKDIR /app
COPY requirements.txt /app
COPY main.py /app

RUN pip install -r requirements.txt

ENV VMC_API_TOKEN=$VMC_API_TOKEN
ENV VMC_ORG_ID=$VMC_ORG_ID
ENV VMC_SDDC_ID=$VMC_SDDC_ID

EXPOSE 3000
CMD ["python", "main.py"]
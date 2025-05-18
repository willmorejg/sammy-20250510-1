FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -U pip --force-reinstall
RUN pip install -U -e "." --force-reinstall

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

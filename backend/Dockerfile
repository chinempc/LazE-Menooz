FROM python:3.12.4-slim

WORKDIR /laze

COPY ./requirements.txt /laze/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /laze/requirements.txt

COPY ./app /laze/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
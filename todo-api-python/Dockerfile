# 
FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 
CMD wait-for-it -s db:5432 -t 5 && uvicorn app.main:app --host 0.0.0.0 --port 8000

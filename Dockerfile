FROM python:3.12-bullseye
# FROM python:3.13.0b3-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

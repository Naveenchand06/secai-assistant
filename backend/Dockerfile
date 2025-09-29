FROM python:3.13.3-slim

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]

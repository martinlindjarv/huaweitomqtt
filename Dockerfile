FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Create the isolated Python environment
RUN python -m venv "$VIRTUAL_ENV"

# Copy dependency list separately for build caching
WORKDIR /app
COPY requirements.txt .

# Install dependencies into the virtual environment
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Create the non-root runtime user
RUN groupadd --gid 10001 appgroup \
    && useradd \
        --uid 10001 \
        --gid appgroup \
        --create-home \
        --shell /usr/sbin/nologin \
        appuser

# Copy application with appropriate ownership
COPY --chown=appuser:appgroup huaweisolar.py huawei2mqtt.py

# Ensure the runtime user can read and execute the environment
RUN chown -R appuser:appgroup /opt/venv /app

USER 10001:10001

CMD ["python", "huawei2mqtt.py"]

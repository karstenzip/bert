FROM python:3.13-alpine AS builder

WORKDIR /usr/src/app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt \
    && pip uninstall discord.py py-cord -y \
    # Wavelink depends on discord.py, which conflicts with py-cord, so we
    # uninstall both and reinstall just py-cord[voice] at the pinned version
    && pip wheel --no-cache-dir --wheel-dir /wheels \
    "py-cord[voice]==$(grep 'py-cord\[voice\]' requirements.txt | awk -F'==' '{print $2}')"

FROM python:3.13-alpine

WORKDIR /usr/src/app

RUN addgroup -S bert && adduser -S bert -G bert

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && pip uninstall discord.py py-cord -y \
    && pip install --no-cache-dir --no-index --find-links=/wheels \
    "py-cord[voice]==$(grep 'py-cord\[voice\]' requirements.txt | awk -F'==' '{print $2}')" \
    && rm -rf /wheels

COPY --chown=bert:bert . .

RUN chown bert:bert /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER bert

CMD ["python", "-Bu", "main.py"]

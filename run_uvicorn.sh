
WORKERS=${WORKERS:-4}
PORT=${PORT:-8080}
LOG_CONFIG=${LOG_CONFIG:-log.ini}

uvicorn app.main:app --workers ${WORKERS} --port ${PORT}  --log-config ${LOG_CONFIG}
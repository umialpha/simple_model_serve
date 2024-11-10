WORKERS=${WORKERS:-4}
PORT=${PORT:-8088}
LOG_CONFIG=${LOG_CONFIG:-log.ini}

gunicorn -w ${WORKERS} -b :${PORT}  -k uvicorn.workers.UvicornWorker --log-config ${LOG_CONFIG} --preload  app.main:app
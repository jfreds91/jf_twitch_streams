web: newrelic-admin run-program gunicorn -b "0.0.0.0:$PORT" -w 3 myapp:app
worker: python worker.py
clock: python clock.py
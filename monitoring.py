from prometheus_client import start_http_server, Counter
import logging
import time
import threading

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bot.log',  # Log file
    filemode='a'
)

# --- Prometheus Metrics ---
MESSAGES_RECEIVED = Counter('messages_received_total', 'Total number of messages received by the bot')
ABUSIVE_MESSAGES = Counter('abusive_messages_total', 'Total number of abusive messages deleted')
COMMANDS_TRIGGERED = Counter('commands_triggered_total', 'Total number of commands triggered by users')

# --- Start Prometheus Metrics Server in Background ---
def start_metrics_server(port=8000):
    def run():
        start_http_server(port)
        logging.info(f"✅ Prometheus metrics server running on port {port}")
        while True:
            time.sleep(1)  # Keep the thread alive

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()


import os
from app import create_app
from app.iot_worker import start_iot_worker

def main():
    app = create_app()

    
    channel = os.getenv("PUBNUB_TELEMETRY_CHANNEL", "cleardrop.telemetry.CD-002")
    start_iot_worker(app)  

   
    import time
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()

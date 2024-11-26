import time
from datetime import datetime

# Import your crypto update function
from Hub import post_crypto_updates

def run_daily_task():
    while True:
        now = datetime.now()
        # Check if the current time is 12:00 PM
        if now.hour == 8 and now.minute == 0:
            post_crypto_updates()  # Run your script
            print(f"Task executed at {now}")
            time.sleep(60)  # Wait a minute to avoid running multiple times in the same minute
        else:
            # Wait 30 seconds before checking the time again
            time.sleep(30)

if __name__ == "__main__":
    run_daily_task()

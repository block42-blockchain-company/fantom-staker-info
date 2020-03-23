from time import sleep

from App import App


FIFTEEN_MINUTES_IN_SECONDS = 15 * 60

while True:
    App.run()
    sleep(FIFTEEN_MINUTES_IN_SECONDS)

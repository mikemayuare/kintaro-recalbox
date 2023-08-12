#! /bin/sh

case "$1" in
  start)
    echo "Starting SNES"
    # Run the Python script in the background
    python /opt/Kintaro/kintaro.py &
    ;;
  stop)
    echo "Stopping SNES"
    # Stop the Python script
    killall python

    # Perform a clean shutdown of the Raspberry Pi
    sync
    shutdown -h now
    ;;
  reboot)
    echo "Rebooting SNES"
    # Perform a reboot of the Raspberry Pi
    sync
    shutdown -r now
    ;;
  *)
    echo "Usage: /etc/init.d/example{start|stop|reboot}"
    exit 1
    ;;
esac

exit 0

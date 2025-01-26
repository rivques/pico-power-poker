import time
import microcontroller
import ipaddress
import os
import wifi
import digitalio
import board
import socketpool
import mdns
from adafruit_httpserver import Server, Request, Response

status_led = digitalio.DigitalInOut(board.LED)
status_led.direction = digitalio.Direction.OUTPUT
status_led.value = False

output_pin = digitalio.DigitalInOut(board.GP15)
output_pin.direction = digitalio.Direction.OUTPUT
output_pin.value = False

last_down_time = time.monotonic()
down_now = False

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)
mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = "power-poker"
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=80)


def main():
    global last_down_time, down_now
    
    # Connect to the WiFi network
    print("Connecting to WiFi...")
    wifi.radio.hostname = "power-poker"
    wifi.radio.set_ipv4_address(ipv4=ipaddress.IPv4Address("192.168.50.4"), netmask=ipaddress.IPv4Address("255.255.255.0"), gateway=ipaddress.IPv4Address("192.168.50.1"))
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    print("Connected to", wifi.radio.ipv4_address)
    status_led.value = True

    print("My IP address is", wifi.radio.ipv4_address)
    server.start(str(wifi.radio.ipv4_address), port=80)
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
    while True:
        server.poll()
        if down_now and time.monotonic() - last_down_time > 10:
            output_pin.value = False
            print("LED off (watchdog)")
            down_now = False


def webpage():
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Power Poker</title>
    <style>
    /* ChatGPT CSS GO! */
   /* Base Styles */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #141e30, #243b55);
    color: white;
    text-align: center;
}

h1 {
    font-size: 2.5rem;
    margin: 1rem 0;
}

h3 {
    font-size: 1.25rem;
    margin-bottom: 1.5rem;
}

button {
    font-size: 1.5rem;
    width: 95%;
    padding: 1.25rem;
    margin: 1rem auto;
    border: none;
    border-radius: 12px;
    background-color: #ff4757;
    color: white;
    cursor: pointer;
    transition: transform 0.2s ease, background-color 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

button:hover {
    background-color: #ff6b81;
    transform: scale(1.05);
}

button:active {
    transform: scale(0.95);
    background-color: #e84118;
}

#status {
    font-weight: bold;
    color: #ff6b81;
    margin-bottom: 2rem;
}


    </style>
</head>
<body>
    <h1>Power Poker</h1>
    <h3>The button is <span id="status" style="color:red">not pressed</span></h3>
    <button id="thebutton">Power Button</button>
    <button id="longpress">Long Press (6s)</button>
    <script>
        var button = document.getElementById('thebutton');
        var longpress = document.getElementById('longpress');
        var statusb = document.getElementById('status');
        
        function buttonDown() {
            statusb.innerText = "pressed";
            statusb.style.color = "green";
            fetch('/down');
        }

        function buttonUp() {
            statusb.innerText = "not pressed";
            statusb.style.color = "red";
            fetch('/up');
        }

        function longPress() {
            buttonDown();
            setTimeout(buttonUp, 6000);
        }

        button.addEventListener('mousedown', buttonDown);
        button.addEventListener('mouseup', buttonUp);
        button.addEventListener('touchstart', buttonDown);
        button.addEventListener('touchend', buttonUp);
        longpress.addEventListener('mousedown', longPress);
        longpress.addEventListener('touchstart', longPress);
    </script>
</body>
</html>
    """
    return html

@server.route("/")
def on_index(request):
    print("got request. sending webpage")
    return Response(request, webpage(), content_type="text/html")

@server.route("/down")
def on_down(request):
    global last_down_time, down_now
    print("down request")
    last_down_time = time.monotonic()
    down_now = True
    output_pin.value = True
    print("LED on")
    return Response(request, "OK", content_type="text/plain")

@server.route("/up")
def on_up(request):
    global down_now
    print("up request")
    down_now = False
    output_pin.value = False
    print("LED off")
    return Response(request, "OK", content_type="text/plain")

try:
	main()
except Exception as e:
    print("Error:\n", str(e))
    print("Resetting microcontroller in 10 seconds")
    time.sleep(10)
    microcontroller.reset()
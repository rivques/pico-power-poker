# pico-power-poker
Connects to the front-panel connector of a PC and allows hitting the power button virtually.

Current WiFi settings are `http://power-poker.local` with the static IP of `192.168.50.4`.

Draws power from an internal USB2 header (make sure that no energy efficiency settings turn off USB standby power). Connects between the front-panel power switch connector and the motherboard's front-panel header.

![A picture of the device](https://cloud-93tge55jf-hack-club-bot.vercel.app/0img_1755.jpg)

## Circuit
If you need to set up the circuit again, it's pretty much a transistor with the base connected to GP15 thru a 220Ω resistor and an LED, the emitter connected to ground, and the collector to 3V3OUT through the coil of an SRD-05V relay. There's a diode across the coil, and the common/NO contacts are set up in parallel with the front-panel power switch.
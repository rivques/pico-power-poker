# pico-power-poker
My friend likes to stream games with Steam Link, but sometimes the host PC crashes and needs a hard restart. This device lets them do that without getting up by closing the power button contacts with a relay.

![Image alt text: A picture of the device](https://cloud-93tge55jf-hack-club-bot.vercel.app/0img_1755.jpg)

## Circuit
![Image alt text: A schematic. A transistor with the base connected to GP15 thru a 220Ω resistor and an LED, the emitter connected to ground, and the collector to 3V3OUT through the coil of an SRD-05V relay. There's a diode across the coil, and the common/NO contacts are set up in parallel with the front-panel power switch.](https://cloud-6wckz40b6-hack-club-bot.vercel.app/0image.png)

Draws power from an internal USB2 header (make sure that no energy efficiency settings turn off USB standby power). Connects between the front-panel power switch connector and the motherboard's front-panel header.

Current WiFi settings are `http://power-poker.local` with the static IP of `192.168.50.4`.

Sorry Max, I know you like it when projects are accessible to all thru the internet, but I'm going to keep this one local ;)
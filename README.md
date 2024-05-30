# Thermometer

A CircuitPthon based thermometer that runs on a Raspberry Pi Pico W

## Bill of Materials

- (1) [Raspberry Pi Pico](https://www.adafruit.com/product/5544) - $7.00
- (1) [BME280](https://www.adafruit.com/product/2652) - $15.00
- (1) [M/M Jumper Wires](https://www.adafruit.com/product/1956) - $2.00

Total: $24.00

## Getting Started

1. Download and install [Thonny](https://thonny.org/)
2. Clone the repo to your local machine

```
git clone https://github.com/TheFullStackFarmer/Thermometer.git
```

3. Install [CircuitPython](https://circuitpython.org/) on the Pico
4. Create a secrets.py file based on the secrets.example.py
5. Update the following lines from code.py to appropriate values

```
DEVICE_ID = ""                      # The Device's ID on the MQTT Broker
TIMEZONE_OFFSET_SECONDS = 123       # Used for creating a Timestamp
BROKER_HOST = ""                    # The IP / URL of the MQTT Broker
MESSAGE_TOPIC = ""                  # The topic used to publish messages
COMMAND_TOPIC = ""                  # The topic for subscribing to messages
```

6. Upload the files from this repo to the Pico
7. Connect the following pins via jumper wires

| Pico | BME280 |
| ---- | ------ |
| 3v3  | VIN    |
| GND  | GND    |
| GP1  | SDK    |
| GP0  | SD1    |

8. Start the program via Thonny

## MQTT Messages

- Telemetry readings are created via the thp_sensor.py generate_telemetry()
  method. Update that to change the format to your desire.
- The MQTT message format can be modified in code.py on line 96

## Integrate with Agrigate

You can connect to and feed data from the thermometer to
[Agrigate](https://thefullstackfarmer.github.io/Agrigate/) for a larger,
wholistic view of your farming operation.

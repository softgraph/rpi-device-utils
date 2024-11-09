# Device Tree overlay to control PWM Fan

## Device Trees, overlays, and parameters

- See:
  - raspberrypi.com
    - Raspberry Pi Documentation
      - [Configuration](<https://www.raspberrypi.com/documentation/computers/configuration.html>)
        - [Device Trees, overlays, and parameters](<https://www.raspberrypi.com/documentation/computers/configuration.html#device-trees-overlays-and-parameters>)

## Thermal Management

- Thermal management is achieved in devicetree by describing the sensor hardware and the software abstraction of cooling devices and thermal zones required to take appropriate action to mitigate thermal overloads.

- The following node types are used to completely describe a thermal management system in devicetree:
  - **thermal-sensor**:
    - device that measures temperature, has SoC-specific bindings
  - **cooling-device**:
    - device used to dissipate heat either passively or actively
  - **thermal-zones**:
    - A `/thermal-zones` node is required in order to use the thermal framework to manage input from the various thermal zones in the system in order to mitigate thermal overload conditions. It does not represent a real device in the system, but acts as a container to link a thermal sensor device, platform-data regarding temperature thresholds and the mitigation actions to take when the temperature crosses those thresholds.
    - Each thermal zone node contains information about how frequently it must be checked, the sensor responsible for reporting temperature for this zone, one sub-node containing the various trip points for this zone and one sub-node containing all the zone cooling-maps.

### Thermal Sensor

| Node | Compatible with |
|-|-|
| `/soc/avs-monitor@xxxxxxxx/thermal/` | `brcm,bcm2711-thermal` |
| or ||
| `/soc/thermal@xxxxxxxx/` | `brcm,bcm2837-thermal` |

- See:
  - raspberrypi.com/linux/
    - devicetree/bindings/
      - thermal/
        - [brcm,avs-ro-thermal.yaml](<https://github.com/raspberrypi/linux/blob/rpi-6.6.y/Documentation/devicetree/bindings/thermal/brcm%2Cavs-ro-thermal.yaml>)
          - for `brcm,bcm2711-thermal`
        - [brcm,bcm2835-thermal.yaml](<https://github.com/raspberrypi/linux/blob/rpi-6.6.y/Documentation/devicetree/bindings/thermal/brcm%2Cbcm2835-thermal.yaml>)
          - for `brcm,bcm2837-thermal`

### Cooling Device

| Node | Compatible with |
|-|-|
| `/pwm-fan/` | `pwm-fan` |

- See:
  - raspberrypi.com/linux/
    - devicetree/bindings/
      - hwmon/
        - [pwm-fan.yaml](<https://github.com/raspberrypi/linux/blob/rpi-6.6.y/Documentation/devicetree/bindings/hwmon/pwm-fan.yaml>)

### Thermal Zones

| Node | Phandle |
|-|-|
| `/thermal-zones/cpu-thermal/` | `&cpu_thermal/` |
| `/thermal-zones/cpu-thermal/trips/` | `&thermal_trips/` |
| `/thermal-zones/cpu-thermal/trips/trip?/` ||
| `/thermal-zones/cpu-thermal/cooling-maps/` | `&cooling_maps/` |
| `/thermal-zones/cpu-thermal/cooling-maps/map?/` ||

- See:
  - raspberrypi.com/linux/
    - devicetree/bindings/
      - thermal/
        - [thermal-zones.yaml](<https://github.com/raspberrypi/linux/blob/rpi-6.6.y/Documentation/devicetree/bindings/thermal/thermal-zones.yaml>)

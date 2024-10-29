# Device Tree Overlay for PWM Fan Control

## Device Trees, overlays, and parameters

### References (`raspberrypi.com`)

- Configuration
  - Device Trees, overlays, and parameters  
    <https://www.raspberrypi.com/documentation/computers/configuration.html#device-trees-overlays-and-parameters>

## Thermal Bindings

There are five types of nodes involved to describe thermal bindings:

- thermal sensors:
  - devices which may be used to take temperature measurements.
- cooling devices:
  - devices which may be used to dissipate heat.
- trip points:
  - describe key temperatures at which cooling is recommended.
    The set of points should be chosen based on hardware limits.
- cooling maps:
  - used to describe links between trip points and cooling devices;
- thermal zones:
  - used to describe thermal data within the hardware;

### Thermal sensor devices

- Required property:
  - `#thermal-sensor-cells`

### Cooling device nodes

- Required property:
  - `#cooling-cells`

- For the details, see `fragment@2`

### Trip points

- Required property:
  - `temperature`
  - `hysteresis`
  - `type`

- For the details, see `fragment@4`

### Cooling device maps

- Required property:
  - `cooling-device`
  - `trip`
- Optional property:
  - `contribution`

- For the details, see `fragment@5`

### Thermal zone nodes

- Required property:
  - `polling-delay`
  - `polling-delay-passive`
  - `thermal-sensors`
  - `trips`
- Optional property:
  - `cooling-maps`
  - `coefficients`
  - `sustainable-power`

- For the details, see `fragment@3`

### References (`kernel.org`)

- devicetree/bindings/thermal/thermal.txt  
  <https://www.kernel.org/doc/Documentation/devicetree/bindings/thermal/thermal.txt>

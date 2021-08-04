# PyPCPanelPro

Python module to interact with a PCPanel pro device
This module requires `pyusb` in order to work, to install it go to https://github.com/pyusb/pyusb

---

# How to use the module

In order to use the module a new instance of `pcpro_panel` should be created.

```python
    new_panel = pcpro_panel()
```
The panel contains all the elements present on the physical device as attributes, 5 knob named k1 to k5, 5 buttons named b1 to b5, 4 sliders named s1 to s4, 4 labels named l1 to l4 and the logo named logo.

All of those elements except the logo has an attribute called `value`, the value attribute is automatically read and updated from the device, the value of knobs and sliders vary between 0 and 255 while buttons have value 1 if pressed otherwise 0.

## Knobs

The color is determined by the `'color'` attribute of the knob, the attribute itself is a list containing two color written in the typical web color code, the firs one is for when the knob is in the 0 position and the second for when the knobis in the 10 position.

```python
    new_panel.k1.color = ['#ff0000', '#0000ff']
```

Knobs have an attribute caller `color_mode` that indicates wich color mode to use, by default the mode is `'static'` but `'gradient'` is also available, if the color mode is set to static the only color displayed will be the send one.

## Labels

Labels have a `'color_mode'` attribute but it is present only for future proofing, at the moment the value can be only `'static'`, the only meaningful attribute is the `'color'` attribute that contains a color value in web color code.

```python
    new_panel.l1.color = '#880088'
```

## Sliders

Sliders like knobs has a `'color'` attribute that is composed of a list of two colors in web color codes and like the knobs the first is the color when the slider is at its minimum and the secon when at its maximum.

```python
    new_panel.s1.color = ['#ff0000', '#0000ff']
```

The available values for the `'color_mode'` attribute are `'static'` and `vol_gradient'`, if color_mode is set to static the color will be a gradient going from the firs  color to the second, if the color_mode is instead vol_gradient the color gradient remains the same but the illuminated part will reac only to the slider position

## Logo

The logo attribute `'color_mode'` can have values of `'static'`, `'rainbow'` or `'breath'`, each mode uses different attributes to display the desired effect, static mode uses the `color` attribute, rainbow mode uses the `brightness` and `speed` attributes and the breath mode uses `hue`, `brightness` and `speed` attributes.

The `color` attribute has as a value a color in the web color code format.

```python
    new_panel.logo.color = '#ffffff'
```

The `hue`, `brightness` and `speed` have a value ranging between `'00'` and `'ff'`, the value is a string of a hexadecimal value.

# Available functions

The `pcpro_panel` class has some available functions used to interact with the device, the `update_colors()` function, the  `print(tag)` function and the `toggle_lights` function.

The `update_colors()` function has to be invoked after the values of the attributes related to the colors on the panel are changed otherwise the color will remain the same.

```python
    new_panel.update_colors()
```

The  `print(tag)` function is used to print to terminal informations about the state of the `pcpro_panel` instance, the available tags are `colors` to display the color related information and `values` to display the values of the elements, the default value of tag is colors.

```python
    new_panel.print('colors')
    new_panel.print('values')
```

The `toggle_lights()` function is used to turn off the lights on the panel without altering the values of the attributes, this function automatically updates the lights so there is no need to use the `update_colors()` function.

```python
    new_panel.toggle_lights()
```

# Default panel attributes values

Each attribute has its own attributes, by default those are :

for knobs :

```python
    color_mode = 'static'
    color = ['#000000', '#000000']
    value = 0
    type = 'knob'
```

for buttons :

```python
    value = 0
    type = 'button
```

for  labels :

```python
    color_mode = 'static'
    color = '#000000'
    type = 'label'
```

for sliders :

```python
    color_mode = 'static'
    color = ['#000000', '#000000']
    value = 0
    type = 'slider'
```

for the logo :

```python
    color_mode = 'static'
    self.color = '#000000'
    self.type = 'logo'
    self.hue = '00'
    self.brightness = 'ff'
    self.speed = '89'
```

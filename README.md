# collectd-plugin-VMG3006-D70A-xDSL

## Supported hardware
This is a [collectd](https://collectd.org/) plugin for monitoring the
xDSL status of Zyxel VMG3006 VDSL/VDSL2-supervectoring modems.

I developed and tested it with the D70A-version (a VDSL2-Vectoring  
supervectoring modem for Germany) of this modem, but it might work as  
well with other variants.


## Supported parameters
This plugin reads the ***xDSL-status only***! \
It does not support reading things like interface-counters etc.

If your modem has a page like the one shown below, this plugin will
probably be able to read all status parameters of the paragraphs
"Data rate" , "Operation data / defect indication" and
"Error indicators".

![VMG3006-D70A-xDSL-page](https://media.githubusercontent.com/media/kettenbach-it/collectd-plugin-VMG3006-D70A-xDSL/master/images/screenshot.png)


## Dependencies
- collectd 4.9+

## Installation
1. `pip3 install collectd-plugin-VMG3006-xDSL`
2. Configure the plugin as shown below
3. Restart collectd

## Configuration
```
LoadPlugin python 
<Plugin python>
    Import "VMG3006_xDSL"

    <Module VMG3006_xDSL>
        URL "http://<ip_of_your_modem>"
        User "admin"
        Password "1234"
    </Module>
</Plugin>
````


## License
This project is licensed under the terms of the GPLv3 license.

## Build
`python setup.py sdist`

`twine upload dist/*`





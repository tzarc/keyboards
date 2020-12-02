# Djinn Split Keyboard

The Djinn is a 64-key split keyboard -- dual 4x7 with a 4-key thumb cluster. It also has a 5-way tactile switch under the thumb.

Extravagance-wise, it's got audio, encoder support, per-key RGB and RGB underglow... and a 240x320 LCD. And for the safety conscious, it has ESD protection, transient voltage suppression, and polarity protection on both the USB connector as well as the split transport.

It also runs [QMK](https://qmk.fm/)! It's just.... not in the main repo, yet.

![Djinn](https://i.imgur.com/iZmEG2e.jpg)

Unfortunately, the Djinn isn't currently supported in QMK's master, as it's running on hardware that's a bit too new. It's also intended to be used as a testbed for QMK features as well as one of the major drivers for upgrading ChibiOS. In due course it'll hit QMK master, but for now it needs to live outside.

The QMK firmware branch required to build the Djinn can be found here: [tzarc/qmk_firmware/djinn](https://github.com/tzarc/qmk_firmware/tree/djinn).

Building can be done with:

```
make tzarc/djinn:default
```

## Rev1

BOM: [Click](Rev1/Djinn-BOM.md)

![Djinn PCB](https://i.imgur.com/tDgQIRd.png)
![Djinn PCB](https://i.imgur.com/HIBmkHB.jpg)
![Djinn PCB](https://i.imgur.com/NRcNDYy.jpg)

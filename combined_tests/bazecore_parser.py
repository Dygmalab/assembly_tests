#!/usr/bin/env python3
import json

class ParseBazeCoreJSON():

    def __init__(self, filename):
        # load the layer file
        with open(filename) as fh:
            config = json.load(fh)

            assert 'keymap' in config
            assert 'onlyCustom' in config['keymap']
            assert 'palette' in config
            assert 'colormap' in config
            self.config = config

    # keymap
    def parse_keymap(self):
        api_message = "keymap.custom"
        assert len(self.config['keymap']['custom']) == 10
        for layer in self.config['keymap']['custom']:
            assert len(layer) == 80
            for key in layer:
                api_message += " " + str(key['keyCode'])
    
        return api_message

    # onlyCustom
    def parse_onlyCustom(self):
        api_message = "keymap.onlyCustom"
        if self.config['keymap']['onlyCustom']:
            api_message += " 1"
        else:
            api_message += " 0"

        return api_message

    # palette
    def parse_palette(self):
        api_message = "palette"
        assert len(self.config['palette']) == 16
        for rgb in self.config['palette']:
            for colour in 'rgb':
                api_message += " " + str(rgb[colour])

        return api_message

    # layer colours
    def parse_layerColours(self):
        api_message = "colormap.map"
        assert len(self.config['colormap']) == 10
        for layer in self.config['colormap']:
            assert len(layer) == 132 # number of LEDs in the raise (underglow + backlight)
            for key in layer:
                api_message += " " + str(key)

        return api_message

    def parse_all(self):
        api_messages = []
        api_messages.append(self.parse_keymap())
        api_messages.append(self.parse_onlyCustom())
        api_messages.append(self.parse_palette())
        api_messages.append(self.parse_layerColours())
        return api_messages

if __name__ == '__main__':
    parser = ParseBazeCoreJSON('Layers.json')
    print(parser.parse_all())

#! /bin/python
"""
Author: mcncm, 2019

Methods:
"Play", "Pause", "PlayPause", "Next", "Previous"
"""

import sys
import dbus

bus_name = "org.mpris.MediaPlayer2.spotify"
object_path = "/org/mpris/MediaPlayer2"

# used for "Play", "Pause", etc.
player_interface = "org.mpris.MediaPlayer2.Player"

# used for "Metadata".
properties_interface = "org.freedesktop.DBus.Properties"

bus = dbus.SessionBus()
proxy = bus.get_object(bus_name, object_path)

def spotify_dbus_call(method, *args, dbus_interface=player_interface):
    return getattr(proxy, method)(*args, dbus_interface=dbus_interface)

def get_metadata():
    """Metadata about currently-playing track
    """
    metadata = spotify_dbus_call("Get", player_interface,
            "Metadata", dbus_interface=properties_interface)

    return {key.split(':')[-1]: value for key, value in metadata.items()}

if __name__ == '__main__':
    if sys.argv[1] in ["Play", "Pause", "PlayPause", "Next", "Previous"]:
        spotify_dbus_call(sys.argv[1])
    elif sys.argv[1] in ["Metadata"]:
        print(get_metadata())

#!/usr/bin/python3
#
# Notifier.py
# Catch Ubuntu notifications and send them through espeak
# Part of the worthless Ubuntu hacks series :-)
# I have visual limitations, and on Ubuntu the notifications are on top
# and are often too small and disappear too quickly to see.
# This hack speaks them instead.  Firs,t it lets me know they're there,
# and, it's useful if a server is an office with one of your co-workers.
# After all, they did something to deserve this right?
#
# I know espeak leaves much to be desired, but it's easily added.
# Still feel free to replace with Festival or whatever you like.
#
# This code comes with no warranty of any kind.  I am too
# embarrassed to admit I had anything to do with it.
# Feel free to use, alter, destroy etc. this code as you will.
#
#
# John Antypas (ja@antypas.net)
# But I wasn't anywhere near this code --- honest!
#

# First get the dbus stuff
import gi
from gi.repository import GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
#
# Now get the stuff we need to call espeak
#
from subprocess import call
#
#
#
# The list of appnames we'll speak since we don't want to announce *every* notification
#
# spokenapps is the case-insensitive list of app names we'll speak IF
# that app does not have a summary in excludesummary
# speaker is the process name (espeak right now) we'll invoke
#
#
spokenapps = ["beeper", "notify-send"]
excludesummary = ["winbox"]
speaker = "espeak"
#
# This funcion does all the work by putting the attributes into a dictionary
# (Thank you Stackoverflow)
#
def print_notification(bus, message):
  keys = ["app_name", "replaces_id", "app_icon", "summary",
          "body", "actions", "hints", "expire_timeout"]
  args = message.get_args_list()
  if len(args) == 8:
    notification = dict([(keys[i], args[i]) for i in range(8)])
    # Build our Englush message
    msg = "Notification sent by: "+notification["app_name"]+". Message was: "+ notification["summary"]+":"+notification["body"]
    # Speak it
    # Technically, we could add other espeak attributes here in case you wanted to speak with an American or
    # West-Indies English accent for example, or speak in another language, but that's up to you.
    #
    if (notification["app_name"].lower()) in spokenapps:
        if notification["summary"].lower() not in excludesummary:
            call([speaker, msg])

# Attach out hook to DBUS for notificatons only
loop = DBusGMainLoop(set_as_default=True)
session_bus = dbus.SessionBus()
session_bus.add_match_string("type='method_call',interface='org.freedesktop.Notifications',member='Notify',eavesdrop=true")
session_bus.add_message_filter(print_notification)

GLib.MainLoop().run()


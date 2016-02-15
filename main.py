#!/usr/bin/env python3

"""
This is a simple AppIndicator for Ubuntu used as an introduction to 
AppIndicators. Retrieves a random Pokemon name from a public API.
"""

import json
import os
import random
import signal
import string
import urllib.request

from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import Notify


APPINDICATOR_ID = "example-pokemon-appindicator"


def main():
	indicator = AppIndicator3.Indicator.new(
			APPINDICATOR_ID,
			os.path.abspath("pokeball-icon.svg"),
			AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
	indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
	indicator.set_menu(menu_build())
	Notify.init(APPINDICATOR_ID)

	Gtk.main()


def menu_build():
	"""Return a Gtk+ menu."""
	menu = Gtk.Menu()

	item_pokemon = Gtk.MenuItem("Random Pokemon")
	item_pokemon.connect('activate', pokemon_get)
	menu.append(item_pokemon)

	item_quit = Gtk.MenuItem("Quit")
	item_quit.connect('activate', quit)
	menu.append(item_quit)

	menu.show_all()
	
	return menu


def pokemon_get(source):
	"""Output a random Pokemon's name via a notification."""

	# As of today, there are 721 Pokemon, so we choose between 1 and 721.
	url = "http://pokeapi.co/api/v2/pokemon/" + str(random.randint(1,721))
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	pokemon_name = json.loads(response.read().decode('utf-8'))['name']
	pokemon_name = string.capwords(pokemon_name) # make it look nice
	
	Notify.Notification.new("<b>A wild Pokemon appeared</b>", 
							pokemon_name,
							None).show()
def quit(source):
	Notify.uninit()
	Gtk.main_quit()


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()

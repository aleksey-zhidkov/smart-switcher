#!/usr/bin/python

import os
import sys

def active_window():
	f = os.popen('xdotool getactivewindow')
	return f.read().strip()

def current_desktop():
	f = os.popen('xdotool get_desktop')
	return f.read().strip()

def windows_by_class(current_desktop, windowclass):
	f = os.popen('xdotool search --desktop ' + current_desktop + ' --class ' + windowclass)
	return f.read().strip().split('\n')

def all_windows(current_desktop):
	f = os.popen('xdotool search --desktop ' + current_desktop + ' .')
	return f.read().strip().split('\n')

def activate_window(window_id):
	os.system('xdotool windowactivate ' + window_id)

def minimize_window(window_id):
	os.system('xdotool windowminimize ' + window_id)

def toggle_other_window(windowclasses):
	cd = current_desktop()
	aw = active_window()
	all_wins = all_windows(cd)

	spec_windows = []
	for windowclass in windowclasses:
		spec_windows.extend(windows_by_class(cd, windowclass))

	for window in all_wins:
		if window not in spec_windows and window != aw:
			activate_window(window)
			return

	# if we here, so there only one 'other' window and it is active
	minimize_window(aw)


def toggle_window_class(windowclass):
	cd = current_desktop()
	windows = windows_by_class(cd, windowclass)
	aw = active_window()

	if len(windows) == 1:
		if windows[0] == aw:
			minimize_window(windows[0])
		else:
			activate_window(windows[0])
	else:
		for window in windows:
			if window != aw:
				activate_window(window)
				return


if sys.argv[1] == '-n':
	toggle_other_window(sys.argv[2:])
else:
	toggle_window_class(sys.argv[1])
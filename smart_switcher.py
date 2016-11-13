#!/usr/bin/python

import os
import subprocess
import sys

def active_window():
	f = os.popen('xdotool getactivewindow')
	return f.read().strip()

def current_desktop():
	f = os.popen('xdotool get_desktop')
	return f.read().strip()

def windows_by_class(current_desktop, windowclass):
	f = os.popen('xdotool search --desktop ' + current_desktop + ' --class "' + windowclass + '"')
	return [a for a in f.read().strip().split('\n') if len(a) > 0]

def all_windows(current_desktop):
	f = os.popen('xdotool search --desktop ' + current_desktop + ' .')
	return f.read().strip().split('\n')

def activate_window(window_id):
	os.system('xdotool windowactivate ' + window_id)

def minimize_window(window_id):
	os.system('xdotool windowminimize ' + window_id)

def toggle_other_window(windowclass):
	cd = current_desktop()
	all_wins = all_windows(cd)
	if len(all_wins) == 0:
		return

	aw = active_window()
	if len(aw) == 0:
		activate_window(all_wins[0])
		return

	spec_windows = windows_by_class(cd, windowclass)

	for window in all_wins:
		if window not in spec_windows and window != aw:
			activate_window(window)
			return

	# if we here, so there only one 'other' window and it is active
	minimize_window(aw)


def toggle_window_class(windowclass, runCmd):
	cd = current_desktop()
	windows = windows_by_class(cd, windowclass)
	aw = active_window()

	if len(windows) == 0 and runCmd != None:
		subprocess.Popen([runCmd], stdin=None, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	elif len(windows) == 1:
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
	toggle_other_window('|'.join(map(lambda x:"(" + x + ")", sys.argv[2:])))
else:
	toggle_window_class(sys.argv[1], (sys.argv[2] if len(sys.argv) == 3 else None))

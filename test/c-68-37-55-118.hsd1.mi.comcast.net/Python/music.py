#!/usr/bin/python

import pyglet

sound = pyglet.media.load('mysound.mp3', streaming=False)
sound.play()
pyglet.app.run()

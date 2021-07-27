import board
import digitalio
from time import sleep

import usb_midi

import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

import adafruit_ble_midi

import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.midi_message import MIDIMessage, MIDIUnknownEvent
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.timing_clock import TimingClock

from random import randint

led = digitalio.DigitalInOut(board.BLUE_LED)
led.direction = digitalio.Direction.OUTPUT

# Setup the BLE service and adverstisement
midi_service = adafruit_ble_midi.MIDIService()
advertisement = ProvideServicesAdvertisement(midi_service)

# Set up BLE connection
ble = adafruit_ble.BLERadio()
if ble.connected:
  for c in ble.connections:
    c.disconnect()

# MIDI setup
midi = adafruit_midi.MIDI(midi_out=midi_service, out_channel=0)

# USB MIDI Sending on channel 1 as the OP-Z routes it to the active instrument
midi2 = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=1, in_channel=0,midi_in=usb_midi.ports[0])

# Start the BLE things
ble.start_advertising(advertisement)

tick = 0.01

counter = 0
note = NoteOn(127, randint(64,127))

# Main loop
while True:
  led.value = False

  # print("Connected")
  led.value = ble.connected
  # Delay after connection a bit to settle
  # sleep(1) 

  msg_in = midi2.receive()
  # print(msg_in)
  if msg_in is not None and ble.connected:
    if isinstance(msg_in, TimingClock):
      # we can send some random note
      if counter == 0:
        midi.send(NoteOff(note.note))
        midi2.send(NoteOff(note.note))
        note = NoteOn(127, randint(64,127))
        midi.send(note)
        midi2.send(note)
        counter = 20
      # decrement the counter on all runs
      counter -= 1

  # if ble.connected:
  #   midi.send(NoteOn(127))
  # midi2.send(NoteOn(64))

  # sleep(1)
  # if ble.connected:
  #   midi.send(NoteOff(127))
  # midi2.send(NoteOff(64))

  sleep(tick)


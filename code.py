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

# 12 notes over all. to transpose one octave add 0x0C. Start with C-1
major_scale_0 = (
  0x00,
  0x02,
  0x04,
  0x05,
  0x07,
  0x09,
  0x0B,
)

major_scale_1 = [n + 0x0C for n in major_scale_0] # C0
major_scale_2 = [n + 0x0C for n in major_scale_1] # C1
major_scale_3 = [n + 0x0C for n in major_scale_2] # C2
major_scale_4 = [n + 0x0C for n in major_scale_3] # C3
major_scale_5 = [n + 0x0C for n in major_scale_4] # C4
major_scale_6 = [n + 0x0C for n in major_scale_5] # C5
major_scale_7 = [n + 0x0C for n in major_scale_6] # C6


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
midi2 = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0, in_channel=0,midi_in=usb_midi.ports[0])

# Start the BLE things
ble.name = "MIDIThing"
ble.start_advertising(advertisement)

tick = 0.01

counter = 0
note = NoteOn(randint(64,127), randint(64,127))

def send_rand_note():
  global note
  midi.send(NoteOff(note.note))
  midi2.send(NoteOff(note.note))
  sleep(tick)
  # note = NoteOn(major_scale_4[randint(0,6)], randint(64,127))
  note.note = major_scale_5[randint(0,6)]
  note.velocity = randint(64,127)
  midi.send(note)
  midi2.send(note)

# Main loop
while True:
  led.value = False

  # print("Connected")
  led.value = ble.connected
  # Delay after connection a bit to settle
  # sleep(1) 

  msg_in = midi2.receive()
  # print(msg_in)

  send_rand_note()
  print(note)
  sleep(0.1)
  midi.send(NoteOff(note.note))
  midi2.send(NoteOff(note.note))
  sleep(0.0)
  # if msg_in is not None:
  #   if isinstance(msg_in, TimingClock):
  #     # we can send some random note
  #     if counter == 0:

  #       counter = 20
  #     # decrement the counter on all runs
  #     counter -= 1

  # if ble.connected:
  #   midi.send(NoteOn(127))
  # midi2.send(NoteOn(64))

  # sleep(1)
  # if ble.connected:
  #   midi.send(NoteOff(127))
  # midi2.send(NoteOff(64))

  sleep(tick)


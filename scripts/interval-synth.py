#!/usr/bin/env python

import argparse
from copy import deepcopy
from music21 import note, stream, midi, chord

__author__ = 'artonson'


def parse_options():
    parser = argparse.ArgumentParser(description='Synthesize specified intervals.')

    parser.add_argument('-t', '--note-duration', default='whole', help='duration of note.')
    parser.add_argument('-r', '--rest-duration', default='whole', help='duration of rest.')
    parser.add_argument('--repeats', type=int, help='number of times to repeat synthesis.')
    parser.add_argument('-c', '--chord', action='store_true', default=False, help='synthesize duration via chords.')

    notes_group = parser.add_argument_group('notes', 'Specify concrete notes to play.')
    notes_group.add_argument('--n1', required=True, help='first note of first interval')
    notes_group.add_argument('--n2', required=True, help='second note of first interval')
    notes_group.add_argument('--n3', required=True, help='first note of second interval')
    notes_group.add_argument('--n4', required=True, help='second note of second interval')

    return parser.parse_args()


def synthesize(options):
    n1 = note.Note(options.n1, type=options.note_duration)
    n2 = note.Note(options.n2, type=options.note_duration)
    n3 = note.Note(options.n3, type=options.note_duration)
    n4 = note.Note(options.n4, type=options.note_duration)
    r = note.Rest(type=options.note_duration)

    s = stream.Stream()
    for repeat in xrange(options.repeats):
        if options.chord:
            c1 = chord.Chord([n1, n2])
            c2 = chord.Chord([n3, n4])
            s.append(deepcopy(c1))
            s.append(deepcopy(r))
            s.append(deepcopy(c2))
            s.append(deepcopy(r))
        else:
            for n in [n1, n2, r, n3, n4, r]:
                s.append(deepcopy(n))

    s.show('text')

    player = midi.realtime.StreamPlayer(s)
    player.play()


if __name__ == '__main__':
    options = parse_options()
    synthesize(options)
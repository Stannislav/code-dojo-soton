var instrument = Synth.createInstrument('edm');

var setInstrument = function(name) {
    instrument = Synth.createInstrument(name.value);
};

var time = 2;

var sounds = {
    '00': {
        note: 'B',
        val: 2,
        time: 2
    },
    '01': {
        note: 'C',
        val: 2,
        time: 2
    },
    '02': {
        note: 'D',
        val: 2,
        time: 2
    },
    '03': {
        note: 'E',
        val: 2,
        time: 2
    },
    '10': {
        note: 'B',
        val: 3,
        time: 2
    },
    '11': {
        note: 'C',
        val: 3,
        time: 2
    },
    '12': {
        note: 'D',
        val: 3,
        time: 2
    },
    '13': {
        note: 'E',
        val: 3,
        time: 2
    },
    '20': {
        note: 'B',
        val: 4,
        time: 2
    },
    '21': {
        note: 'C',
        val: 4,
        time: 2
    },
    '22': {
        note: 'D',
        val: 4,
        time: 2
    },
    '23': {
        note: 'E',
        val: 4,
        time: 2
    },
    '30': {
        note: 'B',
        val: 5,
        time: 2
    },
    '31': {
        note: 'C',
        val: 5,
        time: 2
    },
    '32': {
        note: 'D',
        val: 5,
        time: 2
    },
    '33': {
        note: 'E',
        val: 5,
        time: 2
    }
};

var keypress = function(thing) {
    var id = thing.id.toString();
    console.log(id);
    instrument.play(sounds[id].note, sounds[id].val, sounds[id].time);
};

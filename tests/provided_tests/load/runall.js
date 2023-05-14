import smallConcert from './small-concert.js';
import presale from './presale.js';
import general from './general.js';
import seating from './seating.js';
import evening from './evening.js';

export default function() {
    smallConcert();
    presale();
    general();
    seating();
    evening();
}

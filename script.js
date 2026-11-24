// giga jackal!! literally just a lil virtual white jackal pup (anubis vibes) made w jquery

$(function() { // this just waits til the whole page is loaded bc otherwise jquery cant find any of the stuff on the page

  // show the starting stats on the page right away
  checkAndUpdatePetInfoInHtml();

  // hooking each button up to its function (the functions are all down below)
  $('.treat-button').click(clickedTreatButton);
  $('.play-button').click(clickedPlayButton);
  $('.exercise-button').click(clickedExerciseButton);
  $('.nap-button').click(clickedNapButton); // the new one i added
  $('.feast-button').click(clickedFeastButton); // HW10: the button with the intentional bug
});

// my pet!! name (string), weight (number), happiness (number) + energy (number) which i added bc of the nap button
var pet_info = { name: "Anubis", weight: 20, happiness: 50, energy: 60 };

// limits so nothing goes crazy. happiness + energy are on 0-100 bars
var MAX_STAT = 100;
var MIN_WEIGHT = 1; // a pup cant weigh 0 pounds lol so 1 is the lowest

// random lil comments for each action, one gets picked every click so he doesnt say the same thing 50 times
var comments = {
  treat: [
    "nom nom nom!! offering accepted",
    "is that a golden bone?? i love u",
    "yum!! can i have another one"
  ],
  play: [
    "ball!! ball!! throw it again pls",
    "desert zoomies!! catch me if u can",
    "that was so fun awoo"
  ],
  exercise: [
    "huff... puff... that was a LONG run across the dunes",
    "my paws are tired but im still happy",
    "do we rly have to do more laps around the pyramid"
  ],
  nap: [
    "zzz... dreaming about chasing scarabs...",
    "ahh a warm sunny nap, i feel brand new",
    "*yawn* five more mins pls, guarding stuff is hard work"
  ],
  tooTired: [
    "im too sleepy for that... can we nap first",
    "*flops on the floor* no energy left"
  ],
  tooSkinny: [
    "im already lean enough, no more laps"
  ]
};

function clickedTreatButton() {
  // treat = happier + heavier (+ a tiny bit of energy bc snacks)
  pet_info.happiness += 5;
  pet_info.weight += 1;
  pet_info.energy += 3;
  petSays(randomFrom(comments.treat));
}

function clickedPlayButton() {
  // playing takes energy so if hes wiped out he asks for a nap instead
  if (pet_info.energy < 10) {
    petSays(randomFrom(comments.tooTired));
    return;
  }
  // play = way happier, lose a lil weight, use some energy
  pet_info.happiness += 8;
  pet_info.weight -= 1;
  pet_info.energy -= 10;
  petSays(randomFrom(comments.play));
}

function clickedExerciseButton() {
  if (pet_info.energy < 15) {
    petSays(randomFrom(comments.tooTired));
    return;
  }
  if (pet_info.weight <= MIN_WEIGHT) {
    petSays(randomFrom(comments.tooSkinny));
    return;
  }
  // exercise = less happy (hes tired lol), lose weight, use more energy
  pet_info.happiness -= 6;
  pet_info.weight -= 2;
  pet_info.energy -= 15;
  petSays(randomFrom(comments.exercise));
}

// NEW BEHAVIOR for the NEW button: napping gives a bunch of energy back and makes him a lil happier.
// weight doesnt change
function clickedNapButton() {
  pet_info.energy += 25;
  pet_info.happiness += 2;
  petSays(randomFrom(comments.nap));
}

// HW10 DEBUGGING DEMO -- INTENTIONAL BUG (see assets/ PDF, section 4)
// Feast gives him several treats at once. Expected: 3 treats => weight 20 -> 23.
// Actual: weight shows "203" because .val() returns a STRING, and number + string = string concatenation.
// FIX (apply it live in the Sources panel, then Ctrl/Cmd+S):
//   var treats = parseInt($('.feast-input').val(), 10);
function clickedFeastButton() {
  var treats = $('.feast-input').val();      // <-- BUG: "3" (string), not 3 (number)
  pet_info.weight += treats;                 // 20 + "3"  ->  "203"
  pet_info.happiness += treats * 2;          // * forces a number, so this line "works" and hides the problem
  pet_info.energy += 5;
  petSays('feast time!! ' + treats + ' treats, best day ever');
}

function checkAndUpdatePetInfoInHtml() {
  checkWeightAndHappinessBeforeUpdating();
  updatePetInfoInHtml();
}

// this is the bug fix: keeps every number in its allowed range so nothing can ever go below zero (or past 100)
function checkWeightAndHappinessBeforeUpdating() {
  if (pet_info.weight < MIN_WEIGHT) { pet_info.weight = MIN_WEIGHT; }
  if (pet_info.happiness < 0)       { pet_info.happiness = 0; }
  if (pet_info.happiness > MAX_STAT){ pet_info.happiness = MAX_STAT; }
  if (pet_info.energy < 0)          { pet_info.energy = 0; }
  if (pet_info.energy > MAX_STAT)   { pet_info.energy = MAX_STAT; }
}

// puts whatever is currently in pet_info onto the page
function updatePetInfoInHtml() {
  $('.name').text(pet_info['name']);
  $('.weight').text(pet_info['weight']);
  $('.happiness').text(pet_info['happiness']);
  $('.energy').text(pet_info['energy']);

  /* jQuery method #1: .width()
     .width(value) sets how wide an element is. since happiness + energy are 0-100
     i just pass in the number + "%" (like "60%") so the colored bar fills that much
     of the grey bar behind it. so every time the numbers change the bars grow
     or shrink w them. */
  $('.happiness-bar').width(pet_info.happiness + '%');
  $('.energy-bar').width(pet_info.energy + '%');
}

// shows the pets comment after a button press. no alert() or console.log() like the assignment said!
function petSays(message) {
  checkAndUpdatePetInfoInHtml();

  // 1) put the comment in the speech bubble over his head
  $('#speech').text(message);

  /* jQuery method #2: .prepend()
     .prepend(content) sticks new stuff at the very START inside an element
     (.append() is the opposite, it puts stuff at the end). so every new
     comment becomes the first <li> in the diary list and the newest one is
     always on top. */
  $('#log').prepend('<li><strong>' + pet_info.name + ':</strong> ' + message + '</li>');

  // keep the diary short: once theres more than 6 entries, delete the oldest one at the bottom
  // (plain javascript on purpose so my only new jquery methods are the two above)
  var entries = document.querySelectorAll('#log li');
  if (entries.length > 6) {
    entries[entries.length - 1].remove();
  }

  hopAround();
}

// extra: makes him hop every click by replaying the css bounce animation
function hopAround() {
  var pup = $('.pet-image')[0];       // grabs the normal DOM element out of the jquery object
  pup.classList.remove('bounce');     // take the class off...
  void pup.offsetWidth;               // ...force the browser to recalc so it forgets the old animation...
  pup.classList.add('bounce');        // ...then put it back so the animation plays again
}

// picks a random thing out of a list
function randomFrom(list) {
  return list[Math.floor(Math.random() * list.length)];
}

# giga jackal 🐺 [https://jakibugarin517-dev.github.io/Project-2/](https://jakibugarin517-dev.github.io/hw10-devtools/)

this is my giga pet project for comp 484. its a lil virtual white jackal pup named Anubis. u can feed him, play w him, exercise him, or put him down for a nap and he literally talks back to u after every click.

the image is my own art!

## how to run it

1. unzip the folder
2. open `index.html` in chrome
3. thats it, just click the buttons

(it needs internet bc jquery loads from a link)

## what's in the folder

- `index.html` = the page layout
- `style.css` = all the colors + looks
- `script.js` = all the pet stuff (the brain)
- `images/jackal.png` = my art

## what each button does

| button | happiness | weight | energy |
|---|---|---|---|
| 🦴 treat | up | up | up a tiny bit |
| 🎾 play | way up | down | down |
| 🏃 exercise | down | down | down more |
| 😴 nap (new!) | up a lil | same | way up |

if his energy is too low he's too tired to play or exercise and he'll tell u he needs a nap instead.

## the assignment 

- **pet_info object**: has name, weight, happiness (+ energy that i added)
- **button behaviors**: treat, play, exercise all do what the assignment says
- **bug fix**: weight, happiness and energy can never go below zero (happiness + energy also stop at 100)
- **new button + behavior**: nap, gives energy back. the energy stat is right under happiness
- **notification**: he talks in a speech bubble + a diary list. no `alert()` or `console.log()`
- **new image**: my own jackal art

## my two jquery methods

1. **`.width()`** = sets how wide an element is. i use it to make the happiness + energy bars fill up to a % of the grey bar
2. **`.prepend()`** = adds stuff at the very start of an element. i use it so the newest diary message is always on top

(both are explained in the comments in `script.js` too)

## extra stuff i did

- he hops every time u click a button
- energy system, so he gets too tired to play
- random comments so he doesnt say the same thing every time
- a diary that keeps the last 6 messages
- desert / egyptian color theme

## things i used

- html, css, javascript
- jquery 2.2.1

---

# HW10: Chrome DevTools additions

This repo is a copy of Project 2 with debugging demos added.

- `devtools-demo.js`: console.info/log/warn/error/table/group/%c demos + 404, TypeError and Violation triggers (buttons in the "DevTools Lab" section of the page)
- `script.js`: new **Feast** button with an intentional bug (`.val()` returns a string, so weight becomes `203` instead of `23`) used for the Sources-panel debugging walkthrough
- `screenshots/`: put screenshots here (names listed in `build_pdf.py`)
- `build_pdf.py`: builds `assets/HW10-DevTools-Report.pdf` from the screenshots
- `assets/HW10-DevTools-Report.pdf`: the report

Run it from a server (not file://) so the 404s show up as 404s: `python3 -m http.server` then open http://localhost:8000

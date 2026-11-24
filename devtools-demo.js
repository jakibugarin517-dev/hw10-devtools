// HW10 - Chrome DevTools demos. Every function here is triggered by a button in the "DevTools Lab" section.
// All messages start with "[demo]" so they are easy to find with the Console text / regex filters.

// ---------- 1. Console message logging ----------

function demoInfo() {
  console.info('[demo] info: Anubis is awake, weight =', pet_info.weight);
  console.log('[demo] log: current pet_info object ->', pet_info);
}

function demoWarn() {
  console.warn('[demo] warn: energy is low (' + pet_info.energy + '). Anubis may be too tired to play.');
}

function demoError() {
  console.error('[demo] error: could not save pet_info (this is a fake error for the demo)');
}

function demoTable() {
  // array of objects -> nice table in the console
  var actions = [
    { button: 'treat',    happiness: '+5', weight: '+1', energy: '+3' },
    { button: 'play',     happiness: '+8', weight: '-1', energy: '-10' },
    { button: 'exercise', happiness: '-6', weight: '-2', energy: '-15' },
    { button: 'nap',      happiness: '+2', weight: '0',  energy: '+25' }
  ];
  console.log('[demo] table: what each button does');
  console.table(actions);
  console.table(pet_info); // an object works too
}

function demoGroup() {
  console.group('[demo] group: Anubis report card');
  console.info('name:', pet_info.name);
  console.info('weight:', pet_info.weight);
  console.group('[demo] nested group: mood');
  console.log('happiness:', pet_info.happiness);
  console.log('energy:', pet_info.energy);
  console.groupEnd(); // closes "mood"
  console.groupEnd(); // closes "report card"
}

function demoCustom() {
  // %c applies the CSS in the next argument to the text that follows it
  console.log(
    '%c[demo] 🐺 GIGA JACKAL %c custom styled message',
    'color:#fff; background:#2b2d5b; font-size:16px; font-weight:bold; padding:4px 10px; border-radius:6px;',
    'color:#e0a928; font-style:italic; font-size:14px;'
  );
}

// ---------- 2. Browser-logged messages ----------

function demo404() {
  // (a) missing JSON "API" file
  fetch('api/missing-pets.json')
    .then(function (res) {
      if (!res.ok) { console.warn('[demo] fetch finished but the server said:', res.status, res.statusText); }
    })
    .catch(function (err) { console.error('[demo] fetch failed:', err); });
  // (b) missing image
  var img = new Image();
  img.src = 'images/missing-jackal.png';
}

function demoTypeError() {
  // pet_info has no "favoriteToy" property, so it is undefined, and undefined.name throws a TypeError.
  // Intentionally NOT caught, so the browser logs "Uncaught TypeError".
  var toyName = pet_info.favoriteToy.name;
  console.log(toyName);
}

function demoViolation() {
  // Blocks the main thread for ~300ms inside a click handler. Chrome logs
  // "[Violation] 'click' handler took XXXms" (shown at the Verbose level).
  var end = Date.now() + 300;
  while (Date.now() < end) { /* busy wait on purpose */ }
}

// ---------- wiring ----------

$(function () {
  var demos = {
    info: demoInfo, warn: demoWarn, error: demoError, table: demoTable,
    group: demoGroup, custom: demoCustom,
    '404': demo404, typeerror: demoTypeError, violation: demoViolation
  };

  $('.lab-btn').on('click', function () {
    var name = $(this).data('demo');
    if (name === 'all') {
      ['info', 'warn', 'error', 'table', 'group', 'custom'].forEach(function (n) { demos[n](); });
    } else {
      demos[name]();
    }
  });
});

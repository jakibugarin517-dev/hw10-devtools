"""
Builds assets/HW10-DevTools-Report.pdf.

1. Take your screenshots and save them in screenshots/ using the exact file names below (.png or .jpg).
2. Run:  pip install reportlab pillow   then   python3 build_pdf.py
Any screenshot that is missing shows up as a dashed placeholder box so you can see what's left.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, Image, KeepTogether, Preformatted)

OUT = os.path.join("assets", "HW10-DevTools-Report.pdf")
SHOTS = "screenshots"
MAXW, MAXH = 6.5 * inch, 3.6 * inch

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=colors.HexColor("#2b2d5b"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=colors.HexColor("#2b2d5b"), spaceBefore=14)
H3 = ParagraphStyle("H3", parent=ss["Heading3"], spaceBefore=10, spaceAfter=2)
BODY = ParagraphStyle("B", parent=ss["BodyText"], leading=14)
CAP = ParagraphStyle("Cap", parent=ss["Italic"], fontSize=9, textColor=colors.grey, spaceAfter=8)
CODE = ParagraphStyle("Code", parent=ss["Code"], fontSize=8, leading=10, backColor=colors.HexColor("#f4f1ea"),
                      borderPadding=4, spaceAfter=6)

# (slot file name without extension, heading, explanation, caption)
SECTIONS = [
 ("Part 2.1 - Console Message Logging",
  "Implemented in <b>devtools-demo.js</b> and triggered from the DevTools Lab buttons on the page. "
  "Every message starts with <b>[demo]</b> so it can be found with the filters in Part 2.3.",
  [
   ("c1-info", "Log Info: console.info() / console.log()",
    "<font face='Courier'>console.info()</font> prints an informational message and "
    "<font face='Courier'>console.log()</font> prints the live <font face='Courier'>pet_info</font> object, which can be expanded in the console.",
    "Screenshot: Console after clicking the <i>info / log</i> button."),
   ("c2-warn", "Log Warning: console.warn()",
    "Shown with a yellow background and a warning icon. Used here to warn that Anubis' energy is low.",
    "Screenshot: Console after clicking the <i>warn</i> button."),
   ("c3-error", "Log Error: console.error()",
    "Shown in red with an error icon, plus a stack trace that points back to the line in devtools-demo.js.",
    "Screenshot: Console after clicking the <i>error</i> button."),
   ("c4-table", "Log Table: console.table()",
    "Displays an array of objects (what each button does to happiness, weight and energy) as a table, one row per object.",
    "Screenshot: Console showing the table output."),
   ("c5-group", "Log Group: console.group() / console.groupEnd()",
    "Groups related messages under a collapsible heading. A nested group is also shown. Each group is closed with <font face='Courier'>console.groupEnd()</font>.",
    "Screenshot: Console showing the expanded group (and nested group)."),
   ("c6-custom", "Log Custom: %c CSS-styled output",
    "<font face='Courier'>%c</font> in the first argument applies the CSS string passed as the next argument to the text after it. "
    "Two <font face='Courier'>%c</font> tags are used to give two different styles in one message.",
    "Screenshot: Console showing the styled message."),
  ]),
 ("Part 2.2 - Browser-Logged Messages",
  "These messages are produced by the browser itself, not by a console.* call. "
  "<b>Note:</b> the 404 only appears when the page is served over http(s) (GitHub Pages or "
  "<font face='Courier'>python3 -m http.server</font>). Opened as a file:// URL it logs net::ERR_FILE_NOT_FOUND instead.",
  [
   ("b1-404", "404 Network Error",
    "The 404 button requests <font face='Courier'>api/missing-pets.json</font> with fetch() and "
    "<font face='Courier'>images/missing-jackal.png</font> with an Image object. Neither file exists, so the browser logs "
    "<i>GET ... 404 (Not Found)</i> for each one. The same requests appear in red in the Network panel.",
    "Screenshot: Console showing both 404 messages."),
   ("b2-typeerror", "TypeError",
    "The TypeError button reads <font face='Courier'>pet_info.favoriteToy.name</font>. "
    "<font face='Courier'>favoriteToy</font> was never defined, so it is <i>undefined</i>, and reading a property of undefined throws "
    "<i>Uncaught TypeError: Cannot read properties of undefined (reading 'name')</i>.",
    "Screenshot: Console showing the uncaught TypeError and its stack trace."),
   ("b3-violation", "Violation (long-running event handler)",
    "The Violation button runs a busy loop for about 300 ms inside a click handler. Chrome logs "
    "<i>[Violation] 'click' handler took ...ms</i>. <b>Violations are hidden unless the Verbose level is enabled</b> in the log-level dropdown.",
    "Screenshot: Console with the Verbose level enabled showing the [Violation] message."),
  ]),
 ("Part 2.3 - Filtering Console Messages",
  "First click <b>run all</b>, the <b>404</b>, <b>TypeError</b> and <b>Violation</b> buttons so the console has a mix of message types.",
  [
   ("f1-level", "Filter by log level",
    "Use the log-level dropdown (Default levels) to show only Info, only Warnings, or only Errors. Show one screenshot per level or one showing the dropdown with Errors only.",
    "Screenshot: Log-level dropdown set so that only one level (e.g. Errors) is displayed."),
   ("f2-text", "Filter by text",
    "Type a keyword such as <font face='Courier'>group</font> or <font face='Courier'>[demo] warn</font> in the Filter box. Only messages containing that text remain.",
    "Screenshot: Filter box with a keyword and the matching messages only."),
   ("f3-regex", "Filter by regular expression",
    "Wrap a pattern in slashes, for example <font face='Courier'>/\\[demo\\] (warn|error)/</font> to show only the warn and error demo messages.",
    "Screenshot: Filter box containing a /regex/ and the matching results."),
   ("f4-source", "Filter by message source",
    "Use the Console sidebar (or <font face='Courier'>url:devtools-demo.js</font> in the filter box) to show only messages from "
    "devtools-demo.js, and <font face='Courier'>-url:devtools-demo.js</font> to hide them, leaving the browser/network messages such as the 404s.",
    "Screenshot: Console filtered by source, user script vs. browser/network."),
   ("f5-user", "Filter by user messages",
    "Click <b>User messages</b> in the Console sidebar. Only messages created by the page's own JavaScript (console.* calls) are listed; "
    "browser-generated messages (404, violations) are hidden.",
    "Screenshot: Console sidebar with 'user messages' selected."),
  ]),
 ("Part 2.4 - JavaScript Debugging Workflow (Sources Panel)",
  "<b>The bug:</b> the new <b>Feast</b> button should add the number of treats to Anubis' weight (3 treats: 20 &rarr; 23 pounds). "
  "Instead the page shows 203 pounds. The code is in <font face='Courier'>clickedFeastButton()</font> in script.js.",
  [
   ("d1-reproduce", "Step 1 - Reproduce the bug",
    "Leave the Feast input at 3 and click Feast. Weight is shown as 203 pounds instead of 23.",
    "Screenshot: Page showing the wrong weight (203) after clicking Feast."),
   ("d2-breakpoint", "Step 2 - Sources UI and line-of-code breakpoint",
    "DevTools &rarr; Sources &rarr; open script.js in the file navigator and click the line number of "
    "<font face='Courier'>pet_info.weight += treats;</font> to set a line-of-code breakpoint (blue marker).",
    "Screenshot: Sources panel with script.js open and the breakpoint set."),
   ("d3-scope", "Step 3a - Pause and inspect: Scope pane",
    "Click Feast again. Execution pauses on the breakpoint. In the Scope pane, under Local, <font face='Courier'>treats</font> is the string \"3\" "
    "(it has quotes), and under Global <font face='Courier'>pet_info.weight</font> is the number 20.",
    "Screenshot: Paused on the breakpoint with the Scope pane showing treats = \"3\"."),
   ("d4-watch", "Step 3b - Pause and inspect: Watch expressions",
    "Add watch expressions with the + button: <font face='Courier'>typeof treats</font> (shows \"string\"), "
    "<font face='Courier'>pet_info.weight + treats</font> (shows \"203\").",
    "Screenshot: Watch pane with the expressions and their values."),
   ("d5-console", "Step 3c - Pause and inspect: Console drawer",
    "Press Esc to open the Console drawer while still paused and evaluate expressions, e.g. "
    "<font face='Courier'>typeof treats</font>, <font face='Courier'>Number(treats)</font>, <font face='Courier'>pet_info.weight + Number(treats)</font> (23). "
    "This confirms that converting treats to a number is the fix.",
    "Screenshot: Console drawer open while paused, showing evaluated expressions."),
   ("d6-fix", "Step 4 - Apply a fix and verify",
    "Resume (F8), then edit the line in the Sources editor to "
    "<font face='Courier'>var treats = parseInt($('.feast-input').val(), 10);</font> and save with Ctrl/Cmd+S. "
    "Reload and click Feast: the weight is now 23. The same fix is committed to script.js.",
    "Screenshot: Edited code in Sources and the page now showing the correct weight (23)."),
  ]),
]

def slot_flowable(slot, caption):
    path = next((os.path.join(SHOTS, slot + e) for e in (".png", ".jpg", ".jpeg") if os.path.exists(os.path.join(SHOTS, slot + e))), None)
    if path:
        from PIL import Image as PI
        w, h = PI.open(path).size
        scale = min(MAXW / w, MAXH / h, 1.0 if w < MAXW else MAXW / w)
        img = Image(path, width=w * scale, height=h * scale)
        t = Table([[img]], colWidths=[MAXW])
        t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, colors.grey), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    else:
        t = Table([[Paragraph(f"<b>[ screenshot goes here ]</b><br/>screenshots/{slot}.png", BODY)]],
                  colWidths=[MAXW], rowHeights=[1.6 * inch])
        t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.red, None, (4, 3)),
                               ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return [t, Paragraph(caption, CAP)]

story = [
 Paragraph("HW10: Chrome DevTools in Project 2 (Giga Jackal)", H1),
 Paragraph("Name: ______________________ &nbsp;&nbsp; GitHub repo: ______________________", BODY),
 Spacer(1, 8),
 Paragraph("This document explains the DevTools techniques that were added to a copy of Project 2 and shows a screenshot for each one. "
           "Code: <b>devtools-demo.js</b> (console and browser-message demos), <b>script.js</b> (the intentional Feast bug), "
           "<b>index.html</b> (the DevTools Lab buttons and Feast control).", BODY),
]
for title, intro, items in SECTIONS:
    story += [PageBreak(), Paragraph(title, H2), Paragraph(intro, BODY)]
    for slot, head, text, cap in items:
        story.append(KeepTogether([Paragraph(head, H3), Paragraph(text, BODY), Spacer(1, 4)] + slot_flowable(slot, cap)))

os.makedirs("assets", exist_ok=True)
SimpleDocTemplate(OUT, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                  title="HW10 DevTools Report").build(story)
print("Wrote", OUT)

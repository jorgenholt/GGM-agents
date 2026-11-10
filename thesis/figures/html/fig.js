// Arrows for the HTML figures. Each arrow is attached to the real edges of two
// elements after the browser has laid them out, so nothing is placed by guesswork.
//
//   arrow("#a:r@0.3", "#b:l", { color: "agent", label: "suggestions", side: "above" })
//
// An end is "#id:side" with side t, r, b or l, and optionally "@f" for where along
// that side (0..1, default 0.5) or "@12mm" for a distance from its start (top or left).
// The path runs straight if the two ends line up, otherwise with right-angle bends.
// Options: color (a name from fig.css), dashed, both (heads at both ends), straight,
// label, at (0..1 along the path, default 0.5), side (above, below, left, right),
// mid (where to put the bend: mm from the figure's left or top, or "#id" to bend at its centre),
// dotted, width.

const MM = 96 / 25.4;
const NS = "http://www.w3.org/2000/svg";
const queue = [];

function css(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(`--${name}`).trim() || name;
}

function centre(sel, fig) {
  const f = fig.getBoundingClientRect(), r = document.querySelector(sel).getBoundingClientRect();
  return { x: r.left - f.left + r.width / 2, y: r.top - f.top + r.height / 2 };
}

function point(spec, fig) {
  // { x: "#a", y: "#b", dir: "r" }: x of a's centre, y of b's centre, pointing right (for lifelines)
  if (typeof spec === "object") {
    const x = typeof spec.x === "number" ? spec.x * MM : centre(spec.x, fig).x;
    const y = typeof spec.y === "number" ? spec.y * MM : centre(spec.y, fig).y;
    const d = { t: [0, -1], b: [0, 1], l: [-1, 0], r: [1, 0] }[spec.dir || "r"];
    return { x: x + (spec.dx || 0) * MM, y: y + (spec.dy || 0) * MM, d };
  }
  const [, id, side, at] = /^(#[\w-]+):([trbl])(?:@([\d.]+(?:mm)?))?$/.exec(spec) || [];
  if (!id) throw new Error(`Bad arrow end: ${spec}`);
  const el = document.querySelector(id);
  if (!el) throw new Error(`No element ${id}`);
  const f = fig.getBoundingClientRect(), r = el.getBoundingClientRect();
  const x0 = r.left - f.left, y0 = r.top - f.top;
  const along = (len) => (at == null ? len / 2 : at.endsWith("mm") ? parseFloat(at) * MM : parseFloat(at) * len);
  if (side === "t") return { x: x0 + along(r.width), y: y0, d: [0, -1] };
  if (side === "b") return { x: x0 + along(r.width), y: y0 + r.height, d: [0, 1] };
  if (side === "l") return { x: x0, y: y0 + along(r.height), d: [-1, 0] };
  return { x: x0 + r.width, y: y0 + along(r.height), d: [1, 0] };
}

function route(a, b, mid) {
  // mid: where to bend, as mm from the figure's edge or as the centre of an element
  const ah = a.d[0] !== 0, bh = b.d[0] !== 0;
  if (ah && bh) {
    if (Math.abs(a.y - b.y) < 0.5) return [a, { x: b.x, y: a.y }];
    const mx = mid == null ? (a.x + b.x) / 2 : typeof mid === "object" ? mid.x : mid * MM;
    return [a, { x: mx, y: a.y }, { x: mx, y: b.y }, b];
  }
  if (!ah && !bh) {
    if (Math.abs(a.x - b.x) < 0.5) return [a, { x: a.x, y: b.y }];
    const my = mid == null ? (a.y + b.y) / 2 : typeof mid === "object" ? mid.y : mid * MM;
    return [a, { x: a.x, y: my }, { x: b.x, y: my }, b];
  }
  return ah ? [a, { x: b.x, y: a.y }, b] : [a, { x: a.x, y: b.y }, b];
}

function pointAt(pts, t) {
  const segs = pts.slice(1).map((p, i) => Math.hypot(p.x - pts[i].x, p.y - pts[i].y));
  let left = segs.reduce((s, l) => s + l, 0) * t;
  for (let i = 0; i < segs.length; i++) {
    if (left <= segs[i] || i === segs.length - 1) {
      const k = segs[i] ? left / segs[i] : 0;
      return { x: pts[i].x + (pts[i + 1].x - pts[i].x) * k, y: pts[i].y + (pts[i + 1].y - pts[i].y) * k,
               horizontal: pts[i].y === pts[i + 1].y };
    }
    left -= segs[i];
  }
}

// how far (in line widths) the tip runs past the end of the line: (9 - 5) of 10 units of a 5.5-wide marker
const HEAD_BACK = (9 - 5) / 10 * 5.5;

function marker(svg, color) {
  const id = "head-" + color.replace(/[^\w]/g, "");
  if (!svg.querySelector("#" + id)) {
    const m = document.createElementNS(NS, "marker");
    // the line ends at refX, where the head is already wider than the line; the tip is HEAD_BACK further on
    Object.entries({ id, viewBox: "0 0 10 10", refX: 5, refY: 5, markerWidth: 5.5, markerHeight: 5.5,
                     orient: "auto-start-reverse", markerUnits: "strokeWidth" }).forEach(([k, v]) => m.setAttribute(k, v));
    const p = document.createElementNS(NS, "path");
    p.setAttribute("d", "M 0 1 L 9 5 L 0 9 L 2.2 5 Z");
    p.setAttribute("fill", color);
    m.append(p);
    svg.querySelector("defs").append(m);
  }
  return `url(#${id})`;
}

function arrow(from, to, opts = {}) { queue.push([from, to, opts]); }

// Small icons, written <i data-icon="gear"></i>; they take the colour of their panel.
const ICONS = {
  person: '<circle cx="12" cy="7.2" r="4.2"/><path d="M3.8 22c0-4.6 3.7-8.3 8.2-8.3s8.2 3.7 8.2 8.3z"/>',
  agent: '<circle cx="12" cy="12" r="11.5"/><path fill="#fff" d="M12 4.2c.8 5.2 2.6 7 7.8 7.8-5.2.8-7 2.6-7.8 7.8-.8-5.2-2.6-7-7.8-7.8 5.2-.8 7-2.6 7.8-7.8z"/>',
  gear: [0, 45, 90, 135, 180, 225, 270, 315].map((a) => `<rect x="10.3" y="1.2" width="3.4" height="5" rx=".7" transform="rotate(${a} 12 12)"/>`).join("") +
        '<circle cx="12" cy="12" r="7.4"/><circle cx="12" cy="12" r="2.9" fill="#fff"/>',
  doc: '<path d="M5 2h9.5L19 6.5V22H5z" fill="#fff" stroke="currentColor" stroke-width="1.6"/><path d="M14.5 2v4.5H19" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 11h8M8 14.5h8M8 18h5" stroke="currentColor" stroke-width="1.5"/>',
  sheet: '<rect x="2.5" y="3.5" width="19" height="17" rx="1.5" fill="#fff" stroke="currentColor" stroke-width="1.6"/><path d="M2.5 8.5h19M2.5 13.5h19M8.8 3.5v17M15.2 3.5v17" stroke="currentColor" stroke-width="1.2"/><rect x="2.5" y="3.5" width="19" height="5" rx="1.5"/>',
  ledger: '<rect x="4" y="2.5" width="16" height="19" rx="1.5" fill="#fff" stroke="currentColor" stroke-width="1.6"/><path d="M7.5 8l1.5 1.5 3-3M7.5 14l1.5 1.5 3-3" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M14 8.5h3M14 14.5h3" stroke="currentColor" stroke-width="1.5"/>',
  log: '<circle cx="12" cy="12" r="9.5" fill="#fff" stroke="currentColor" stroke-width="1.8"/><path d="M12 6.5V12l3.8 2.4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  lesson: '<path d="M12 2.5a6.5 6.5 0 0 0-3.8 11.8V17h7.6v-2.7A6.5 6.5 0 0 0 12 2.5z" fill="#fff" stroke="currentColor" stroke-width="1.6"/><path d="M9 19.5h6M10 22h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
  laptop: '<rect x="4" y="4" width="16" height="11" rx="1.2" fill="#fff" stroke="currentColor" stroke-width="1.8"/><path d="M1.5 18.5h21l-1.2 2H2.7z"/>',
  check: '<circle cx="12" cy="12" r="11"/><path d="M6.8 12.4l3.4 3.4 7-7.3" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
  clock: '<circle cx="12" cy="12" r="9.5" fill="#fff" stroke="currentColor" stroke-width="1.8"/><path d="M12 6.5V12l3.8 2.4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  loop: '<path d="M19.5 12a7.5 7.5 0 1 1-2.2-5.3" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/><path d="M20.5 3.2v6h-6z"/>',
  ship: '<path d="M2 15h20l-2.6 4.6H4.6z"/><rect x="5" y="10.5" width="11" height="4.5" rx="0.6"/><rect x="15" y="7" width="4" height="8"/><circle cx="7.5" cy="10.5" r="2.2" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="12.5" cy="10.5" r="2.2" fill="none" stroke="currentColor" stroke-width="1.4"/>',
  database: '<ellipse cx="12" cy="5.5" rx="8" ry="3" fill="#fff" stroke="currentColor" stroke-width="1.6"/><path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13" fill="#fff" stroke="currentColor" stroke-width="1.6"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" fill="none" stroke="currentColor" stroke-width="1.6"/>',
  chat: '<path d="M3 4.5h18v11.5H9.5L5 20v-4H3z" fill="#fff" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M7 8.8h10M7 12h6" stroke="currentColor" stroke-width="1.5"/>',
};
function icons() {
  document.querySelectorAll("i[data-icon]").forEach((i) => {
    const s = document.createElementNS(NS, "svg");
    s.setAttribute("viewBox", "0 0 24 24");
    s.setAttribute("fill", "currentColor");
    s.setAttribute("class", "icon " + (i.className || ""));
    s.innerHTML = ICONS[i.dataset.icon];
    i.replaceWith(s);
  });
  document.querySelectorAll("i[data-pixel]").forEach((i) => i.replaceWith(pixels(i.dataset.pixel, i.className)));
}

// Pixel avatars, written <i data-pixel="analyst"></i>. The analyst is a person; the agents are
// robots, each with its own hat. One character per pixel on a 14 x 14 grid, "." is empty.
const PALETTE = {
  h: "#4A3428", s: "#F2C9A4", e: "#2B2B2B", m: "#A8563F", o: "#E07A3F", O: "#B85E2B",   // the analyst
  p: "#8B7FF0", P: "#4A3DB8", d: "#2B2150", w: "#FFFFFF", l: "#CFC9FA", y: "#F2C14E",               // the agents
  c: "#1B8A9A", M: "#2D3E50", g: "#B9C7D6",                                          // code, GGM
  G: "#4E9A3E", D: "#3E7C31", q: "#A39274", k: "#2B2B2B", S: "#C9A227", u: "#8F7317",   // lessons, heuristics
};
const ROBOT = [
  "...PPPPPPPP...", "...PppppppP...", "...PddddddP...", "..lPdwddwdPl..", "...PddddddP...",
  "...PppppppP...", "...PPPPPPPP...", ".....PppP.....", "..PPPPPPPPPP..", "..PppppppppP..",
];
const HATS = {
  agent:       ["..............", "..............", "......ll......", "......PP......"],
  scenario:    ["......Pllll...", "......Plll....", "......P.......", "......P......."],
  data:        ["..............", "....PPPPPP....", "....PPyyPP....", "..PPPPPPPPPP.."],
  calibration: ["...ll....ll...", "....P....P....", ".....P..P.....", "......PP......"],
  results:     ["..............", ".PPPPPPPPPPPP.", "....PPPPPP..l.", "....PPPPPP..l."],
};
const SPRITES = {
  analyst: ["..............", "..............", "....hhhhhh....", "...hhhhhhhh...", "...hssssssh...",
            "...ssssssss...", "...ssessess...", "...ssssssss...", "...sssmmsss...", "....ssssss....",
            "......ss......", "..ooooOOoooo..", ".oooooooooooo.", ".oooooooooooo."],
  code: ["......cc......", "..cc.cccc.cc..", "..cccccccccc..", "...cccccccc...", ".ccccc..ccccc.", ".cccc....cccc.", "cccc......cccc",
         "cccc......cccc", ".cccc....cccc.", ".ccccc..ccccc.", "...cccccccc...", "..cccccccccc..", "..cc.cccc.cc..", "......cc......"],
  ggm: ["..............", "..............", ".MMMMMMMMMMMM.", ".MggggggggggM.", ".MggggMMggggM.", ".MggggMMgMMgM.", ".MgMMgMMgMMgM.",
        ".MgMMgMMgMMgM.", ".MggggggggggM.", ".MMMMMMMMMMMM.", "......MM......", "......MM......", "....MMMMMM....", ".............."],
  lessons: ["............qq", "...........qqq", "...........qq.", "...DDDDDDDqqq.", "...DGGGGGqqq..", "...DGGwwGqq...", "...DGGGGkGD...", "...DGGGkGGD...", "...DGGGGGGD...", "...DGGGGGGD...", "...DGGGGGGD...", "...DGGGGGGD...", "...DwwwwwwD...", "...DDDDDDDD..."],
  heuristics: ["..............", "...uuuuuuuu...", "...uwwwwwwu...", "...uwSSSSwu...", "...uwwwwwwu...", "...uwSSSwwu...", "...uwwwwwwu...",
               "...uwSSSSwu...", "...uwwwwwwu...", "...uwSSwwwu...", "...uwwwwwwu...", "...uwwwwwwu...", "...uuuuuuuu...", ".............."],
  solving: ["..............", "..............", ".MMMMMMMMMMMM.", ".MggggggggggM.", ".MgMMgMgMMggM.", ".MggggggggggM.", ".MgMgMMMgMggM.",
            ".MggggggggggM.", ".MgMMMMMwwggM.", ".MggggggggggM.", ".MMMMMMMMMMMM.", "......MM......", "....MMMMMM....", ".............."],
};
for (const [k, hat] of Object.entries(HATS)) SPRITES[k] = [...hat, ...ROBOT];

function pixels(name, cls = "") {
  const rows = SPRITES[name], s = document.createElementNS(NS, "svg");
  s.setAttribute("viewBox", "0 0 14 14");
  s.setAttribute("shape-rendering", "crispEdges");
  s.setAttribute("class", "icon pixel " + cls);
  // one path per colour; each run of pixels is one rectangle, a hair taller so rows never show a seam
  const runs = {};
  rows.forEach((row, y) => {
    for (let x = 0; x < row.length; ) {
      const ch = row[x];
      let n = 1;
      while (row[x + n] === ch) n++;
      if (ch !== ".") (runs[ch] ||= []).push(`M${x} ${y}h${n}v1.04h-${n}z`);
      x += n;
    }
  });
  s.innerHTML = Object.entries(runs).map(([ch, d]) => `<path fill="${PALETTE[ch]}" d="${d.join("")}"/>`).join("");
  return s;
}

// The automatic check: text that spills out of its box, labels that overlap boxes
// or each other, and anything outside the figure. Problems go to the console and
// to <body data-issues>, which export.py prints.
function check(fig) {
  const issues = [];
  const name = (el) => el.id ? "#" + el.id : `${el.className.baseVal ?? el.className} "${el.textContent.trim().slice(0, 30)}"`;
  const f = fig.getBoundingClientRect();
  const boxes = [...fig.querySelectorAll(".panel, .chip, .card, .cell, .item, .note, .alabel, [data-box]")];
  // badges sit on a box's corner on purpose, so leave them out of the spill check
  const badges = [...fig.querySelectorAll(".badge")];
  badges.forEach((b) => (b.style.display = "none"));
  for (const el of boxes) {
    if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) issues.push(`text spills out of ${name(el)}`);
    const r = el.getBoundingClientRect();
    if (r.left < f.left - 0.5 || r.right > f.right + 0.5 || r.top < f.top - 0.5) issues.push(`${name(el)} is outside the figure`);
  }
  badges.forEach((b) => {
    b.style.display = "";
    const r = b.getBoundingClientRect();
    if (r.left < f.left - 0.5 || r.right > f.right + 0.5 || r.top < f.top - 0.5) issues.push(`a badge sticks out of the figure`);
  });
  const hit = (a, b, pad = 0) => a.left < b.right - pad && b.left < a.right - pad && a.top < b.bottom - pad && b.top < a.bottom - pad;
  const labels = [...fig.querySelectorAll(".alabel")];
  const solid = [...fig.querySelectorAll(".chip, .card, .cell, .item, .panel > h2, .note, [data-box]")];
  for (const l of labels) {
    const r = l.getBoundingClientRect();
    for (const o of [...solid, ...labels]) {
      if (o === l) continue;
      if (hit(r, o.getBoundingClientRect(), 0.5)) issues.push(`label ${name(l)} overlaps ${name(o)}`);
    }
    for (const p of fig.querySelectorAll(".panel")) {
      const q = p.getBoundingClientRect();
      const crosses = hit(r, q) && !(r.left >= q.left && r.right <= q.right && r.top >= q.top && r.bottom <= q.bottom);
      if (crosses) issues.push(`label ${name(l)} crosses the border of ${name(p)}`);
    }
  }
  const unique = [...new Set(issues)];
  unique.forEach((i) => console.warn("figure check:", i));
  document.body.dataset.issues = JSON.stringify(unique);
}

// A digit centred by its line box sits low and a little off, because digits have no descender
// and uneven side bearings. Measure the ink itself and place it in the middle of the circle.
function centreNumbers(fig) {
  const ctx = document.createElement("canvas").getContext("2d");
  fig.querySelectorAll(".n").forEach((el) => {
    const cs = getComputedStyle(el);
    if (cs.borderTopLeftRadius !== "50%") return;
    const txt = el.textContent.trim(), w = el.clientWidth, h = el.clientHeight;
    ctx.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const m = ctx.measureText(txt);
    const x = (w - m.actualBoundingBoxLeft - m.actualBoundingBoxRight) / 2 + m.actualBoundingBoxLeft;
    const y = (h - m.actualBoundingBoxAscent - m.actualBoundingBoxDescent) / 2 + m.actualBoundingBoxAscent;
    el.innerHTML = `<svg width="${w}" height="${h}" style="display:block"><text x="${x}" y="${y}" fill="${cs.color}" ` +
                   `style="font:${ctx.font}">${txt}</text></svg>`;
  });
}

function draw() {
  icons();
  centreNumbers(document.getElementById("fig"));
  const fig = document.getElementById("fig");
  const svg = document.createElementNS(NS, "svg");
  svg.id = "arrows";
  svg.append(document.createElementNS(NS, "defs"));
  fig.append(svg);
  for (const [from, to, o] of queue) {
    // every arrow is the same grey, whatever colour the figure asks for
    const color = css("flow"), ink = css("flow-ink");
    const a = point(from, fig), b = point(to, fig);
    // straight: true lines the end up with the start, for a clean vertical or horizontal arrow
    if (o.straight) { if (a.d[0] === 0) b.x = a.x; else b.y = a.y; }
    // leave a hair of space between the arrowhead and the box it points at, and stop the line
    // inside the head (see marker), so its corners never show beside the point
    const w = o.width || 1.1, back = HEAD_BACK * w;
    b.x += b.d[0] * (0.5 + back); b.y += b.d[1] * (0.5 + back);
    if (o.both) { a.x += a.d[0] * (0.5 + back); a.y += a.d[1] * (0.5 + back); }
    const pts = route(a, b, typeof o.mid === "string" ? centre(o.mid, fig) : o.mid);
    const path = document.createElementNS(NS, "path");
    path.setAttribute("d", pts.map((p, i) => `${i ? "L" : "M"} ${p.x.toFixed(2)} ${p.y.toFixed(2)}`).join(" "));
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", color);
    path.setAttribute("stroke-width", w);
    path.setAttribute("stroke-linejoin", "round");
    if (o.dashed) path.setAttribute("stroke-dasharray", "3 2");
    if (o.dotted) { path.setAttribute("stroke-dasharray", "0.1 2.2"); path.setAttribute("stroke-linecap", "round"); }
    path.setAttribute("marker-end", marker(svg, color));
    if (o.both) path.setAttribute("marker-start", marker(svg, color));
    svg.append(path);
    if (o.label) {
      const p = pointAt(pts, o.at ?? 0.5);
      const l = document.createElement("div");
      l.className = "alabel" + (o.plain ? " plain" : "");
      l.style.color = ink;
      l.innerHTML = o.label;
      fig.append(l);
      const w = l.offsetWidth, h = l.offsetHeight, g = 1 * MM;
      const side = o.side || (p.horizontal ? "above" : "right");
      const pos = { above: [p.x - w / 2, p.y - h - g * 0.6], below: [p.x - w / 2, p.y + g * 0.6],
                    left: [p.x - w - g, p.y - h / 2], right: [p.x + g, p.y - h / 2] }[side];
      l.style.left = `${pos[0]}px`; l.style.top = `${pos[1]}px`;
    }
  }
  check(fig);
  // Size the printed page to the figure, so the PDF has no margins.
  const r = fig.getBoundingClientRect();
  const s = document.createElement("style");
  s.textContent = `@page { size: ${r.width}px ${Math.ceil(r.height + 1)}px; margin: 0; }`;
  document.head.append(s);
  document.body.dataset.ready = "1";
}

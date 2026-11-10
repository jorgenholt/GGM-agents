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
// mid (where to put the bend, in mm from the figure's left or top).

const MM = 96 / 25.4;
const NS = "http://www.w3.org/2000/svg";
const queue = [];

function css(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(`--${name}`).trim() || name;
}

function point(spec, fig) {
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
  const ah = a.d[0] !== 0, bh = b.d[0] !== 0;
  if (ah && bh) {
    if (Math.abs(a.y - b.y) < 0.5) return [a, { x: b.x, y: a.y }];
    const mx = mid != null ? mid * MM : (a.x + b.x) / 2;
    return [a, { x: mx, y: a.y }, { x: mx, y: b.y }, b];
  }
  if (!ah && !bh) {
    if (Math.abs(a.x - b.x) < 0.5) return [a, { x: a.x, y: b.y }];
    const my = mid != null ? mid * MM : (a.y + b.y) / 2;
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

function marker(svg, color) {
  const id = "head-" + color.replace(/[^\w]/g, "");
  if (!svg.querySelector("#" + id)) {
    const m = document.createElementNS(NS, "marker");
    Object.entries({ id, viewBox: "0 0 10 10", refX: 8.5, refY: 5, markerWidth: 5.5, markerHeight: 5.5,
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
}

function draw() {
  icons();
  const fig = document.getElementById("fig");
  const svg = document.createElementNS(NS, "svg");
  svg.id = "arrows";
  svg.append(document.createElementNS(NS, "defs"));
  fig.append(svg);
  for (const [from, to, o] of queue) {
    const color = css(o.color ? `${o.color}` : "ink");
    const ink = css(o.color ? `${o.color}-ink` : "ink");
    const a = point(from, fig), b = point(to, fig);
    // straight: true lines the end up with the start, for a clean vertical or horizontal arrow
    if (o.straight) { if (a.d[0] === 0) b.x = a.x; else b.y = a.y; }
    // leave a hair of space between the arrowhead and the box it points at
    b.x += b.d[0] * 0.5; b.y += b.d[1] * 0.5;
    const pts = route(a, b, o.mid);
    const path = document.createElementNS(NS, "path");
    path.setAttribute("d", pts.map((p, i) => `${i ? "L" : "M"} ${p.x.toFixed(2)} ${p.y.toFixed(2)}`).join(" "));
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", color);
    path.setAttribute("stroke-width", o.width || 1.1);
    path.setAttribute("stroke-linejoin", "round");
    if (o.dashed) path.setAttribute("stroke-dasharray", "3 2");
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
  // Size the printed page to the figure, so the PDF has no margins.
  const r = fig.getBoundingClientRect();
  const s = document.createElement("style");
  s.textContent = `@page { size: ${r.width}px ${Math.ceil(r.height + 1)}px; margin: 0; }`;
  document.head.append(s);
  document.body.dataset.ready = "1";
}

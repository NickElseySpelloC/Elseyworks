// Site search: loads /index.json once, then ranks articles as the visitor types.
(function () {
  var input = document.getElementById("q");
  var status = document.getElementById("search-status");
  var list = document.getElementById("search-results");
  var indexUrl = document.currentScript.dataset.index;
  var docs = null;

  // Lower-case and strip accents so "cafe" finds "café".
  function norm(s) {
    return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  function prepare(d) {
    d._title = norm(d.title);
    d._meta = norm(d.section + " " + d.publication);
    d._desc = norm(d.description);
    d._text = norm(d.text);
    return d;
  }

  function count(hay, term) {
    var n = 0, i = hay.indexOf(term);
    while (i !== -1 && n < 5) { n++; i = hay.indexOf(term, i + term.length); }
    return n;
  }

  function score(d, terms) {
    var total = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      var s = (d._title.indexOf(t) !== -1 ? 10 : 0) + (d._meta.indexOf(t) !== -1 ? 4 : 0) +
        (d._desc.indexOf(t) !== -1 ? 3 : 0) + count(d._text, t);
      if (!s) return 0; // every word must appear somewhere
      total += s;
    }
    return total;
  }

  // Build a short excerpt around the first match, with matches highlighted.
  function snippet(d, terms) {
    var text = d.text, low = d._text, at = -1;
    for (var i = 0; i < terms.length && at === -1; i++) at = low.indexOf(terms[i]);
    if (at === -1) return [{ t: d.description }];
    var start = Math.max(0, at - 70), end = Math.min(text.length, at + 150);
    var piece = (start ? "…" : "") + text.slice(start, end) + (end < text.length ? "…" : "");
    var parts = [], lowPiece = norm(piece), pos = 0;
    while (pos < piece.length) {
      var next = -1, len = 0;
      for (var j = 0; j < terms.length; j++) {
        var k = lowPiece.indexOf(terms[j], pos);
        if (k !== -1 && (next === -1 || k < next)) { next = k; len = terms[j].length; }
      }
      if (next === -1) { parts.push({ t: piece.slice(pos) }); break; }
      if (next > pos) parts.push({ t: piece.slice(pos, next) });
      parts.push({ t: piece.slice(next, next + len), hit: true });
      pos = next + len;
    }
    return parts;
  }

  function render(results, terms, q) {
    list.textContent = "";
    results.forEach(function (d) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = d.url;
      var kick = document.createElement("span");
      kick.className = "kicker";
      kick.textContent = [d.section, d.publication, d.date].filter(Boolean).join(" · ");
      var h = document.createElement("span");
      h.className = "search-title";
      h.textContent = d.title;
      var p = document.createElement("span");
      p.className = "search-snippet";
      snippet(d, terms).forEach(function (part) {
        if (part.hit) {
          var m = document.createElement("mark");
          m.textContent = part.t;
          p.appendChild(m);
        } else {
          p.appendChild(document.createTextNode(part.t));
        }
      });
      a.append(kick, h, p);
      li.appendChild(a);
      list.appendChild(li);
    });
    status.textContent = results.length
      ? results.length + (results.length === 1 ? " article" : " articles") + " found for “" + q + "”"
      : "Nothing found for “" + q + "”. Try a different word, or browse all the writing.";
  }

  function run() {
    var q = input.value.trim();
    var terms = norm(q).split(/\s+/).filter(Boolean);
    if (!terms.length) { list.textContent = ""; status.textContent = ""; return; }
    if (!docs) { status.textContent = "Searching…"; return; }
    var hits = docs.map(function (d) { return { d: d, s: score(d, terms) }; })
      .filter(function (r) { return r.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .map(function (r) { return r.d; });
    render(hits, terms, q);
  }

  var params = new URLSearchParams(location.search);
  input.value = params.get("q") || "";
  input.addEventListener("input", function () {
    var url = input.value.trim() ? "?q=" + encodeURIComponent(input.value.trim()) : location.pathname;
    history.replaceState(null, "", url);
    run();
  });
  input.form.addEventListener("submit", function (e) { e.preventDefault(); run(); });

  fetch(indexUrl)
    .then(function (r) { return r.json(); })
    .then(function (data) { docs = data.map(prepare); run(); })
    .catch(function () { status.textContent = "Search isn’t working right now. You can browse all the writing instead."; });
})();

/* Fran C. · Systems portfolio: progressive enhancements.
   Every page reads fine without this file; it adds the mobile menu, blueprint tabs,
   the assessment and QA demos, project case-study dialogs and the copy-email button. */
(function () {
  var root = document.documentElement;
  root.classList.remove('no-js');
  root.classList.add('js');
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Mobile menu ---------- */
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(open));
      menuBtn.textContent = open ? 'Close' : 'Menu';
    });
  }

  /* ---------- Funnel flow tabs ---------- */
  var tablist = document.querySelector('[role="tablist"]');
  var selectFlow = function () {};
  if (tablist) {
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i, false); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = tabs.length;
        if (k === 'ArrowRight') { e.preventDefault(); select((i + 1) % n, true); }
        if (k === 'ArrowLeft') { e.preventDefault(); select((i - 1 + n) % n, true); }
        if (k === 'Home') { e.preventDefault(); select(0, true); }
        if (k === 'End') { e.preventDefault(); select(n - 1, true); }
      });
    });
    selectFlow = function (id) { panels.forEach(function (p, i) { if (p.id === 'flow-' + id) select(i, false); }); };
  }
  document.querySelectorAll('[data-flow]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var dlg = a.closest('dialog');
      if (dlg) dlg.close();
      selectFlow(a.dataset.flow);
      var target = document.getElementById('funnels');
      if (target) target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  });

  /* ---------- Assessment demo (sample data only) ---------- */
  var demo = document.getElementById('assessment-demo');
  if (demo) {
    var OUTCOMES = {
      foundation: { name: 'Foundation Builder', blurb: 'The offer and audience need defining before traffic will convert.', tag: 'outcome-foundation',
        seq: [['Instant', 'Results email: your Foundation Builder profile'], ['Day 1', 'Guide: defining one clear offer'], ['Day 3', 'Story: what a simple funnel looks like'], ['Day 5', 'Invite: book a strategy call']] },
      growth: { name: 'Growth Optimiser', blurb: 'Leads are coming in; the follow-up is where opportunities are lost.', tag: 'outcome-growth',
        seq: [['Instant', 'Results email: your Growth Optimiser profile'], ['Day 1', 'Checklist: five follow-up gaps to fix'], ['Day 3', 'Example: a nurture sequence that books calls'], ['Day 5', 'Invite: book a funnel review']] },
      scale: { name: 'Scale-Ready', blurb: 'The system works; the next step is automation and tighter tracking.', tag: 'outcome-scale',
        seq: [['Instant', 'Results email: your Scale-Ready profile'], ['Day 1', 'Guide: automating the handoff to sales'], ['Day 3', 'Example: pipeline stages that stay accurate'], ['Day 5', 'Invite: apply for implementation support']] }
    };
    var form = demo.querySelector('form');
    var out = {
      result: document.getElementById('demo-result'),
      record: document.getElementById('demo-record'),
      seq: document.getElementById('demo-seq'),
      status: document.getElementById('demo-status')
    };
    function render() {
      var groups = ['q1', 'q2', 'q3'], score = 0, answered = 0, answers = {};
      groups.forEach(function (g) {
        var c = form.querySelector('input[name="' + g + '"]:checked');
        if (c) { answered++; score += Number(c.value); answers[g] = c.dataset.label; }
      });
      if (answered < groups.length) {
        out.status.textContent = 'Answer all three questions to see what the system does. ' + answered + ' of 3 answered.';
        return;
      }
      var key = score <= 2 ? 'foundation' : score <= 4 ? 'growth' : 'scale';
      var o = OUTCOMES[key];
      out.status.textContent = 'Score ' + score + ' of 6 → ' + o.name + '. Result page, CRM record and email path updated.';
      out.result.innerHTML = '<span class="mono" style="font-size:12px;color:#FF9C7E">YOUR RESULT</span><b>' + o.name + '</b><span>' + o.blurb + '</span>';
      out.record.innerHTML =
        row('email', 'sample.lead@example.com') + row('first_name', 'Sample') + row('lead_source', 'assessment-landing-page') +
        row('q1_offer', answers.q1) + row('q2_leads', answers.q2) + row('q3_followup', answers.q3) +
        row('assessment_score', String(score)) + row('assessment_outcome', o.name) +
        '<div><dt>tags</dt><dd><span class="chips"><span class="chip tag">assessment-completed</span><span class="chip tag">' + o.tag + '</span></span></dd></div>' +
        row('workflow', o.name + ' nurture');
      out.seq.innerHTML = o.seq.map(function (s) { return '<li><span class="when">' + s[0] + '</span><span>' + s[1] + '</span></li>'; }).join('') +
        '<li><span class="when">Exit</span><span>Leaves the sequence as soon as a call is booked</span></li>';
    }
    function row(k, v) { return '<div><dt>' + k + '</dt><dd>' + escapeHtml(v) + '</dd></div>'; }
    form.addEventListener('change', render);
    form.addEventListener('submit', function (e) { e.preventDefault(); render(); });
  }

  /* ---------- QA demo (sample journey) ---------- */
  var qa = document.getElementById('qa-demo');
  if (qa) {
    var checks = Array.prototype.slice.call(qa.querySelectorAll('.check'));
    var runBtn = document.getElementById('qa-run');
    var fixBtn = document.getElementById('qa-fix');
    var diag = document.getElementById('qa-diagnosis');
    var fixed = false, running = false;
    function setState(el, state, label) {
      el.dataset.state = state;
      el.querySelector('.ic').textContent = state === 'pass' ? '✓' : state === 'fail' ? '!' : state === 'skip' ? '–' : '·';
      el.querySelector('.chip').textContent = label;
    }
    function run() {
      if (running) return;
      running = true;
      runBtn.disabled = true;
      checks.forEach(function (c) { setState(c, 'idle', 'queued'); });
      var failAt = fixed ? -1 : Number(qa.dataset.failAt);
      var i = 0;
      (function next() {
        if (i >= checks.length) { finish(failAt); return; }
        var c = checks[i];
        if (failAt !== -1 && i > failAt) setState(c, 'skip', 'not reached');
        else if (i === failAt) setState(c, 'fail', 'failed');
        else setState(c, 'pass', 'passed');
        i++;
        setTimeout(next, reduceMotion ? 0 : 380);
      })();
    }
    function finish(failAt) {
      running = false;
      runBtn.disabled = false;
      diag.querySelector('[data-when="broken"]').hidden = failAt === -1;
      diag.querySelector('[data-when="fixed"]').hidden = failAt !== -1;
      diag.querySelector('[data-when="idle"]').hidden = true;
      fixBtn.hidden = failAt === -1;
      runBtn.textContent = 'Run the test again';
    }
    runBtn.addEventListener('click', function () { run(); });
    fixBtn.addEventListener('click', function () { fixed = true; run(); });
  }

  /* ---------- Project dialogs ---------- */
  document.querySelectorAll('[data-open]').forEach(function (btn) {
    var dlg = document.getElementById(btn.dataset.open);
    if (!dlg || typeof dlg.showModal !== 'function') return;
    btn.addEventListener('click', function () { dlg.showModal(); if (history.replaceState) history.replaceState(null, '', '#' + dlg.id); });
  });
  document.querySelectorAll('dialog.case').forEach(function (dlg) {
    dlg.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', function () { dlg.close(); }); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('close', function () { if (history.replaceState) history.replaceState(null, '', location.pathname); });
  });
  function openFromHash() {
    if (!location.hash) return;
    var target = document.querySelector('dialog.case' + location.hash.replace(/[^#\w-]/g, ''));
    if (target && !target.open && typeof target.showModal === 'function') target.showModal();
  }
  openFromHash();
  window.addEventListener('hashchange', openFromHash);

  /* ---------- Copy email ---------- */
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var text = b.dataset.copy;
      function selectFallback() {
        var el = document.getElementById(b.dataset.target);
        if (el) { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }
        b.textContent = 'Selected: press copy';
      }
      try { navigator.clipboard.writeText(text).then(function () { b.textContent = 'Copied'; }, selectFallback); } catch (e) { selectFallback(); }
    });
  });

  function escapeHtml(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
})();

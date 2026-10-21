"""Build index.html: Pricing Desk demo, enablement and UAT test script (SaaScend-branded).

    python3 build.py

Content lives in content.py. The page is one self-contained file: own CSS/JS, the logo inline,
only Google Fonts external. Test results persist per browser (localStorage) and export as CSV.
"""
import base64
import html
import json
import os

import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGO = base64.b64encode(open(os.path.join(ROOT, 'logo_white.png'), 'rb').read()).decode()
esc = html.escape


def a(href, text):
    return f'<a href="{esc(href)}" target="_blank" rel="noopener">{text}</a>'


def fig(name, cap, alt=None):
    src = f'shots/{name}'
    return (f'<figure class="shot"><a href="{src}" target="_blank" rel="noopener" title="Open full size">'
            f'<img src="{src}" alt="{esc(alt or cap)}" loading="lazy"></a><figcaption>{cap}</figcaption></figure>')


BLURNOTE = 'Cost and GP values are blurred on this public page. You will see them in the sandbox.'


CSS = r'''
:root{
  --ink:#1A1D28; --ink-soft:#4A4A4A; --muted:#6b7280;
  --ground:#F5F8FA; --card:#ffffff; --line:#E2E6EA; --tint:#EBF9FF;
  --accent:#00ACD4; --accent-ink:#0B5FA3; --navy:#031F49; --navy-2:#0A2E5C; --on-navy:#ffffff;
  --pass:#1e7a45; --pass-tint:#e4f6ea; --fail:#b42318; --fail-tint:#fdecea;
  --warn:#b45309; --warn-tint:#fdf3e3; --na:#6b7280; --na-tint:#eef0f3;
  --f-disp:"Montserrat",system-ui,sans-serif; --f-body:"Open Sans",system-ui,sans-serif;
  --f-mono:ui-monospace,"SFMono-Regular",Menlo,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ink:#e8edf5; --ink-soft:#b7c3d3; --muted:#8fa0b6; --ground:#07142e; --card:#0f2147; --line:#22375f;
  --tint:#12305a; --accent:#3cc5f5; --accent-ink:#7fd6f5; --navy:#031633; --navy-2:#0A2E5C;
  --pass:#5fc98a; --pass-tint:#12301e; --fail:#f19a8f; --fail-tint:#3a1714; --warn:#e8a24b; --warn-tint:#3a2c12;
  --na:#9aa6b8; --na-tint:#1b2c4e;
}}
:root[data-theme="dark"]{
  --ink:#e8edf5; --ink-soft:#b7c3d3; --muted:#8fa0b6; --ground:#07142e; --card:#0f2147; --line:#22375f;
  --tint:#12305a; --accent:#3cc5f5; --accent-ink:#7fd6f5; --navy:#031633; --navy-2:#0A2E5C;
  --pass:#5fc98a; --pass-tint:#12301e; --fail:#f19a8f; --fail-tint:#3a1714; --warn:#e8a24b; --warn-tint:#3a2c12;
  --na:#9aa6b8; --na-tint:#1b2c4e;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{background:var(--ground);color:var(--ink);font:16px/1.6 var(--f-body);margin:0}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:var(--f-disp);line-height:1.2;margin:0;text-wrap:balance}
h1{font-size:2.2rem;font-weight:800;letter-spacing:-.02em}
h2{font-size:1.5rem;font-weight:700;margin:0 0 .4rem}
h3{font-size:1.05rem;font-weight:700;margin:1.2rem 0 .3rem}
p{margin:.5rem 0;max-width:72ch}
a{color:var(--accent-ink)}
code{font-family:var(--f-mono);font-size:.84em;background:var(--tint);padding:1px 5px;border-radius:4px;
  border:1px solid var(--line);overflow-wrap:anywhere}
pre{font-family:var(--f-mono);font-size:.82em;background:var(--tint);border:1px solid var(--line);
  border-radius:6px;padding:8px 10px;margin:.4rem 0;white-space:pre-wrap}
.eyebrow{font-family:var(--f-disp);font-weight:700;font-size:.72rem;letter-spacing:.18em;
  text-transform:uppercase;color:var(--accent);margin:0 0 .5rem}

header.hero{background:linear-gradient(135deg,var(--navy),var(--navy-2));color:var(--on-navy);
  padding:26px 0 34px;border-bottom:4px solid var(--accent)}
.brandbar{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:28px}
.brandbar img{height:38px;width:auto}
.brandbar .tag{font-size:.78rem;color:#a9c4e4;border:1px solid rgba(255,255,255,.2);border-radius:99px;padding:3px 10px}
header.hero .eyebrow{color:#7fd6f5}
header.hero p{color:#cfdcee;font-size:1.05rem}
.facts{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.facts span{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:6px;
  padding:6px 10px;font-size:.85rem}
.facts b{color:#7fd6f5;font-weight:600}

nav.toc{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--line)}
nav.toc .wrap{display:flex;gap:4px;overflow-x:auto;padding-top:6px;padding-bottom:6px;scrollbar-width:thin}
nav.toc a{white-space:nowrap;text-decoration:none;color:var(--ink-soft);font-family:var(--f-disp);font-weight:600;
  font-size:.82rem;padding:6px 10px;border-radius:6px}
nav.toc a:hover{background:var(--tint);color:var(--ink)}

section.block{padding:38px 0 8px}
section.block>.wrap>p.lead{font-size:1.06rem;color:var(--ink-soft)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:14px 0}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.callout{border-left:4px solid var(--accent);background:var(--tint);border-radius:6px;padding:12px 14px;margin:14px 0}
.callout.warn{border-left-color:var(--warn);background:var(--warn-tint)}
.tbl{width:100%;border-collapse:collapse;font-size:.92rem;background:var(--card)}
.tblwrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;margin:12px 0}
.tbl th,.tbl td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl th{font-family:var(--f-disp);font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);background:var(--ground)}
.tbl tr:last-child td{border-bottom:0}
.pill{display:inline-block;font-family:var(--f-disp);font-weight:700;font-size:.72rem;border-radius:99px;
  padding:2px 9px;background:var(--tint);color:var(--accent-ink);white-space:nowrap}
.pill.now{background:var(--pass-tint);color:var(--pass)} .pill.next{background:var(--warn-tint);color:var(--warn)}

/* screenshots */
figure.shot{margin:14px 0;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
figure.shot a{display:block;line-height:0}
figure.shot img{width:100%;height:auto;display:block}
figure.shot figcaption{padding:9px 14px;font-size:.86rem;color:var(--ink-soft);border-top:1px solid var(--line)}
.shots2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.shots2 figure.shot{margin:0}
.reclinks a{display:inline-block;margin:2px 10px 2px 0;white-space:nowrap}

/* flow diagram */
.flow{display:flex;flex-wrap:wrap;align-items:stretch;gap:0;margin:16px 0}
.flow .step{flex:1 1 150px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;
  position:relative;margin:6px 14px 6px 0}
.flow .step:not(:last-child)::after{content:"→";position:absolute;right:-13px;top:50%;transform:translateY(-50%);
  color:var(--accent);font-weight:800}
.flow .step.p2{border-style:dashed;background:transparent}
.flow .n{font-family:var(--f-disp);font-weight:800;color:var(--accent);font-size:.8rem}
.flow .t{font-family:var(--f-disp);font-weight:700;font-size:.95rem;margin:2px 0 4px}
.flow .d{font-size:.83rem;color:var(--ink-soft)}
ol.steps{margin:.4rem 0;padding-left:1.3rem} ol.steps li{margin:.25rem 0}

/* test script */
.runbar{position:sticky;top:44px;z-index:4;background:var(--card);border:1px solid var(--line);border-radius:10px;
  padding:12px 14px;margin:14px 0;display:flex;flex-wrap:wrap;gap:10px 16px;align-items:end}
.runbar label{font-size:.75rem;font-family:var(--f-disp);font-weight:700;color:var(--muted);display:block}
.runbar input{font:inherit;font-size:.9rem;padding:6px 8px;border:1px solid var(--line);border-radius:6px;
  background:var(--ground);color:var(--ink);min-width:170px}
.meter{flex:1 1 220px}
.meter .bar{height:10px;background:var(--ground);border:1px solid var(--line);border-radius:99px;overflow:hidden;display:flex}
.meter .bar i{display:block;height:100%}
.meter .txt{font-size:.82rem;color:var(--ink-soft);margin-top:4px;font-variant-numeric:tabular-nums}
.btn{font-family:var(--f-disp);font-weight:700;font-size:.82rem;border:1px solid var(--accent-ink);background:var(--card);
  color:var(--accent-ink);border-radius:6px;padding:7px 12px;cursor:pointer}
.btn.primary{background:#1071C3;border-color:#1071C3;color:#fff}
.suite{margin:22px 0}
.suite h3{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.suite h3 small{font-family:var(--f-body);font-weight:400;color:var(--muted);font-size:.85rem}
.case{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--line);border-radius:10px;
  padding:14px 16px;margin:10px 0;display:grid;grid-template-columns:1fr 1fr;gap:6px 22px}
.case[data-r="pass"]{border-left-color:var(--pass)} .case[data-r="fail"]{border-left-color:var(--fail)}
.case[data-r="blocked"]{border-left-color:var(--warn)} .case[data-r="na"]{border-left-color:var(--na)}
.case .hd{grid-column:1/-1;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.case .id{font-family:var(--f-mono);font-size:.8rem;font-weight:700;color:var(--accent-ink)}
.case .ttl{font-family:var(--f-disp);font-weight:700}
.case .lbl{font-family:var(--f-disp);font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700}
.case .exp{background:var(--ground);border-radius:6px;padding:8px 10px;font-size:.93rem}
.case .res{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:6px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.seg button{font:600 .8rem var(--f-disp);border:0;background:var(--card);color:var(--ink-soft);padding:7px 11px;cursor:pointer;
  border-right:1px solid var(--line)}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"][data-v="pass"]{background:var(--pass);color:#fff}
.seg button[aria-pressed="true"][data-v="fail"]{background:var(--fail);color:#fff}
.seg button[aria-pressed="true"][data-v="blocked"]{background:var(--warn);color:#fff}
.seg button[aria-pressed="true"][data-v="na"]{background:var(--na);color:#fff}
.case textarea{flex:1 1 260px;font:inherit;font-size:.88rem;min-height:38px;padding:6px 8px;border:1px solid var(--line);
  border-radius:6px;background:var(--ground);color:var(--ink);resize:vertical}
.signoff input{font:inherit;font-size:.9rem;width:100%;padding:5px 7px;border:1px solid var(--line);border-radius:6px;
  background:var(--ground);color:var(--ink)}
footer{margin-top:40px;background:var(--navy);color:#a9c4e4;padding:22px 0;font-size:.85rem}
footer img{height:26px;vertical-align:middle;margin-right:10px}
@media (max-width:700px){
  h1{font-size:1.7rem} .case{grid-template-columns:1fr} .runbar{top:44px;position:static}
  .flow .step{flex-basis:100%;margin-right:0} .flow .step:not(:last-child)::after{content:"↓";right:auto;left:50%;top:auto;bottom:-15px;transform:none}
}
@media print{
  nav.toc,.runbar .btn,.themebtn{display:none} header.hero{background:#031F49!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .case{break-inside:avoid} body{background:#fff}
}
'''


def hero():
    return f'''<header class="hero"><div class="wrap">
  <div class="brandbar"><img src="data:image/png;base64,{LOGO}" alt="SaaScend">
    <span class="tag">Sandbox · internal · not for customers</span></div>
  <p class="eyebrow">DXR Cyber · Round 2 · scoping, margin, approvals and e-signature</p>
  <h1>Pricing Desk, Approvals &amp; E-signature</h1>
  <p>Demo guide, enablement and the UAT test script for the small test group. Every case below has to pass before we plan the production release.</p>
  <div class="facts">
    <span><b>Org</b> Xypher_Sandbox_FC (full-copy sandbox)</span>
    <span><b>Testing</b> open · cost data still to come</span>
    <span><b>Build status</b> Apex 218/218 · browser UAT 9 suites green · 21 Oct</span>
    <span><b>As of</b> 21 Oct 2026</span>
  </div>
</div></header>'''


TOC = [('round2', 'Round 2: start here'), ('access', 'Access & links'), ('how', 'How it works'), ('demo', 'Demo walkthrough'),
       ('reps', 'Rep enablement'), ('catalogue', 'Catalogue & costs'), ('docgen', 'Document generation'),
       ('script', 'Test script'), ('gaps', 'Known gaps'), ('signoff', 'Sign-off')]


def toc():
    return '<nav class="toc" aria-label="Sections"><div class="wrap">' + ''.join(
        f'<a href="#{i}">{t}</a>' for i, t in TOC) + '</div></nav>'


def round2():
    new = [
        ('Scoping', 'Request Scoping asks: <b>send it to the customer</b> or <b>complete it yourself</b>. A sent form can be taken back with <b>Complete it myself</b>; the customer\'s link stops working. Closing a scope is now <b>engineer verification</b>: a technical verifier ticks "I have checked these figures", and nobody verifies a scope they filled in.', 'SCOPE'),
        ('Margin and GP', 'Net revenue = price − licence cost; GP = net revenue − delivery cost. A <b>fully costed</b> quote below <b>40% GP</b> needs manager approval, and the <b>Margin</b> card says how to pass ("cut the discount to 57%", with Apply). A quote with any uncosted line shows <b>GP n/a</b> and falls back to "over 40% discount needs approval".', 'MRG'),
        ('Approvals', '<b>Save &amp; Submit</b> goes to your Salesforce manager with the reason filled in. Recall, Edit &amp; Resubmit, and a notification either way. Partner deals pre-fill the partner\'s discount on eligible lines.', 'MRG'),
        ('Send for e-signature', '<b>Request to Send</b> (from Proposal onwards) goes to your manager; their approval is DXR Cyber\'s acceptance. PandaDoc then sends the order form <b>as the manager</b>, so reps need no PandaDoc licence. Revise &amp; Resend withdraws a sent version.', 'SEND'),
        ('Signed deals tidy themselves', 'The Opportunity syncs to the quote when it goes out. On signature: signed PDF on the Quote and Opportunity, contract dates from the signing date, and a "Close Won" Task plus a notification for the owner.', 'SEND'),
    ]
    rows = ''.join(f'<tr><td><b>{t}</b></td><td>{d}</td><td><a href="#suite-{sid}">{sid}</a></td></tr>' for t, d, sid in new)
    roles = [
        ('Sales rep', 'Requests scoping, builds and submits quotes, requests the send', 'SCOPE-01–04, MRG, SEND'),
        ('Sales manager', 'Approves or rejects price and send requests; must have a PandaDoc seat', 'MRG-06, SEND-03'),
        ('Technical verifier', 'Verifies and closes scoping (DXR Scoping Technical)', 'SCOPE-05–06'),
        ('Catalogue manager', 'Loads costs as they arrive (Cost Upload)', 'COST'),
        ('SaaScend', 'Sets everyone up, simulates the customer signature on request, answers questions', 'SEND-04'),
    ]
    rr = ''.join(f'<tr><td><b>{r}</b></td><td>{w}</td><td>{c}</td></tr>' for r, w, c in roles)
    e2e = ''.join(f'<tr><td><b>{esc(n)}</b></td><td>{esc(d)}</td><td>' + ''.join(a(u, esc(l)) for l, u in links) + '</td></tr>'
                  for n, d, links in C.E2E)
    return f'''<section class="block" id="round2"><div class="wrap">
  <p class="eyebrow">Round 2 · start here</p><h2>What's new, and what to test first</h2>
  <div class="callout warn"><b>Awaiting cost data, but testing can start now.</b> 583 of the 727 active products have no cost loaded yet; DXR Cyber is filling in the cost template. Until a quote's lines all have costs, the desk shows <b>GP n/a</b> and the rule is the simpler one: <b>a discount over 40% needs manager approval</b>. Every flow below works today. The few cases that need a costed product say so and use <code>GRC-CE-009</code>. Once costs are loaded we re-run MRG-02/03 on real deals.</div>
  <div class="tblwrap"><table class="tbl"><tr><th>Change</th><th>What you'll see</th><th>Tests</th></tr>{rows}</table></div>
  <h3>Who does what</h3>
  <div class="tblwrap"><table class="tbl"><tr><th>Role</th><th>In this round</th><th>Cases</th></tr>{rr}</table></div>
  <div class="grid2">
    <div class="card"><h3 style="margin-top:0">Before you start (SaaScend sets this up)</h3><ul>
      <li>Each tester has a <b>Manager</b> in Salesforce (approvals go there; there is no fallback).</li>
      <li>Each manager is marked as holding a <b>PandaDoc seat</b>.</li>
      <li>Reps have <b>DXR Scoping Sales</b>; verifiers have <b>DXR Scoping Technical</b>.</li>
      <li>A test channel for questions and for "please sign SEND-04".</li>
    </ul></div>
    <div class="card"><h3 style="margin-top:0">Suggested order</h3><ol class="steps">
      <li><b>ACC</b>: log in and find things.</li>
      <li><b>SCOPE</b>, then <b>MRG</b>, then <b>SEND</b>: the new round, on your own <code>[UAT]</code> opportunities.</li>
      <li>The round 1 suites (DESK to PERM) as a regression check, on the <code>[DEMO]</code> records.</li>
      <li>Export your CSV and send it to SaaScend.</li>
    </ol></div>
  </div>
  <h3>See it end to end first</h3>
  <p style="font-size:.92rem;color:var(--ink-soft)">Two fictional deals were run through the whole process on 21 Oct and kept, so managers can see every output before testing: the scoping document and PDF, the quote, both approvals in the Quote's Approval History, the order form, and the signed copy in Files.</p>
  <div class="tblwrap"><table class="tbl reclinks"><tr><th>Deal</th><th>What it shows</th><th>Open</th></tr>{e2e}</table></div>
  <p style="font-size:.88rem;color:var(--muted)">PandaDoc links open in DXR Cyber's PandaDoc workspace; log in there first. They are sandbox test documents, so the names start with <b>[DEV]</b>, they sit in the <b>SF-Sandbox</b> folder, and the customer signature was simulated. If PandaDoc says you don't have access, ask a workspace admin (Scott Goodwin) to share them.</p>
  <div class="callout"><b>In the sandbox:</b> PandaDoc sends silently to a SaaScend inbox, so customers never receive anything and SaaScend simulates the signature. Customer scoping emails go to whatever address the contact has, so use a test contact with your own email. Never use a real customer's opportunity.</div>
</div></section>'''


def access():
    rows = ''.join(f'<tr><td>{a(u, esc(n))}</td><td>{esc(d)}</td></tr>' for n, u, d in C.LINKS)
    ps = ''.join(f'<li><code>{p}</code></li>' for p in C.TESTER['psets'])
    recs = ''.join(f'<tr><td><b>{esc(d)}</b></td><td>' + ''.join(a(u, esc(l)) for l, u in links) + '</td></tr>'
                   for d, links in C.RECORDS)
    return f'''<section class="block" id="access"><div class="wrap">
  <p class="eyebrow">Start here</p><h2>Access and links</h2>
  <p class="lead">Test as the <b>UAT Pricing Tester</b>, not as an admin. That user has exactly what a DXR rep has, plus the Catalogue Manager permission set, so it proves the real permissions.</p>
  <div class="grid2">
    <div class="card"><h3 style="margin-top:0">The tester user</h3>
      <table class="tbl"><tr><th>Name</th><td>{esc(C.TESTER['name'])}</td></tr>
      <tr><th>Username</th><td><code>{esc(C.TESTER['username'])}</code></td></tr>
      <tr><th>Profile</th><td>{esc(C.TESTER['profile'])}</td></tr></table>
      <p style="font-size:.9rem"><b>Permission sets:</b></p><ul style="margin:.2rem 0;font-size:.9rem">{ps}</ul></div>
    <div class="card"><h3 style="margin-top:0">Getting in</h3>
      <ol class="steps">
        <li>Salesforce sent the tester's set-password email to SaaScend's delivery mailbox. SaaScend sets the password and shares it with you <b>directly, never in this page or in chat channels</b>.</li>
        <li>Log in at {a(C.LOGIN, 'the sandbox login page')} (not login.salesforce.com).</li>
        <li>One person at a time: every rep tester shares this user. Put your own name in the test script's <b>Tester</b> box so your results are yours.</li>
        <li><b>Managers and technical verifiers</b> (round 2) log in to the sandbox as themselves: approvals and verification have to come from a different person than the rep.</li>
      </ol>
      <div class="callout warn" style="font-size:.9rem"><b>Sandbox only.</b> The <code>[DEMO]</code> companies and contacts are fictional. Never test on a real customer's opportunity.</div></div>
  </div>
  <h3>Links</h3>
  <div class="tblwrap"><table class="tbl"><tr><th>Open</th><th>What it's for</th></tr>{rows}</table></div>
  <h3>Every demo record</h3>
  <p style="font-size:.92rem;color:var(--ink-soft)">Direct links into the sandbox. Log in first, then these open straight to the record.</p>
  <div class="tblwrap"><table class="tbl reclinks"><tr><th>Deal</th><th>Records</th></tr>{recs}</table></div>
  <p style="font-size:.9rem;color:var(--muted)">If a screen looks out of date after an update, hard-refresh (Cmd/Ctrl+Shift+R). Salesforce caches components in the browser.</p>
</div></section>'''


def how():
    steps = [
        ('1', 'Scoping', 'Sent to the customer or completed by the rep, then verified and closed by the technical team. The scoping PDF is filed on the Opportunity.'),
        ('2', 'Pricing Desk', 'The rep builds a quote from the catalogue (products, prices, bundles and costs in the Xypher Catalogue app). Margin is checked live.'),
        ('3', 'Approval', 'Below 40% GP (fully costed), or over 40% discount on a line with no cost: the rep\'s manager approves in Salesforce.'),
        ('4', 'Request to Send', 'From Proposal onwards. The manager approves the send, which is DXR Cyber\'s acceptance. The Opportunity syncs to the quote.'),
        ('5', 'PandaDoc', 'The order form goes out for e-signature as the manager. Status is checked every 15 minutes.'),
        ('6', 'Signed', 'Signed PDF on the Quote and Opportunity, contract dates set, and the owner is told to Close Won.'),
    ]
    f = ''.join(f'<div class="step"><div class="n">{n}</div><div class="t">{t}</div><div class="d">{d}</div></div>' for n, t, d in steps)
    return f'''<section class="block" id="how"><div class="wrap">
  <p class="eyebrow">The model</p><h2>How it works</h2>
  <p class="lead">Scoping feeds pricing, and one catalogue feeds one desk. The desk writes a standard Quote, and the Opportunity is kept in step with it. The order form is rendered from the Quote, so it can't disagree with what was priced, and what is signed comes back to the deal.</p>
  <div class="flow">{f}</div>
  {fig('01b-launcher-card.png', 'The Pricing Desk tab on every Opportunity: the synced quote, its TCV and ARR, and the way into the desk.')}
  <div class="tblwrap"><table class="tbl">
    <tr><th>Rule</th><th>What the user sees</th></tr>
    <tr><td><b>40% GP minimum</b> (fully costed quotes)</td><td>Below 40% GP the quote needs manager approval. The Margin card shows the bar and suggests the change that passes, with an Apply button.</td></tr>
    <tr><td><b>Lines with no cost</b></td><td>GP can't be checked, so the desk shows "GP n/a". A discount over 40% on any line needs manager approval instead.</td></tr>
    <tr><td><b>Until approved</b></td><td>The quote saves as Approval Required. Sync &amp; Confirm and Generate PDF stay locked. Salesforce's own quote-line editor can't get round it. Over 100%, or a line past the contract end, is Blocked outright.</td></tr>
    <tr><td><b>Sending for signature</b></td><td>Only at Proposal / Bid Submitted or Negotiation, and only with the manager's approval. Reps need no PandaDoc licence.</td></tr>
    <tr><td><b>Partner deals</b></td><td>The partner Account's Partner Discount % is pre-filled on eligible lines (not licences, third-party, hardware or channel-priced lines).</td></tr>
    <tr><td><b>Mandatory components</b></td><td>Added automatically with their parent. They can't be removed on their own.</td></tr>
    <tr><td><b>Choice groups</b></td><td>SOC maturity: exactly one, Standard by default. SIEM platform: none or one.</td></tr>
    <tr><td><b>Revenue class and term</b></td><td>Annual-recurring lines × term years; one-offs count once. TCV is the Opportunity Amount.</td></tr>
    <tr><td><b>Adjustments</b></td><td><code>15</code> or <code>15%</code> is a discount, <code>£250</code> is amount off, <code>+8%</code> and <code>+£500</code> are uplifts.</td></tr>
    <tr><td><b>Gross profit</b></td><td>Net revenue = price − licence cost; GP = net revenue − delivery cost. Shown as a % only when every line is costed.</td></tr>
    <tr><td><b>Contract dates and part-term lines</b></td><td>Set the contract start (or leave blank for "on signature"); the end is calculated. A line can start later or end earlier, in whole months. Recurring lines are charged for the months they run; <b>annual recurring stays the full annual rate</b>. Renewals are priced from the lines still running at the end.</td></tr>
  </table></div>
</div></section>'''


def demo():
    rows = ''.join(f'<tr><td><b>{k}</b></td><td>{esc(n)}</td><td>{esc(s)}</td><td>{esc(w)}</td></tr>' for k, n, s, w in C.DEMO_RECORDS)
    return f'''<section class="block" id="demo"><div class="wrap">
  <p class="eyebrow">15-minute demo</p><h2>Demo walkthrough</h2>
  <p class="lead">Five fictional deals are staged so every part of the story can be shown without building anything in front of the audience, except the last one, which is built live.</p>
  <div class="tblwrap"><table class="tbl"><tr><th>#</th><th>Opportunity</th><th>State</th><th>What it shows</th></tr>{rows}</table></div>
  <div class="shots2">
    {fig('01-opportunity-record.png', 'Harbourline after sync: the Opportunity Products are the quote lines.')}
    {fig('02-desk-quote-list.png', 'Northshire in the desk: one quote ready to sync, one over the cap. ' + BLURNOTE)}
  </div>
  <div class="card"><h3 style="margin-top:0">Running order</h3><ol class="steps">
    <li><b>The finished article (2 min).</b> {a(C.opp('A'), 'Harbourline')}: Amount £344,595 is the quote's TCV, and the Quote Summary shows annual £114,865. Open the Quote → Quote PDFs → the DXR Cyber order form.</li>
    <li><b>The guard-rail (2 min).</b> {a(C.desk('C'), 'Northshire in the desk')}: open the 45% quote to show "needs manager approval" and the greyed-out Sync and PDF. Change it to 40%, Save, and it turns Ready.</li>
    <li><b>Sync live (2 min).</b> Open the other Northshire quote and click Sync &amp; Confirm. Back on the Opportunity, Amount is £6,915 and the Products are filled in. Generate PDF.</li>
    <li><b>A two-service deal (2 min).</b> {a(C.opp('B'), 'Kestrel &amp; Vane')}: its order form has one delivery section per service line, and the £3,600 one-off sits in year 1.</li>
    <li><b>Build one (5 min).</b> {a(C.desk('E'), 'Brightwater')}: New Quote → search <code>SOC-CORE-1.5TB-OPS</code> → the bundle arrives → switch maturity → add a SIEM tier → 10% off → Save → Sync → Generate PDF.</li>
    <li><b>Behind the scenes (2 min).</b> {a(C.CATALOGUE, 'Xypher Catalogue')}: the Products grid, Data Quality tiles, Change Log and Cost Upload.</li>
  </ol>
  <p style="font-size:.9rem;color:var(--muted)">Syncing or editing a demo record changes it for the next person. SaaScend can rebuild all five from the build scripts in minutes.</p></div>
  <div class="callout warn">The order forms print <b>DRAFT</b> with orange placeholders for the contracting entity, company and VAT numbers, and the terms URL. Say so up front. It's waiting on DXR Cyber's details, not a fault.</div>
</div></section>'''


def reps():
    return f'''<section class="block" id="reps"><div class="wrap">
  <p class="eyebrow">Enablement · sales reps</p><h2>Using the Pricing Desk</h2>
  <p class="lead">Reps quote from the Opportunity and never touch Opportunity Products directly. The desk is the one way in.</p>
  <div class="grid2">
    <div class="card"><h3 style="margin-top:0">Build and send a quote</h3><ol class="steps">
      <li>Opportunity → <b>Pricing Desk</b> tab → <b>Open Pricing Desk</b>.</li>
      <li><b>New Quote</b>. Name it and set the term in months. Check the commercial terms dropdowns.</li>
      <li>Add products by <b>search</b> (name or SKU) or by <b>service-line chip</b>. Packages bring their mandatory components with them.</li>
      <li>Click a package line to open <b>Bundle &amp; Add-ons</b>: pick the maturity level, and the SIEM tier if one is needed.</li>
      <li>Type adjustments in <b>Adj.</b> on each line. Watch the <b>Margin</b> card: if it says approval is needed, Apply its suggestion or use <b>Save &amp; Submit for Approval</b>.</li>
      <li><b>Save</b>. When the deal reaches Proposal, click <b>Request to Send</b>: your manager approves and PandaDoc sends it as them.</li>
      <li>Or, to keep working by hand: <b>Sync &amp; Confirm</b>, then <b>Generate PDF</b>.</li>
    </ol></div>
    <div class="card"><h3 style="margin-top:0">Good to know</h3><ul>
      <li><b>Edit after sync?</b> Just Save. A synced quote pushes changes to the Opportunity by itself.</li>
      <li><b>Try an alternative?</b> <b>Save as New Quote</b> makes a copy; only the synced one drives the Opportunity.</li>
      <li><b>Needs approval?</b> The Margin card says why and what would pass. Apply it, or submit with a reason; your manager decides.</li>
      <li><b>GP n/a?</b> At least one line has no cost yet, so only discounts are checked (over 40% needs approval).</li>
      <li><b>Monthly-priced items</b> (e.g. SIEM platform tiers) come in at qty 12 for a year.</li>
      <li><b>Product missing?</b> It may be hidden or retired in the Catalogue. Ask the catalogue manager.</li>
      <li><b>Deal notes</b> are for context the quote doesn't show. They don't print on the order form.</li>
      <li><b>Service starting later, or co-terming?</b> Use the line's <b>Period</b> cell: From month 4 for 33 months, say. Recurring lines are charged pro-rata; one-offs are never pro-rated.</li>
    </ul></div>
  </div>
  {fig('03-desk-soc-bundle.png', 'A SOC package: mandatory components locked, one maturity level, one SIEM tier, and totals that update as you type. ' + BLURNOTE)}
  {fig('04-desk-blocked.png', 'Over the cap: the 45% line turns red, and Sync &amp; Confirm and Generate PDF are disabled. ' + BLURNOTE)}
</div></section>'''


def catalogue():
    return f'''<section class="block" id="catalogue"><div class="wrap">
  <p class="eyebrow">Enablement · catalogue managers</p><h2>Managing the catalogue and costs</h2>
  <p class="lead">{a(C.CATALOGUE, 'Xypher Catalogue')} is the back office for 732 products. Prices, costs and bundles set here are what the desk quotes, and the Change Log records every change, who made it and when.</p>
  <div class="tblwrap"><table class="tbl"><tr><th>Task</th><th>Where</th><th>Notes</th></tr>
    <tr><td>Find a product</td><td>Products tab: service-line filter, name/SKU search</td><td>Shows active, hidden and retired products</td></tr>
    <tr><td>Add a product</td><td><b>Add Product</b>: name, SKU, list price, revenue class, business unit</td><td>Business unit is required</td></tr>
    <tr><td>Change a name, price or cost</td><td>Edit inline in the grid; saves when you leave the cell</td><td>Price changes are logged as <b>Reprice</b>, costs as <b>Cost Change</b></td></tr>
    <tr><td>Stop a product being quoted</td><td><b>Hide</b> (temporary) or <b>Retire</b> (permanent)</td><td>Retire warns you if bundles depend on the product. Nothing is ever deleted</td></tr>
    <tr><td>Bundles</td><td><b>Bundle editor</b> on the product</td><td>Mandatory, optional or choice (with a group). Circular bundles are refused</td></tr>
    <tr><td>Bulk costs</td><td><b>Cost Upload</b>: paste <code>SKU,Cost</code>, then <b>Preview Upload</b>, then <b>Apply Cost Upload</b></td><td>Only matched rows apply. Unknown, duplicate and non-numeric rows are listed and skipped</td></tr>
    <tr><td>Catalogue health</td><td><b>Data Quality</b> tiles</td><td>e.g. no cost loaded (613), service-line gap, leftover -CH codes</td></tr>
  </table></div>
  {fig('06-catalogue-products.png', 'Products tab, searched for SOC-MON: price and cost edit inline, and Actions holds Hide, Retire and Bundle editor. ' + BLURNOTE)}
  <div class="shots2">
    {fig('07-catalogue-data-quality.png', 'Data Quality: what still needs fixing in the catalogue.')}
    {fig('08-cost-upload-preview.png', 'Cost Upload preview: only matched rows apply. Unknown, duplicate and invalid rows are flagged. ' + BLURNOTE)}
  </div>
  <div class="callout"><b>Costs and GP.</b> Costs are in GBP. Once a product has one, every quote line for it shows cost and GP, and the Opportunity's Quote Summary reports total GP and coverage ("N of M lines costed"). Costs never appear on the order form. 13 products hold USD costs that need converting before upload.</div>
  <div class="callout warn"><b>Change prices only here.</b> The standard Salesforce price book screens are locked for catalogue managers on purpose, so every price change goes through the log.</div>
</div></section>'''


def docgen():
    return f'''<section class="block" id="docgen"><div class="wrap">
  <p class="eyebrow">Document generation</p><h2>How the order form is built, now and with PandaDoc</h2>
  <p class="lead">Salesforce builds the order form from the Quote itself, so the PDF always matches the priced lines. PandaDoc joins in phase 2 for signature only. It doesn't rebuild the document.</p>
  <div class="grid2">
    <div class="card"><h3 style="margin-top:0"><span class="pill now">Now · built</span> Salesforce renders the PDF</h3><ol class="steps">
      <li>The rep clicks <b>Generate PDF</b> on a Ready or Synced quote. Blocked quotes can't generate one.</li>
      <li>Salesforce fills the DXR Cyber template from the Quote:
        <ul><li><b>Header and parties</b>: the contracting entity for the Business Unit, plus the customer's account, primary contact and billing address.</li>
        <li><b>Pricing</b>: one table of lines with the discount visible and the SKU in small grey. Cost and margin never print.</li>
        <li><b>Payment schedule</b>: year by year, with one-offs in year 1.</li>
        <li><b>Delivery sections</b>: one per service line on the quote, from 27 modules plus a default.</li>
        <li><b>Terms</b>: incorporated by version.</li></ul></li>
      <li>The PDF is saved on the Quote under <b>Quote PDFs</b> and opens in a new tab. Regenerating adds a new version and keeps the old one.</li>
    </ol>
    <p style="font-size:.9rem">Delivery wording and entity details are data, not code. An admin edits them in Setup → Custom Metadata Types (<code>Order Form Delivery</code>, <code>Order Form Entity</code>). No deployment is needed.</p></div>
    <div class="card"><h3 style="margin-top:0"><span class="pill now">Built · in sandbox</span> PandaDoc for signature</h3><ol class="steps">
      <li>The rep clicks <b>Request to Send</b> (from Proposal onwards). Their manager approves; that approval is DXR Cyber's acceptance and prints on the order form.</li>
      <li>Salesforce uploads the order form to DXR Cyber's PandaDoc workspace with the signature fields in place and sends it <b>as the manager</b>. Only the customer signs; reps need no PandaDoc licence.</li>
      <li>Every 15 minutes Salesforce checks the status (sent, viewed, signed), within PandaDoc's API limits.</li>
      <li>On signature the signed PDF is filed on the Quote and the Opportunity, the contract dates are set, and the owner is told to Close Won. <b>Revise &amp; Resend</b> withdraws a sent version.</li>
    </ol>
    <p style="font-size:.9rem"><b>Needed before production:</b> the production PandaDoc API key, and PandaDoc seats for the approving managers.</p></div>
  </div>
  <div class="shots2">
    {fig('of-1.png', 'Page 1 of the Harbourline order form: parties, agreement, totals and the payment schedule. Orange = details DXR Cyber still has to supply.')}
    {fig('of-3.png', 'The delivery section for the Managed SOC service line: what’s included, what we need from you, how we deliver.')}
  </div>
  {fig('05-quote-pdfs.png', 'Every generated order form is kept on the Quote under Quote PDFs.')}
  <div class="callout">Why this route: the pricing lives in Salesforce, so one template serves DXR, CyberCrowd, Intaforensics and Aristi products. The alternative was 16 PandaDoc templates per brand, all mapped to fields.</div>
</div></section>'''


def case_html(sid, c):
    cid, title, steps, exp = c
    st = ''.join(f'<li>{s}</li>' for s in steps)
    seg = ''.join(f'<button type="button" data-v="{v}" aria-pressed="false">{l}</button>'
                  for v, l in (('pass', 'Pass'), ('fail', 'Fail'), ('blocked', 'Blocked'), ('na', 'N/A')))
    return f'''<article class="case" id="{cid}" data-id="{cid}" data-suite="{sid}" data-title="{esc(title)}">
  <div class="hd"><span class="id">{cid}</span><span class="ttl">{esc(title)}</span></div>
  <div><div class="lbl">Steps</div><ol class="steps">{st}</ol></div>
  <div><div class="lbl">Expected result</div><div class="exp">{exp}</div></div>
  <div class="res"><div class="seg" role="group" aria-label="Result for {cid}">{seg}</div>
    <textarea placeholder="Notes: what you saw, if it differed" aria-label="Notes for {cid}"></textarea></div>
</article>'''


def script():
    total = sum(len(s['cases']) for s in C.SUITES)
    body = ''
    for s in C.SUITES:
        note = f'<p style="font-size:.92rem;color:var(--ink-soft)">{s["note"]}</p>' if s.get('note') else ''
        body += (f'<div class="suite" id="suite-{s["id"]}"><h3>{s["id"]} · {esc(s["title"])} '
                 f'<small>{esc(s["who"])} · {len(s["cases"])} cases</small></h3>{note}'
                 + ''.join(case_html(s['id'], c) for c in s['cases']) + '</div>')
    return f'''<section class="block" id="script"><div class="wrap">
  <p class="eyebrow">UAT</p><h2>Test script</h2>
  <p class="lead">{total} cases in {len(C.SUITES)} suites. Start with ACC, then the round 2 suites (SCOPE, MRG, SEND), then the round 1 suites as a regression check. Each suite says who runs it. Mark each case Pass, Fail, Blocked or N/A. A Fail needs a note saying what you saw. Results stay in this browser until you export them. Send the CSV to SaaScend.</p>
  <div class="runbar">
    <div><label for="tester">Tester</label><input id="tester" autocomplete="name" placeholder="Your name"></div>
    <div><label for="rundate">Date</label><input id="rundate" type="date"></div>
    <div class="meter"><div class="bar" aria-hidden="true"><i id="m-pass" style="background:var(--pass)"></i><i id="m-fail" style="background:var(--fail)"></i><i id="m-blocked" style="background:var(--warn)"></i><i id="m-na" style="background:var(--na)"></i></div>
      <div class="txt" id="mtxt" aria-live="polite">0 of {total} recorded</div></div>
    <button class="btn primary" id="export" type="button">Export CSV</button>
    <button class="btn" id="print" type="button">Print / PDF</button>
    <button class="btn" id="reset" type="button">Clear results</button>
  </div>
  <p style="font-size:.9rem"><b>Release rule:</b> every case Pass (or N/A with a reason). A single Fail or Blocked holds the release.</p>
  {body}
</div></section>'''


def gaps():
    rows = ''.join(f'<tr><td>{esc(g)}</td><td>{esc(o)}</td><td>{esc(e)}</td></tr>' for g, o, e in C.KNOWN_GAPS)
    return f'''<section class="block" id="gaps"><div class="wrap">
  <p class="eyebrow">Before release</p><h2>Known gaps</h2>
  <p class="lead">None of these stop testing. Each needs an answer before the production plan is dated.</p>
  <div class="tblwrap"><table class="tbl"><tr><th>Open item</th><th>Owner</th><th>Effect today</th></tr>{rows}</table></div>
  <div class="callout"><b>Found while setting up this tester (25 Sep):</b> the desk, sync and Catalogue Manager edits worked for admins but were refused for ordinary users, because of a Salesforce API 67 permission default. Add Product also failed for everyone, since Business Unit is required and the form didn't ask for it. Both are fixed and re-verified as a non-admin user. This is why the script must be run as the tester, not as an admin.</div>
</div></section>'''


def signoff():
    rows = ''.join(f'<tr><td>{esc(r)}</td><td><input data-so="{i}-name" aria-label="{esc(r)} name"></td>'
                   f'<td><input data-so="{i}-date" type="date" aria-label="{esc(r)} date"></td>'
                   f'<td><input data-so="{i}-res" placeholder="Approved / Not yet" aria-label="{esc(r)} decision"></td></tr>'
                   for i, r in enumerate(C.SIGNOFF))
    return f'''<section class="block signoff" id="signoff"><div class="wrap">
  <p class="eyebrow">Gate</p><h2>Sign-off</h2>
  <p class="lead">Release planning starts once every role below has signed off on a clean run.</p>
  <div class="tblwrap"><table class="tbl"><tr><th>Role</th><th>Name</th><th>Date</th><th>Decision</th></tr>{rows}</table></div>
</div></section>'''


JS = r'''
(function(){
  var KEY='dxr-pricing-uat-v2', st={};
  try{ st=JSON.parse(localStorage.getItem(KEY)||'{}')||{}; }catch(e){ st={}; }
  st.r=st.r||{}; st.n=st.n||{}; st.so=st.so||{};
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(st)); }catch(e){} }
  var cases=[].slice.call(document.querySelectorAll('.case')), total=cases.length;
  function paint(){
    var c={pass:0,fail:0,blocked:0,na:0};
    cases.forEach(function(el){ var v=st.r[el.dataset.id]; if(v){c[v]++; el.dataset.r=v;} else el.removeAttribute('data-r');
      el.querySelectorAll('.seg button').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.v===v?'true':'false'); }); });
    ['pass','fail','blocked','na'].forEach(function(k){ document.getElementById('m-'+k).style.width=(100*c[k]/total)+'%'; });
    var done=c.pass+c.fail+c.blocked+c.na;
    document.getElementById('mtxt').textContent=done+' of '+total+' recorded · '+c.pass+' pass · '+c.fail+' fail · '+c.blocked+' blocked · '+c.na+' n/a';
  }
  cases.forEach(function(el){
    var id=el.dataset.id, ta=el.querySelector('textarea');
    ta.value=st.n[id]||'';
    ta.addEventListener('input',function(){ st.n[id]=ta.value; save(); });
    el.querySelectorAll('.seg button').forEach(function(b){ b.addEventListener('click',function(){
      st.r[id]= st.r[id]===b.dataset.v ? undefined : b.dataset.v; if(!st.r[id]) delete st.r[id]; save(); paint(); }); });
  });
  var tester=document.getElementById('tester'), rd=document.getElementById('rundate');
  tester.value=st.tester||''; rd.value=st.date||new Date().toISOString().slice(0,10);
  tester.addEventListener('input',function(){ st.tester=tester.value; save(); });
  rd.addEventListener('input',function(){ st.date=rd.value; save(); });
  document.querySelectorAll('[data-so]').forEach(function(i){ i.value=st.so[i.dataset.so]||'';
    i.addEventListener('input',function(){ st.so[i.dataset.so]=i.value; save(); }); });
  function q(s){ s=String(s==null?'':s); return /[",\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s; }
  document.getElementById('export').addEventListener('click',function(){
    var rows=[['Case','Suite','Title','Result','Notes','Tester','Date']];
    cases.forEach(function(el){ var id=el.dataset.id; rows.push([id,el.dataset.suite,el.dataset.title,st.r[id]||'',st.n[id]||'',tester.value,rd.value]); });
    var blob=new Blob([rows.map(function(r){return r.map(q).join(',');}).join('\n')],{type:'text/csv'});
    var a=document.createElement('a'); a.href=URL.createObjectURL(blob);
    a.download='dxr-pricing-uat-'+(tester.value||'tester').replace(/\W+/g,'-').toLowerCase()+'-'+rd.value+'.csv';
    document.body.appendChild(a); a.click(); setTimeout(function(){URL.revokeObjectURL(a.href); a.remove();},500);
  });
  document.getElementById('print').addEventListener('click',function(){ window.print(); });
  document.getElementById('reset').addEventListener('click',function(){
    if(!confirm('Clear every result and note in this browser?')) return; st.r={}; st.n={}; save();
    cases.forEach(function(el){ el.querySelector('textarea').value=''; }); paint(); });
  paint();
})();
'''


def page():
    return f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>DXR Cyber Pricing Desk UAT</title>
<meta name="description" content="Demo guide, enablement and UAT test script for the DXR Cyber Pricing Desk, approvals, e-signature and scoping (sandbox).">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23031F49'/%3E%3Cpath d='M8 23 16 8l8 15' stroke='%2300ACD4' stroke-width='3.5' fill='none' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Open+Sans:wght@400;600;700&display=swap">
<style>{CSS}</style></head><body>
{hero()}{toc()}
<main>{round2()}{access()}{how()}{demo()}{reps()}{catalogue()}{docgen()}{script()}{gaps()}{signoff()}</main>
<footer><div class="wrap"><img src="data:image/png;base64,{LOGO}" alt="SaaScend">Prepared by SaaScend for DXR Cyber · sandbox builds XYP-PRICING-001–009, XYP-SCOPE-001–002 · 21 Oct 2026 · internal, not for customers</div></footer>
<script>{JS}</script></body></html>'''


if __name__ == '__main__':
    out = os.path.join(ROOT, 'index.html')
    open(out, 'w').write(page())
    print('wrote', out, os.path.getsize(out), 'bytes;', sum(len(s['cases']) for s in C.SUITES), 'cases')

# Xypher Pricing Desk & Order Form: demo, enablement and UAT test script

Live at **https://saascend-org.github.io/xypher-pricing-desk-uat/**

SaaScend-branded, single self-contained page for Xypher's sandbox testers (`Xypher_Sandbox_FC`):
access and links, how it works, a 15-minute demo walkthrough, rep and catalogue-manager enablement,
how the order form is generated (and the phase 2 PandaDoc e-signature plan), a 40-case interactive
test script (Pass/Fail/Blocked/N/A, notes, CSV export, remembered per browser), known gaps and sign-off.

- `noindex` is deliberate: the URL is shareable but this is internal material.
- Only `[DEMO]` (fictional) records are referenced. No credentials, no cost or margin figures.
- Source: `content.py` (all text, ids and figures) + `build.py` in `~/Work/SaaScend/Xypher/pricing-desk-guide/`.
  Edit those and run `python3 build.py`; never edit `index.html` by hand.

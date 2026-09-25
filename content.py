"""Content for the Pricing Desk demo, enablement and UAT test script page.

Every figure, id and label here was read from Xypher_Sandbox_FC on 25 Sep 2026.
Edit this file, then run build.py. Never edit index.html by hand.
"""

L = 'https://xypher--saascendfc.sandbox.lightning.force.com'
LOGIN = 'https://xypher--saascendfc.sandbox.my.salesforce.com'

OPP = {
    'A': '006Pu00000aoVYgIAM',   # Harbourline, synced
    'B': '006Pu00000aoXC9IAM',   # Kestrel & Vane, synced
    'C': '006Pu00000ao64rIAA',   # Northshire, Ready + Blocked
    'E': '006Pu00000aoXFNIA2',   # Brightwater, empty
}
QUOTE = {'A': '0Q0Pu000007ptt0KAA', 'B': '0Q0Pu000007pvBVKAY',
         'C': '0Q0Pu000007pvD7KAI', 'D': '0Q0Pu000007pvD8KAI'}


def opp(k):
    return f'{L}/lightning/r/Opportunity/{OPP[k]}/view'


def quote(k):
    return f'{L}/lightning/r/Quote/{QUOTE[k]}/view'


def desk(k):
    return f'{L}/lightning/n/Xypher_Pricing_Desk?c__oppId={OPP[k]}'


CATALOGUE = f'{L}/lightning/n/Xypher_Catalogue'
ACCOUNT = {'A': '001Pu00000wluqNIAQ', 'B': '001Pu00000wlv35IAA', 'C': '001Pu00000wlIVEIA2', 'E': '001Pu00000wlvB9IAI'}
PDF = {'A': '0QDPu0000007XC9OAM', 'B': '0QDPu0000007XDlOAM'}   # latest QuoteDocument per synced deal
PRODUCT = {'SOC-CORE-1.5TB-OPS': '01tPu00000JNMC1IAP', 'SOC-MON': '01tPu00000JNMF9IAP',
           'GRC-CE-002': '01tPu00000JNCL8IAP', 'LIMA-LIC-PRO-PRI-3Y-002': '01tPu00000JNALxIAP'}


def rec(obj, rid):
    return f'{L}/lightning/r/{obj}/{rid}/view'


def pdf(k):
    return f'{L}/servlet/servlet.FileDownload?file={PDF[k]}'


# Per-deal record links: (deal, [(label, url), ...])
RECORDS = [
    ('A · Harbourline - Managed SOC', [('Opportunity', opp('A')), ('Account', rec('Account', ACCOUNT['A'])),
        ('Quote (synced)', quote('A')), ('Desk', desk('A')), ('Order form PDF', pdf('A'))]),
    ('B · Kestrel & Vane - LIMA and Forensics', [('Opportunity', opp('B')), ('Account', rec('Account', ACCOUNT['B'])),
        ('Quote (synced)', quote('B')), ('Desk', desk('B')), ('Order form PDF', pdf('B'))]),
    ('C/D · Northshire - Cyber Essentials and Pen Test', [('Opportunity', opp('C')), ('Account', rec('Account', ACCOUNT['C'])),
        ('Quote C (Ready)', quote('C')), ('Quote D (Blocked)', quote('D')), ('Desk', desk('C'))]),
    ('E · Brightwater - build a quote live', [('Opportunity', opp('E')), ('Account', rec('Account', ACCOUNT['E'])),
        ('Desk', desk('E'))]),
    ('Catalogue', [('Xypher Catalogue app', CATALOGUE),
        ('SOC-CORE-1.5TB-OPS', rec('Product2', PRODUCT['SOC-CORE-1.5TB-OPS'])),
        ('SOC-MON', rec('Product2', PRODUCT['SOC-MON'])), ('GRC-CE-002', rec('Product2', PRODUCT['GRC-CE-002'])),
        ('Change Log (all)', f'{L}/lightning/o/Catalogue_Change_Log__c/list')]),
]

LINKS = [
    ('Sandbox login', LOGIN, 'Log in as the tester here (sandbox, not production)'),
    ('Pricing Desk: Brightwater (build a quote)', desk('E'), 'The empty opportunity the test script uses'),
    ('Xypher Catalogue', CATALOGUE, 'Products, Data Quality, Change Log, Cost Upload'),
    ('[DEMO] Harbourline - Managed SOC', opp('A'), 'Synced SOC deal, order form already generated'),
    ('[DEMO] Kestrel & Vane - LIMA and Forensics', opp('B'), 'Synced, two service lines on one order form'),
    ('[DEMO] Northshire - Cyber Essentials and Pen Test', opp('C'), 'One Ready quote to sync live, one Blocked at 45%'),
    ('[DEMO] Brightwater - build a quote live', opp('E'), 'Empty. Build from scratch'),
    ('Northshire Ready quote (record)', quote('C'), 'Standard Quote record, used for the bypass check'),
]

TESTER = {
    'name': 'UAT Pricing Tester',
    'username': 'uat.pricing.tester@xypher.uat.invalid',
    'profile': 'Standard User, role Sales Pod 1 - AE, Business Unit DXR',
    'psets': ['Standard_User_Baseline', 'Xypher_Opportunity_Management', 'Xypher_Zoho_Legacy_Fields',
              'Xypher_Pricing_Desk_User', 'PandaDocUser', 'Xypher_Catalogue_Manager'],
}

DEMO_RECORDS = [
    ('A', '[DEMO] Harbourline - Managed SOC', 'Synced. Amount £344,595, annual £114,865, 11 products. Order form on the Quote',
     'The SOC tier bundle, Low maturity, 90-day SIEM tier (qty 12), 10% off operational effort'),
    ('B', '[DEMO] Kestrel & Vane - LIMA and Forensics', 'Synced. Amount £55,920, annual £17,440 + £3,600 one-off. Order form on the Quote',
     'Licences plus an hourly project: two delivery sections, the one-off lands in year 1'),
    ('C', '[DEMO] Northshire - Cyber Essentials and Pen Test', 'Quote "Cyber Essentials Small + penetration test": Ready, not synced (£6,915)',
     'Sync live and watch Amount and Products fill in, then Generate PDF'),
    ('D', 'Same opportunity as C', 'Quote "Same scope at 45% - over the cap": Blocked',
     'The 40% cap: red row, Sync & Confirm and Generate PDF disabled'),
    ('E', '[DEMO] Brightwater - build a quote live', 'Empty, no quote', 'Build from scratch. The test script uses this one'),
]

# ── Test script ─────────────────────────────────────────────────────────────────────────────
# Each case: (id, title, [steps], expected). Steps and expected results may hold inline HTML.
SUITES = [
    {
        'id': 'ACC', 'title': 'Access and navigation', 'who': 'Everyone, first',
        'cases': [
            ('ACC-01', 'Log in as the tester',
             [f'Open <a href="{LOGIN}" target="_blank" rel="noopener">the sandbox login</a>.',
              'Log in as <code>uat.pricing.tester@xypher.uat.invalid</code> with the password SaaScend gave you.'],
             'The Sales app Home page loads. The banner reads <b>Sandbox (SaaScendFC)</b>.'),
            ('ACC-02', 'Find the launcher on an Opportunity',
             [f'Open <a href="{opp("E")}" target="_blank" rel="noopener">[DEMO] Brightwater - build a quote live</a>.',
              'Click the <b>Pricing Desk</b> tab on the record.'],
             'A card shows <b>Open Pricing Desk</b>. No error or "insufficient access" message.'),
            ('ACC-03', 'Open the Catalogue app',
             ['App Launcher (the 9 dots) → search <b>Xypher Catalogue</b> → open it.'],
             'The Products tab loads with a count of the form <b>N of 732 products</b>.'),
        ],
    },
    {
        'id': 'DESK', 'title': 'Build a quote', 'who': 'Sales reps',
        'note': 'Run in order on <b>[DEMO] Brightwater</b>. The figures assume every earlier step was done, at catalogue v2 prices.',
        'cases': [
            ('DESK-01', 'Open the desk',
             ['On Brightwater, go to the Pricing Desk tab and click <b>Open Pricing Desk</b>.'],
             'The desk opens full-width. It shows the Opportunity name, account and stage, a <b>Back to Opportunity</b> link, and no quotes yet.'),
            ('DESK-02', 'New quote defaults',
             ['Click <b>New Quote</b>.'],
             'Commercial terms default to <b>Annually in advance</b>, <b>30 days from invoice</b> and <b>Xypher Standard Terms v1.0</b>. There is no "blocked" banner.'),
            ('DESK-03', 'Browse by service line',
             ['In Add Products, click a service-line chip, e.g. <b>Cyber Essentials</b>.'],
             'Products for that service line are listed with price and revenue class, each with an <b>Add</b> button.'),
            ('DESK-04', 'Add a SOC package',
             ['Name the quote. Set <b>Term (months)</b> to <b>36</b>.',
              'Search <code>SOC-CORE-1.5TB-OPS</code> and click <b>Add</b>.'],
             '<b>10 lines</b> appear: the operational-effort line, 8 components tagged <i>Mandatory Bundle</i> and <b>SOC Monitoring (Standard Effort)</b> tagged <i>Choice</i>. Quote Summary: <b>Annual recurring £89,095</b>, <b>TCV £267,285</b>.'),
            ('DESK-05', 'Mandatory lines are locked',
             ['Try to delete one of the <i>Mandatory Bundle</i> lines.'],
             'You can\'t remove it on its own: the delete control is disabled. Only the parent line removes the package.'),
        ],
    },
    {
        'id': 'BND', 'title': 'Bundles and choices', 'who': 'Sales reps',
        'cases': [
            ('BND-01', 'Open the bundle panel',
             ['Click the operational-effort line.'],
             '<b>Bundle &amp; Add-ons</b> lists the locked mandatory items. <b>Maturity level (choose one)</b> has 5 options with Standard selected. <b>SIEM platform, optional, one at most</b> offers None plus the 30, 90 and 180-day options.'),
            ('BND-02', 'Switch maturity',
             ['Select <b>Low Maturity (High Effort)</b>.'],
             'The Standard line is replaced, so there is still exactly one maturity line. Annual recurring becomes <b>£93,595</b>.'),
            ('BND-03', 'Add a SIEM platform tier',
             ['Select the <b>90 Days Retention</b> SIEM option.',
              'Then select 30 days, then 90 days again.'],
             'It is added with <b>qty 12</b>, because it is priced monthly. Choosing another tier replaces it; there is never more than one. With 90 days, annual is <b>£118,015</b>.'),
        ],
    },
    {
        'id': 'DISC', 'title': 'Discounts and the 40% cap', 'who': 'Sales reps',
        'cases': [
            ('DISC-01', 'Over the cap blocks the quote',
             ['Type <b>45</b> in the operational-effort line\'s <b>Adj.</b> box.', 'Click <b>Save</b>.'],
             'The row turns red with <b>Max 40%</b>. The quote saves as <b>Blocked</b> with a red banner. <b>Sync &amp; Confirm</b> and <b>Generate PDF</b> are disabled.'),
            ('DISC-02', 'Bring it under the cap',
             ['Change the adjustment to <b>20%</b>. Backspace and retype normally.', 'Click <b>Save</b>.'],
             'Annual <b>£111,715</b>, TCV <b>£335,145</b>. Status is <b>Ready</b>. Sync is enabled.'),
            ('DISC-03', 'Other adjustment formats',
             ['On another line try <code>£250</code> (amount off), <code>+8%</code> (uplift) and <code>+£500</code> in turn.',
              'Set it back to <b>0</b> and Save.'],
             'Each value recalculates the line immediately. Uplifts raise the price. Back at 0, the totals return to DISC-02\'s figures.'),
        ],
    },
    {
        'id': 'SYNC', 'title': 'Sync to the Opportunity', 'who': 'Sales reps',
        'cases': [
            ('SYNC-01', 'Sync & Confirm',
             ['Click <b>Sync &amp; Confirm</b>.'],
             'A success message appears. The quote shows as <b>Synced</b>.'),
            ('SYNC-02', 'The Opportunity reflects the quote',
             ['Click <b>Back to Opportunity</b> and refresh.'],
             '<b>Amount = £335,145</b> (TCV), 11 Opportunity Products. The <b>Quote Summary</b> shows annual recurring £111,715 and a 36-month term. Gross profit shows <i>1 of 11 lines costed</i>, because most SOC costs are not loaded yet.'),
            ('SYNC-03', 'Edits flow through without re-syncing',
             ['Re-open the quote, change 20% to <b>10%</b>, then Save.'],
             'The Opportunity updates by itself: <b>Amount £344,595</b>.'),
            ('SYNC-04', 'Save as a new version',
             ['Click <b>Save as New Quote</b>.'],
             'A second quote appears in the list, <b>not synced</b>. The Opportunity Amount is unchanged.'),
            ('SYNC-05', 'The cap can\'t be bypassed',
             [f'Open the <a href="{quote("C")}" target="_blank" rel="noopener">Northshire Ready quote</a> record.',
              'Use Salesforce\'s own <b>Edit Products / Lines</b> to set a line discount of <b>50</b>, then try <b>150</b>.'],
             'Both are refused: over the 40% limit, and over 100%. Cancel the edit.'),
            ('SYNC-06', 'Sync a saved quote live (demo C)',
             [f'Open the desk on <a href="{desk("C")}" target="_blank" rel="noopener">[DEMO] Northshire</a>.',
              'Open <b>Cyber Essentials Small + penetration test</b> and click <b>Sync &amp; Confirm</b>.'],
             'The Opportunity Amount becomes <b>£6,915</b> and the products fill in. The 45% quote on the same deal stays Blocked.'),
        ],
    },
    {
        'id': 'DOC', 'title': 'Order form (document generation)', 'who': 'Sales reps, deal desk',
        'cases': [
            ('DOC-01', 'Generate the order form',
             ['On your Brightwater quote, click <b>Generate PDF</b>.'],
             'The PDF opens in a new browser tab. It is also saved on the Quote: open the Quote record, and it is under <b>Quote PDFs</b>.'),
            ('DOC-02', 'Check the content',
             ['Read the PDF you just generated.'],
             'DXR Cyber branding, marked <b>DRAFT</b>. It shows the customer <b>Brightwater Academy Trust</b>, contact <b>Tom Ashby</b> and the billing address, with the lines and discount matching the desk. There is one delivery section for the Managed SOC service line and a 3-year payment schedule. <b>No cost or margin appears anywhere.</b>'),
            ('DOC-03', 'Placeholders are visible, not blank',
             ['Look at the contracting entity, company and VAT numbers, and the terms URL.'],
             'They show as <b style="color:#c2410c">orange placeholders</b>. This is expected until Xypher supplies the details.'),
            ('DOC-04', 'Multi-service-line deal',
             [f'Open <a href="{opp("B")}" target="_blank" rel="noopener">[DEMO] Kestrel &amp; Vane</a> → its Quote → <b>Quote PDFs</b> → open the PDF.'],
             'Two service lines give <b>two delivery sections</b>. The £3,600 one-off sits in <b>year 1</b> of the payment schedule.'),
            ('DOC-05', 'Blocked quotes can\'t produce a document',
             ['On Northshire, open the <b>Same scope at 45%</b> quote in the desk.'],
             '<b>Generate PDF</b> is disabled.'),
            ('DOC-06', 'Re-generate after a change',
             ['Change a discount on your Brightwater quote, Save, then Generate PDF again.'],
             'A second PDF is added under Quote PDFs with the new figures. The first one is kept.'),
        ],
    },
    {
        'id': 'CAT', 'title': 'Catalogue management', 'who': 'Catalogue managers (Lisa, Stuart)',
        'note': 'Use a throwaway product you create in CAT-02, so no real product is changed. Retire it at the end (CAT-08).',
        'cases': [
            ('CAT-01', 'Find products',
             ['In <b>Xypher Catalogue → Products</b>, filter by a service line, then search a SKU such as <code>GRC-CE-002</code>.'],
             'The grid narrows and shows the SKU, name, service line, revenue class, £ price and cost.'),
            ('CAT-02', 'Add a product',
             ['Click <b>Add Product</b>. Name <code>[UAT] Test product</code>, SKU <code>UAT-TEST-001</code>, Business Unit DXR, revenue class One-Off, list price £100. Save.'],
             'It appears in the grid. The <b>Change Log</b> has a <b>Create</b> entry under your name. In the Pricing Desk, searching <code>UAT-TEST-001</code> finds it at £100.'),
            ('CAT-03', 'Edit a field inline',
             ['In the grid, click the test product\'s name, change it to <code>[UAT] Test product (edited)</code> and click away.'],
             'Saved without a separate Save button. The Change Log records an <b>Edit</b> with the old and new values.'),
            ('CAT-04', 'Reprice',
             ['In the grid, change the test product\'s list price from £100 to <b>£120</b> and click away.'],
             'The grid shows £120 and the desk quotes it at £120 on a new line. The Change Log records a <b>Reprice</b>.'),
            ('CAT-05', 'Hide and unhide',
             ['Tick <b>Hidden From Quoting</b> on the test product. Refresh the desk and search for it.', 'Untick it again.'],
             'Hidden, it is not found in desk search; unhidden, it is found again. The log records <b>Hide</b>, then <b>Unhide</b>.'),
            ('CAT-06', 'Bundle a component',
             ['Open the test product → Bundle editor → add <code>GRC-CE-006</code> as <b>Optional / Additional</b>.',
              'In the desk, add the test product to a quote. Then remove the component in the Catalogue.'],
             'The desk offers GRC-CE-006 as an add-on for the test product. The log records <b>Bundle Add</b>, then <b>Bundle Remove</b>.'),
            ('CAT-07', 'Data Quality',
             ['Open the <b>Data Quality</b> tab.'],
             'Tiles show counts, e.g. <b>No cost loaded</b>, <b>Service Line gap</b> and <b>Leftover -CH product codes</b>.'),
            ('CAT-08', 'Retire (clean-up)',
             ['Retire the test product.'],
             'A confirmation asks you to be sure (and lists any bundle that still depends on it). Once it is retired, the desk no longer finds it. The log records <b>Retire</b>.'),
        ],
    },
    {
        'id': 'COST', 'title': 'Cost upload and GP', 'who': 'Catalogue managers',
        'note': 'Run before CAT-08, while the test product is still active.',
        'cases': [
            ('COST-01', 'Preview a cost file',
             ['<b>Cost Upload</b> tab. Paste:<pre>SKU,Cost\nUAT-TEST-001,60\nNOT-A-SKU,10\nUAT-TEST-001,70\nGRC-CE-002,abc</pre>', 'Click <b>Preview Upload</b>.'],
             'Each row gets a status: <b>matched</b>, <b>unknown SKU</b>, <b>duplicate in file</b> and <b>invalid number</b>. Nothing has changed yet.'),
            ('COST-02', 'Apply only good rows',
             ['Paste just <code>SKU,Cost</code> / <code>UAT-TEST-001,60</code>. <b>Preview Upload</b>, then <b>Apply Cost Upload</b>.'],
             'The test product\'s cost is £60. The Change Log records a <b>Cost Change</b> from blank to 60.'),
            ('COST-03', 'Costs drive GP on the desk',
             ['In the desk, add the test product (list £120, cost £60) to a quote.'],
             'That line shows cost <b>£60</b> and GP <b>£60 (50%)</b>. The Quote Summary GP coverage counts one more costed line.'),
        ],
    },
    {
        'id': 'PERM', 'title': 'Controls', 'who': 'Deal desk / admin',
        'cases': [
            ('PERM-01', 'The Change Log is read-only',
             ['Open a Change Log entry and look for Edit or Delete.'],
             'Neither is available. The log can\'t be changed.'),
            ('PERM-02', 'Prices only change through the Catalogue',
             ['As the tester, open a product\'s Price Book entry in standard Salesforce and try to edit the list price.'],
             'Refused, because Manage Price Books is not granted. The Catalogue app is the only route, and it logs every change.'),
            ('PERM-03', 'Reps can\'t reach the Catalogue',
             ['(Admin) Setup → Permission Sets → <b>Xypher Pricing Desk User</b> → Object Settings / Apex Class Access.'],
             'It grants the desk classes but not <code>CatalogueManagerController</code> or the Xypher Catalogue tab. Only <b>Xypher Catalogue Manager</b> does.'),
        ],
    },
]

KNOWN_GAPS = [
    ('Contracting entity, company/VAT numbers, terms URL', 'Xypher (Dan / finance)', 'Order forms print DRAFT with orange placeholders until supplied'),
    ('One-off invoicing trigger (on acceptance vs on completion)', 'Sarah / finance', 'The order form says "on acceptance"'),
    ('Delivery module wording (27 modules)', 'Each delivery team', 'SaaScend drafts, no SLA numbers. Edited in Setup, no deploy'),
    ('Catalogue v2 open questions: maturity multiplier, USD FX rate, 14 unpriced products, SOC-PRO-UCD, SOC-QBR price, "Annual Rate" label on monthly lines', 'Lisa Washer', 'Affects some prices and labels, not the mechanics'),
    ('Costs: 613 products have none loaded; 13 are in USD', 'Lisa Washer', 'GP shows "N of M lines costed" until loaded'),
    ('Brand font Sailec (Figtree is the stand-in)', 'Xypher marketing', 'Cosmetic'),
    ('PandaDoc e-signature', 'SaaScend + Xypher', 'Phase 2, see "Document generation"'),
    ('Production plan: enabling Quotes can\'t be undone', 'Tej + Xypher', 'Needs a dated cut-over and sign-off'),
]

SIGNOFF = ['Sales (rep) tester', 'Catalogue manager', 'Deal desk / finance', 'Xypher sponsor', 'SaaScend (build lead)']

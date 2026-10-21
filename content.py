"""Content for the Pricing Desk demo, enablement and UAT test script page.

Round 1 figures, ids and labels were read from Xypher_Sandbox_FC on 25 Sep 2026; round 2
(XYP-PRICING-006/007/008/009, XYP-SCOPE-002) on 21 Oct 2026.
Client-facing text says DXR Cyber; "Xypher" appears only in real on-screen labels and identifiers.
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
     'Over 40% on a line with no cost: needs manager approval, so Sync & Confirm and Generate PDF stay locked'),
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
    },    {
        'id': 'SCOPE', 'title': 'Scoping: rep or customer, and verification', 'who': 'Sales reps, technical verifiers',
        'note': 'Use your own <code>[UAT]</code> opportunity with <code>PT-WEB-001</code> (web application pen test) on it. For SCOPE-01, 02 and 04, add a test contact with <b>your own email address</b> so the secure link comes to you. SCOPE-05 and 06 need a <b>technical verifier</b> (DXR Scoping Technical) who did not complete the form.',
        'cases': [
            ('SCOPE-01', 'Send the scoping form to the customer',
             ['On the Opportunity, click <b>Request Scoping</b>. Confirm the service and pick your test contact.',
              'Choose <b>Send it to the contact to complete</b> and click Next.'],
             '"Sent to <i>contact</i>", with reminders at day 3 and day 7. The Scoping Document shows Stage <b>Sent</b> and Completion Method <b>Customer</b>. Its questionnaire is <b>read-only</b>, with the banner "This form is with the customer".'),
            ('SCOPE-02', 'Complete it as the customer',
             ['Open the email that arrived, click <b>Complete the scoping form</b>, answer the questions and click <b>Submit scope</b>.'],
             'The form asks only about the service in scope and shows no prices. Back in Salesforce the document is <b>Received</b>, with the answers on the record.'),
            ('SCOPE-03', 'Complete it yourself (e.g. on the scoping call)',
             ['New opportunity: <b>Request Scoping</b>, choose <b>I\'ll complete it myself now</b>, Next.',
              'Answer two questions, click <b>Save progress</b>, then <b>Finish</b>. Re-open the Scoping Document, finish the answers and click <b>Submit scope</b>.'],
             'The questionnaire opens inside the flow, and saved answers are still there when you come back. On submit: Stage <b>Received</b>, Completion Method <b>Sales rep</b>, Completed By <b>you</b>.'),
            ('SCOPE-04', 'Take a sent form back',
             ['Send a form to your test contact (as SCOPE-01) but don\'t complete it. On the Scoping Document click <b>Complete it myself</b>, confirm, and fill it in.',
              'Now open the link in the email.'],
             'The warning says the customer\'s link will stop working. After you confirm, the questionnaire is editable and Stage is back to <b>Requested</b>. The old link says <b>"This link has been withdrawn"</b>.'),
            ('SCOPE-05', 'Verify and close (technical verifier)',
             ['As a technical verifier, open a <b>Received</b> scoping document you didn\'t complete and click <b>Close Scoping</b>.',
              'Click Next without ticking. Then tick <b>I have checked these figures…</b>, add a verification note and click Next.'],
             'Without the tick it won\'t continue. With it: "Scoping verified and closed". <b>Verified By</b> is you, with the date and your note. The scoping PDF in the Opportunity\'s Files prints <b>Verified by <i>you</i></b> and the note.'),
            ('SCOPE-06', 'Verification controls',
             ['As a rep (not a verifier), open a Received scoping document.',
              'As a verifier, try to close a scope <b>you</b> completed yourself (SCOPE-03).'],
             'The rep has no <b>Close Scoping</b> button. The verifier sees "You completed this scope yourself, so another member of the technical team must verify and close it."'),
        ],
    },
    {
        'id': 'MRG', 'title': 'Margin, GP and approvals', 'who': 'Sales reps, managers',
        'note': '<b>Most products have no cost yet</b> (see the banner at the top). Cases marked <b>costed</b> use <code>GRC-CE-009</code> (Cyber Essentials Support Consultancy), one of the 144 products that have a cost. Use a fresh <code>[UAT]</code> opportunity for this suite.',
        'cases': [
            ('MRG-01', 'The desk layout',
             ['New Quote. Add <code>GRC-CE-009</code> from the side search.'],
             'After the first line, the search becomes a compact bar above the lines, which use the full width. <b>Show catalogue</b> brings the side panel back, and the page remembers your choice. The <b>Margin</b> card shows a bar against the <b>40% minimum</b>.'),
            ('MRG-02', 'Below 40% GP needs approval (costed)',
             ['On <code>GRC-CE-009</code>, set <b>Adj.</b> to <b>60%</b>.'],
             'The Margin card says GP is below the 40% minimum and suggests <b>"Cut the discount … to 57%"</b> with an <b>Apply</b> button. The banner reads <b>Needs manager approval</b>.'),
            ('MRG-03', 'Apply the fix',
             ['Click <b>Apply</b> on the suggestion.'],
             'The discount becomes 57%, GP passes 40%, and the approval banner clears. Status: <b>Ready</b>.'),
            ('MRG-04', 'A line with no cost',
             ['Add <code>PT-WEB-001</code> (no cost loaded). Set its <b>Adj.</b> to <b>30%</b>, then to <b>45%</b>.'],
             'The action bar shows <b>GP n/a · 1 line uncosted</b> instead of a percentage (hover for the costed-lines figure). The Margin card says GP can\'t be checked. 30% needs no approval; 45% shows <b>Over 40%: needs approval</b>.'),
            ('MRG-05', 'Save & Submit, then Recall',
             ['With the 45% line in place, click <b>Save &amp; Submit for Approval</b>. Read the pre-filled reason and click OK.',
              'Then click <b>Recall</b>.'],
             'The reason names the line, the 40% rule and "1 of 2 lines has no cost". The quote shows <b>Awaiting <i>your manager</i></b> and is locked. Recall unlocks it, back to Approval Required.'),
            ('MRG-06', 'Manager approves or rejects',
             ['Submit again. <b>Manager:</b> open the approval request (the bell, or the Approvals tab), read the reason and approve. On a second quote, reject with a comment.'],
             'Approved: the rep is notified, the quote is <b>Ready · Approved</b>, and Generate PDF and Sync unlock. <b>Nothing is sent to the customer</b> (this was a price approval, Signature Status Not Sent). Rejected: the desk shows the comment and an <b>Edit &amp; Resubmit</b> button.'),
            ('MRG-07', 'Partner discount',
             ['(Set-up: an Account with Type <b>Partner</b> and a <b>Partner Discount %</b>, added as the primary partner on the opportunity.) New Quote, add <code>GRC-CE-009</code>.'],
             'A banner names the partner discount, which is pre-filled on eligible service lines with a <b>Partner</b> tag. Licences, third-party costs, hardware and channel-priced lines are not discounted. Typing your own adjustment removes the tag.'),
        ],
    },
    {
        'id': 'SEND', 'title': 'Send for e-signature (PandaDoc)', 'who': 'Sales reps, managers',
        'note': 'In the sandbox, PandaDoc sends <b>silently to a SaaScend test inbox</b>, so no customer email arrives and nobody can sign for real. At SEND-04, post the quote name in the test channel and SaaScend marks it signed in PandaDoc. Status checks run every 15 minutes.',
        'cases': [
            ('SEND-01', 'Locked before Proposal',
             ['On a <code>[UAT]</code> opportunity at <b>Qualify</b>, open a Ready quote in the desk.'],
             '<b>Request to Send</b> is greyed out with <b>Unlocks at Proposal</b> under it (hover to see why). Save, approvals and Generate PDF still work.'),
            ('SEND-02', 'Request to Send',
             ['Move the opportunity to <b>Proposal / Bid Submitted</b> (the usual stage gates apply). Open the quote, click <b>Request to Send</b>, add a note and click OK.'],
             'The quote is locked: <b>Awaiting <i>your manager</i> · approval to send the order form</b>. If the price also needed approval, this one approval covers both.'),
            ('SEND-03', 'Manager approves, and that sends it (DXR Cyber\'s acceptance)',
             ['<b>Manager:</b> open the request from the bell or <b>Home → Items to Approve</b>. Check it says <b>Signature Status: Requested</b>, then click <b>Approve</b>.', '<b>Rep:</b> do nothing else; refresh the desk after a minute or two.'],
             'The approval alone triggers the send: status goes <b>Sending</b>, then <b>Out for signature</b> with a <b>View in PandaDoc</b> link, and no other click is needed. (In the sandbox the PandaDoc email goes to a SaaScend inbox; in production it goes to the customer.) The Opportunity now matches the quote: <b>Amount = the quote TCV</b>, Products filled in, Document Status <b>Sent</b>. The order form carries the manager\'s acceptance line.'),
            ('SEND-04', 'Customer signs (simulated by SaaScend)',
             ['Ask SaaScend to mark it signed. Wait for the next status check (up to 15 minutes), then refresh.'],
             'The desk shows <b>Signed</b>, and the <b>signed order form</b> is in Files on the Quote and the Opportunity. Contract Start is the signing date and Contract End is start + term − 1 day, on both. The stage is <b>not</b> moved: the owner gets a notification and a Task, <b>"Close Won: signed order form received"</b>, and the deal appears in the list view <b>Signed, not yet Closed Won</b>.'),
            ('SEND-05', 'Revise & Resend',
             ['On another sent quote, click <b>Revise &amp; Resend</b> and confirm.'],
             'It shows "Withdrawing…", then <b>Not Sent</b> once PandaDoc confirms. You can edit the quote and send it again, which needs approval again.'),
            ('SEND-06', 'No manager, no send',
             ['(Admin) Clear the tester\'s Manager, try Request to Send, then put the Manager back.'],
             'Refused: "No manager is set on your Salesforce user, so nobody can approve this send."'),
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
        'id': 'DISC', 'title': 'Discounts and the 40% rule', 'who': 'Sales reps',
        'cases': [
            ('DISC-01', 'Over 40% needs approval',
             ['Type <b>45</b> in the operational-effort line\'s <b>Adj.</b> box.', 'Click <b>Save</b>.'],
             'The line shows <b>Over 40%: needs approval</b> and an amber <b>Needs manager approval</b> banner appears (most SOC lines have no cost yet, so the 40% discount rule applies). The quote saves as <b>Approval Required</b>. <b>Sync &amp; Confirm</b> and <b>Generate PDF</b> stay locked until a manager approves. Don\'t submit it here; the MRG suite covers approvals.'),
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
            ('SYNC-05', 'The rule can\'t be bypassed',
             ['On your synced Brightwater quote, open the Quote record and use Salesforce\'s own <b>Edit Products / Lines</b> to set a line discount of <b>50</b>, then try <b>150</b>.'],
             'Both are refused: 50% "needs approval, and a synced quote cannot carry it"; 150% is over 100%. Cancel the edit.'),
            ('SYNC-06', 'Sync a saved quote live (demo C)',
             [f'Open the desk on <a href="{desk("C")}" target="_blank" rel="noopener">[DEMO] Northshire</a>.',
              'Open <b>Cyber Essentials Small + penetration test</b> and click <b>Sync &amp; Confirm</b>.'],
             'The Opportunity Amount becomes <b>£6,915</b> and the products fill in. The 45% quote on the same deal stays Blocked.'),
        ],
    },
    {
        'id': 'DATE', 'title': 'Contract dates and part-term lines', 'who': 'Sales reps, deal desk',
        'note': 'Run after SYNC, on a <b>New Quote</b> on [DEMO] Brightwater with just the ISO 27001 line. Syncing it replaces the SYNC suite\'s quote on that deal. £1,100/yr is the catalogue v2 price.',
        'cases': [
            ('DATE-01', 'Contract start and the calculated end',
             ['New Quote, term <b>36</b>. Set <b>Contract start</b> to <b>1 Nov 2026</b>.'],
             'Under the date: <b>Ends 31 Oct 2029</b>. Clear it and it reads <b>Starts on signature · runs 36 months</b>. Set it back.'),
            ('DATE-02', 'A new line runs the full term',
             ['Search <code>CYB-CON-ISO27001-001</code> and click <b>Add</b>.'],
             'Period shows <b>From 1 for 36 mo</b>. Term value <b>£3,300</b> (£1,100 × 3).'),
            ('DATE-03', 'Start later in the contract',
             ['Set <b>From</b> to <b>4</b> and click away.'],
             '<b>for</b> becomes <b>33</b> by itself (it still runs to the end). Term value <b>£3,025</b>. <b>Annual recurring stays £1,100</b>. A new <b>Year 1 recurring</b> row shows <b>£825</b> (9 months).'),
            ('DATE-04', 'End before the contract does',
             ['Set <b>for</b> to <b>12</b>.'],
             'Term value <b>£1,100</b>. <b>Renewal ARR £0</b> appears, because the line doesn\'t run in the last month so it won\'t renew. Set <b>for</b> back to <b>33</b>.'),
            ('DATE-05', 'Past the contract end is blocked',
             ['Set <b>for</b> to <b>40</b>.'],
             'The row turns red with <b>Past contract end</b>. The quote shows as blocked and <b>Sync &amp; Confirm</b> is disabled. Set it back to <b>33</b>: it clears.'),
            ('DATE-06', 'Package components follow their parent',
             ['(Optional) Add <code>SOC-CORE-1.5TB-OPS</code> and set its <b>From</b> to <b>4</b>.'],
             'Every component shows <b>Months 4–36 · follows package</b> and can\'t be changed on its own. Remove the package afterwards.'),
            ('DATE-07', 'Sync writes the dates to the Opportunity',
             ['Save, then <b>Sync &amp; Confirm</b>. Open the Opportunity.'],
             '<b>Contract Start Date 01/11/2026</b>, <b>Contract End Date 31/10/2029</b>, Amount <b>£3,025</b>. Quote Summary shows <b>Quote Renewal ARR £1,100</b>. The Opportunity Product shows Start Month 4, Months 33, Date 01/02/2027, Line End 31/10/2029.'),
            ('DATE-08', 'The order form shows the periods',
             ['Back in the desk, click <b>Generate PDF</b>.'],
             'Agreement: <b>Service start 1 November 2026</b>, initial term 36 months <b>to 31 October 2029</b>. Under the line: <b>1 February 2027 – 31 October 2029 (33 months)</b>. Schedule rows are dated (<b>Year 1 · Nov 2026 – Oct 2027: £825.00</b>), and the totals say <b>Recurring over 36 months</b>.'),
            ('DATE-09', 'Periods can\'t be changed outside the desk',
             ['(Admin) Try to change a quote line\'s <b>Months</b> outside the desk, e.g. in Salesforce\'s own line editor if it shows the field, or with Data Loader.'],
             'Refused: "Change a line\'s start month or months in the Pricing Desk".'),
        ],
    },
    {
        'id': 'QOL', 'title': 'Everyday speed-ups', 'who': 'Sales reps',
        'note': 'Use a fresh <code>[PRICING TEST]</code> or demo opportunity. Hard-refresh first (Cmd/Ctrl+Shift+R).',
        'cases': [
            ('QOL-01', 'One-click New Quote',
             ['On an Opportunity, open the header ▾ menu and click <b>New Quote</b>.'],
             'The desk opens with a new quote started. Name is "<i>Account</i> – <i>term</i>m v<i>n</i>", term and contract start come from the Opportunity, and expiry is filled in.'),
            ('QOL-02', 'Enter adds, the package folds',
             ['Type <code>SOC-CORE-1.5TB-OPS</code> and press <b>Enter</b>.'],
             'The package arrives as <b>one row</b> with "▸ 9 included". Clicking it shows the 9 components, and clicking again hides them. The name now includes the product. Choices sit above the lines.'),
            ('QOL-03', 'Pinned bar and unsaved marker',
             ['Scroll to the top of the page.'],
             'Save / Generate PDF / Sync, plus TCV · ARR · status, stay visible at the bottom, with an amber <b>Unsaved changes</b> dot.'),
            ('QOL-04', 'Line note on the order form',
             ['Click <b>Add note</b> under the package, type a note, click away. Save, then Generate PDF.'],
             'The note shows under the line in the desk and prints under that line on the PDF.'),
            ('QOL-05', 'Readiness and one message',
             ['After saving, look above Commercial Terms.'],
             '"Before you generate the order form" lists e.g. <b>No primary contact</b> and <b>No PO number</b>, each with a Fix link. The "Quote saved." message appears once, in the bar only.'),
            ('QOL-06', 'Fast save',
             ['Change a discount and Save.'],
             'Done in about a second.'),
            ('QOL-07', 'Fresh Opportunity',
             ['Sync &amp; Confirm, then <b>Back to Opportunity</b>.'],
             'Products and Quotes show the right counts straight away. No refresh needed.'),
            ('QOL-08', 'Out of step warning',
             ['(Admin) Add a product to the Opportunity by hand. Open its Pricing Desk tab.'],
             'An amber "Out of step with the quote" warning appears. <b>Re-sync from quote</b> asks first, then puts the quote\'s products back.'),
            ('QOL-09', 'Quote page and My Open Quotes',
             ['Open the Quote record, then Quotes → <b>My Open Quotes</b>.'],
             'The Quote page shows its Opportunity and Account and lists Quote PDFs first, with no New Contact / Opportunity / Lead buttons. The list view shows your Draft, Ready and Blocked quotes.'),
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
             'They show as <b style="color:#c2410c">orange placeholders</b>. This is expected until DXR Cyber supplies the details.'),
            ('DOC-04', 'Multi-service-line deal',
             [f'Open <a href="{opp("B")}" target="_blank" rel="noopener">[DEMO] Kestrel &amp; Vane</a> → its Quote → <b>Quote PDFs</b> → open the PDF.'],
             'Two service lines give <b>two delivery sections</b>. The £3,600 one-off sits in <b>year 1</b> of the payment schedule.'),
            ('DOC-05', 'Unapproved quotes can\'t produce a document',
             ['On Northshire, open the <b>Same scope at 45%</b> quote in the desk.'],
             'It shows <b>Needs manager approval</b> and <b>Generate PDF</b> is disabled.'),
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

# Round 2 worked examples: two fictional deals run end to end on 21 Oct (kept, not cleaned up)
PANDADOC = 'https://app.pandadoc.com/a/#/documents/'
E2E = [
    ('[E2E DEMO 2] Harbourline Logistics - Web App Pen Test',
     'The full round 2 path: scope sent to the customer and verified, 45% pen-test discount approved, send approved, signed. Amount synced, contract 21 Oct 2026 to 20 Oct 2027, Close Won Task',
     [('Opportunity', rec('Opportunity', '006Pu00000bp8sfIAA')), ('Quote', rec('Quote', '0Q0Pu000008MosnKAC')),
      ('Scoping Document', rec('Scoping_Document__c', 'a0hPu00000AOfvcIAD')), ('PandaDoc', PANDADOC + 'AS7WpbrSHVN6yixppoMZ94')]),
    ('[E2E DEMO] Northwind Analytics - Web App Pen Test',
     'The first run, before round 2\'s fixes: scope completed by the rep, approvals, signed. Useful as a before and after',
     [('Opportunity', rec('Opportunity', '006Pu00000boo1nIAA')), ('Quote', rec('Quote', '0Q0Pu000008MkpBKAS')),
      ('Scoping Document', rec('Scoping_Document__c', 'a0hPu00000AOZOgIAP')), ('PandaDoc', PANDADOC + '2g4nzDKTSYfuUKjftAxLuX')]),
]

KNOWN_GAPS = [
    ('Product costs: 583 of 727 active products have no cost yet', 'DXR Cyber (Lisa Washer), via the cost template', 'GP checks only apply to fully costed quotes. Until then, quotes with an uncosted line show "GP n/a" and fall back to the rule "over 40% discount needs approval". Every flow can be tested now'),
    ('Who is in the test group: reps, their managers (approvers), technical verifiers', 'Tej / DXR Cyber', "SaaScend sets each tester's Manager, the managers' PandaDoc seat flag and the scoping permission sets before testing starts"),
    ('PandaDoc production API key (the sandbox uses a sandbox key)', 'DXR Cyber', 'Sandbox sends go silently to a SaaScend inbox; customer signatures are simulated'),
    ('Contracting entity, company/VAT numbers, terms URL', 'DXR Cyber (Dan / finance)', 'Order forms print DRAFT with orange placeholders until supplied'),
    ('One-off invoicing trigger (on acceptance vs on completion)', 'Sarah / finance', 'The order form says "on acceptance"'),
    ('Delivery module wording (27 modules)', 'Each delivery team', 'SaaScend drafts, no SLA numbers. Edited in Setup, no deploy'),
    ('Catalogue v2 open questions: maturity multiplier, USD FX rate, 14 unpriced products, SOC-PRO-UCD, SOC-QBR price, "Annual Rate" label on monthly lines', 'Lisa Washer', 'Affects some prices and labels, not the mechanics'),
    ('Brand font Sailec (Figtree is the stand-in)', 'DXR Cyber marketing', 'Cosmetic'),
    ('Close Won still runs separately through the work package (it emails Projects and Finance)', 'By design', "Not part of this round's script"),
    ('Production plan: enabling Quotes can\'t be undone', 'Tej + DXR Cyber', 'Needs a dated cut-over and sign-off'),
]

SIGNOFF = ['Sales (rep) tester', 'Sales manager (approver)', 'Technical verifier (scoping)', 'Catalogue manager', 'Deal desk / finance', 'DXR Cyber sponsor', 'SaaScend (build lead)']

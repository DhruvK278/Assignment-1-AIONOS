import json

sources = [
    # Transcript
    {"id": "transcript-1", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:00:00", "from": "Arjun", "to": ["Neha", "Raghav", "Divya"], "text": "Let's keep this quick. Neha, where are we on the Q3 campaign deck?"},
    {"id": "transcript-2", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:01:00", "from": "Neha", "to": ["Arjun"], "text": "Draft is 80% done. I'll send it to Arjun for review by Wednesday."},
    {"id": "transcript-3", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:02:00", "from": "Arjun", "to": ["Raghav"], "text": "Good. Also, remind me — I told Raghav I'd send him the updated vendor list. I'll get that to him by end of day tomorrow."},
    {"id": "transcript-4", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:03:00", "from": "Raghav", "to": ["Arjun", "Divya", "Neha"], "text": "Appreciated. Separately, the Mumbai office renewal paperwork needs someone to sign off this week. Not sure whose desk that's on right now."},
    {"id": "transcript-5", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:04:00", "from": "Divya", "to": ["Raghav", "Arjun", "Neha"], "text": "I think that's supposed to be Facilities, but I haven't seen anyone pick it up."},
    {"id": "transcript-6", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:05:00", "from": "Arjun", "to": ["Divya"], "text": "Okay, flag it, don't assume. Divya, can you also pull the July expense variance report before Thursday's board prep?"},
    {"id": "transcript-7", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:06:00", "from": "Divya", "to": ["Arjun"], "text": "Yes, I'll have it ready Wednesday evening."},
    {"id": "transcript-8", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:07:00", "from": "Arjun", "to": ["Neha", "Raghav", "Divya"], "text": "One more thing — client call with Meridian Logistics got pushed. I need to reconfirm the new time with their team myself."},
    {"id": "transcript-9", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:08:00", "from": "Neha", "to": ["Arjun"], "text": "Also, just a reminder, the campaign deck review — I said Wednesday, but realistically Thursday morning is safer."},
    {"id": "transcript-10", "type": "transcript", "thread": "Leadership Sync", "timestamp": "2026-09-21T09:09:00", "from": "Arjun", "to": ["Neha"], "text": "Noted. Let's close here."},

    # Thread 1: Vendor List
    {"id": "email-vendor-1", "type": "email", "thread": "Vendor List", "timestamp": "2026-09-21T09:50:00", "from": "Raghav", "to": ["Arjun"], "text": "Following up from the sync — can you send the updated vendor list today?"},
    {"id": "email-vendor-2", "type": "email", "thread": "Vendor List", "timestamp": "2026-09-21T17:40:00", "from": "Arjun", "to": ["Raghav"], "text": "Running behind, will send first thing tomorrow morning instead."},
    {"id": "email-vendor-3", "type": "email", "thread": "Vendor List", "timestamp": "2026-09-22T09:15:00", "from": "Raghav", "to": ["Arjun"], "text": "No worries, whenever you get a chance today works."},
    {"id": "email-vendor-4", "type": "email", "thread": "Vendor List", "timestamp": "2026-09-22T18:30:00", "from": "Arjun", "to": ["Raghav"], "text": "Sorry, got pulled into board prep — will send by tomorrow (Wednesday) morning for sure."},
    {"id": "email-vendor-5", "type": "email", "thread": "Vendor List", "timestamp": "2026-09-23T08:45:00", "from": "Raghav", "to": ["Arjun"], "text": "Just checking — still good for this morning?"},

    # Thread 2: Q3 Campaign Deck
    {"id": "email-deck-1", "type": "email", "thread": "Q3 Campaign Deck", "timestamp": "2026-09-21T11:00:00", "from": "Neha", "to": ["Arjun"], "text": "Deck's coming together, still targeting Wednesday for your review."},
    {"id": "email-deck-2", "type": "email", "thread": "Q3 Campaign Deck", "timestamp": "2026-09-22T16:15:00", "from": "Neha", "to": ["Arjun"], "text": "Heads up — shifting the review to Thursday morning instead of Wednesday, need one more day on the data slides."},
    {"id": "email-deck-3", "type": "email", "thread": "Q3 Campaign Deck", "timestamp": "2026-09-23T10:00:00", "from": "Arjun", "to": ["Neha"], "text": "Understood, Thursday morning works. What time exactly?"},
    {"id": "email-deck-4", "type": "email", "thread": "Q3 Campaign Deck", "timestamp": "2026-09-23T10:20:00", "from": "Neha", "to": ["Arjun"], "text": "Let's say 9:30 AM Thursday, before your board prep block."},
    {"id": "email-deck-5", "type": "email", "thread": "Q3 Campaign Deck", "timestamp": "2026-09-24T08:00:00", "from": "Neha", "to": ["Arjun"], "text": "Deck is ready, attaching the draft ahead of our 9:30 review."},

    # Thread 3: Call Reschedule
    {"id": "email-call-1", "type": "email", "thread": "Call Reschedule", "timestamp": "2026-09-21T13:00:00", "from": "Priya", "to": ["Arjun"], "text": "Our scheduled call this week got bumped from our side — can you propose a new time? We're flexible Tuesday–Thursday afternoons."},
    {"id": "email-call-2", "type": "email", "thread": "Call Reschedule", "timestamp": "2026-09-22T15:00:00", "from": "Arjun", "to": ["Priya"], "text": "Apologies for the delay — how about Wednesday 3:00 PM?"},
    {"id": "email-call-3", "type": "email", "thread": "Call Reschedule", "timestamp": "2026-09-22T17:45:00", "from": "Priya", "to": ["Arjun"], "text": "Wednesday 3 PM works on our end, confirmed."},
    {"id": "email-call-4", "type": "email", "thread": "Call Reschedule", "timestamp": "2026-09-23T13:30:00", "from": "Priya", "to": ["Arjun"], "text": "Quick check — still on for 3 PM today?"},
    {"id": "email-call-5", "type": "email", "thread": "Call Reschedule", "timestamp": "2026-09-23T14:00:00", "from": "Arjun", "to": ["Priya"], "text": "Yes, confirmed, see you at 3."},

    # Thread 4: Expense Variance Report
    {"id": "email-expense-1", "type": "email", "thread": "Expense Variance Report", "timestamp": "2026-09-21T14:30:00", "from": "Divya", "to": ["Arjun"], "text": "Starting on the July variance numbers, targeting Thursday morning for board prep as discussed."},
    {"id": "email-expense-2", "type": "email", "thread": "Expense Variance Report", "timestamp": "2026-09-22T09:00:00", "from": "Arjun", "to": ["Divya"], "text": "Actually, can I get it by Wednesday evening instead? Want time to review before Thursday."},
    {"id": "email-expense-3", "type": "email", "thread": "Expense Variance Report", "timestamp": "2026-09-22T09:40:00", "from": "Divya", "to": ["Arjun"], "text": "Wednesday evening is tight but doable, I'll prioritize it."},
    {"id": "email-expense-4", "type": "email", "thread": "Expense Variance Report", "timestamp": "2026-09-23T18:00:00", "from": "Divya", "to": ["Arjun"], "text": "Report attached, sent as promised."},
    {"id": "email-expense-5", "type": "email", "thread": "Expense Variance Report", "timestamp": "2026-09-23T18:10:00", "from": "Arjun", "to": ["Divya"], "text": "Got it, thank you — exactly what I needed before tomorrow."},

    # Thread 5: Mumbai Office Lease Renewal
    {"id": "email-lease-1", "type": "email", "thread": "Mumbai Office Lease Renewal", "timestamp": "2026-09-21T10:15:00", "from": "Facilities", "to": ["All Staff"], "text": "Reminder: the Mumbai office lease renewal requires an authorized signature by Friday, 25 September."},
    {"id": "email-lease-2", "type": "email", "thread": "Mumbai Office Lease Renewal", "timestamp": "2026-09-22T11:00:00", "from": "Raghav", "to": ["Arjun", "Divya"], "text": "Following up from the sync — has anyone confirmed who's signing off on the Mumbai renewal? Don't think it's been assigned."},
    {"id": "email-lease-3", "type": "email", "thread": "Mumbai Office Lease Renewal", "timestamp": "2026-09-23T09:30:00", "from": "Divya", "to": ["Raghav", "Arjun"], "text": "Not on my end — I believe this typically sits with Facilities directly, not us."},
    {"id": "email-lease-4", "type": "email", "thread": "Mumbai Office Lease Renewal", "timestamp": "2026-09-24T16:00:00", "from": "Facilities", "to": ["All Staff"], "text": "Second reminder: signature is still pending. Deadline is Friday, 25 September, end of day."},
    {"id": "email-lease-5", "type": "email", "thread": "Mumbai Office Lease Renewal", "timestamp": "2026-09-24T16:45:00", "from": "Raghav", "to": ["Arjun"], "text": "This is now one day out and still unowned — can you confirm who's handling it?"},

    # Voice Notes
    {"id": "voice-1", "type": "voice_note", "thread": None, "timestamp": "2026-09-21T18:40:00", "from": "Arjun", "to": ["Arjun"], "text": "Quick note to self — need to get Raghav that vendor list, I think I said today but it might slip to tomorrow morning, remind me. Also still haven't heard back on the Mumbai lease thing, someone needs to own that, I don't think it's me."},
    {"id": "voice-2", "type": "voice_note", "thread": None, "timestamp": "2026-09-23T08:15:00", "from": "Arjun", "to": ["Arjun"], "text": "Reminder — expense variance report from Divya needs to be in my hands by Wednesday evening, not Thursday, I want time to go through it before board prep. Also Meridian call — I owe Priya a time, need to lock that in today."}
]

with open("sources.json", "w") as f:
    json.dump(sources, f, indent=2)

print("sources.json created successfully.")

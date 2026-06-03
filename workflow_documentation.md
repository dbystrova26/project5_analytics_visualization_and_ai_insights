# n8n workflow documentation — Cancellation retention workflow

**Workflow name:** Aparthotel cancellation risk → retention offer  
**Purpose:** Automatically identify high-risk bookings and send a personalised retention message before the guest cancels  
**Trigger:** New booking created in PMS (Property Management System)

---

## What this workflow does

When a new booking is created, n8n evaluates whether it is high-risk for cancellation. If it is, an LLM generates a personalised retention message and sends it via email or SMS. Every action is logged to a Google Sheet for audit and transparency.

**Business value:** If the chain processes 500 bookings/week and 30% are high-risk, this workflow handles 150 personalised retention messages per week automatically — work that would otherwise require 1–2 FTE.

---

## Workflow nodes (6 total)

### Node 1 — Webhook trigger
**Type:** n8n Webhook node  
**Purpose:** Receives a POST request from the PMS whenever a new booking is confirmed  
**Configuration:**
- Method: POST
- Path: `/new-booking`
- Authentication: Header auth (Bearer token from PMS)

**Expected payload:**
```json
{
  "booking_id": "BK-20240315-4821",
  "guest_name": "Maria Schmidt",
  "guest_email": "m.schmidt@email.com",
  "guest_phone": "+49123456789",
  "property": "Berlin Mitte Apt 12",
  "check_in": "2024-03-17",
  "check_out": "2024-03-20",
  "lead_time_days": 2,
  "booking_channel": "Booking.com",
  "adr": 145.00,
  "deposit_paid": false
}
```

---

### Node 2 — Filter: high-risk booking?
**Type:** n8n IF node  
**Purpose:** Decides whether to trigger the retention workflow  
**Logic:** Booking is flagged as high-risk if ANY of these conditions are true:
- `lead_time_days` < 3 (last-minute booking)
- `booking_channel` is "Booking.com" OR "Expedia" (OTA bookings cancel at 2.3x the rate)
- `deposit_paid` is false AND `lead_time_days` < 7

**If TRUE:** Proceed to AI message generation  
**If FALSE:** End workflow (no action needed)

---

### Node 3 — AI node: generate personalised message
**Type:** n8n OpenAI or Anthropic node  
**Model:** claude-sonnet-4-20250514 or gpt-4o  
**Purpose:** Generate a personalised, friendly retention message

**Prompt template:**
```
You are a guest relations assistant for {{property_name}}, a premium aparthotel.

Write a short, warm message to {{guest_name}} who has booked:
- Check-in: {{check_in}}
- Property: {{property}}
- Stay length: {{nights}} nights

The message should:
1. Welcome them and confirm their booking
2. Offer ONE small incentive to keep the booking non-refundable:
   - If stay is 1 night: offer free late check-out (until 2pm)
   - If stay is 2-3 nights: offer a €15 food & drink credit
   - If stay is 4+ nights: offer a 10% discount on the next direct booking
3. Include a direct booking link: https://aparthotel.com/book?ref=retention
4. Be under 120 words

Do NOT invent any facts. Use only the information provided above.
```

**Important:** Guest name, property address, check-in date, and incentive value are all injected from PMS data — the LLM only writes the connective prose, preventing hallucination of factual details.

---

### Node 4 — Send email / SMS
**Type:** n8n SendGrid node (email) or Twilio node (SMS)  
**Purpose:** Deliver the AI-generated message to the guest  
**Configuration:**
- SendGrid: use guest_email from webhook payload
- Twilio: use guest_phone from webhook payload (if provided)
- Subject line: `Your stay at {{property}} — a little something from us`

**Fallback:** If both email and phone are missing, write to Google Sheet with status "contact_missing" for manual follow-up.

---

### Node 5 — Log to Google Sheet
**Type:** n8n Google Sheets node  
**Purpose:** Audit trail — every message sent is recorded  
**Sheet columns:**
- Timestamp
- booking_id
- guest_name (anonymised to first name only)
- property
- channel
- lead_time_days
- message_sent (full text)
- send_status (delivered / failed)
- incentive_offered

**Why this matters for Chleo:** This log is the transparency layer. Every AI action is recorded, reviewable, and auditable. Chleo can open the Google Sheet at any time and see exactly what the AI sent and to whom.

---

### Node 6 — End (no action path)
**Type:** n8n No-op / End node  
**Purpose:** Clean exit for bookings that do not meet the high-risk criteria  
**No message is sent, no log entry is created.**

---

## How to set up this workflow in n8n

1. Sign up at [n8n.io](https://n8n.io) (free cloud tier available)
2. Create a new workflow
3. Add a Webhook node — copy the generated URL
4. Add it to your PMS notification settings (or use the workflow.json import below)
5. Configure credentials:
   - OpenAI or Anthropic API key (for Node 3)
   - SendGrid API key (for Node 4)
   - Google account OAuth (for Node 5)
6. Import `workflow.json` and update credentials

---

## Exporting this workflow

After building in n8n, export via: **Three dots menu → Download → workflow.json**  
The exported JSON is saved as `workflow.json` in this folder.

---

## Limitations & future improvements

- Currently rule-based (IF lead_time < 3 days). A future version would call the ML cancellation model API instead of using hard-coded thresholds.
- The incentive logic is static — a more sophisticated version would select incentives based on predicted lifetime value of the guest.
- No A/B testing built in yet — adding a random split node would let you test which message variant performs better.

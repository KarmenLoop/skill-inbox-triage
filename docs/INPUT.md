# Input and output

Supply a UTF-8 JSON object (maximum 10 MiB). Duplicate JSON keys and non-finite JSON constants are rejected. Arrays are required unless documented as optional. IDs must be stable and unique. Dates use ISO 8601; timestamps require an explicit UTC offset.

| Field | Contract |
| --- | --- |
| now | Offset-aware timestamp. |
| sla_hours | Positive number. |
| vip_senders | Array of exact sender addresses; case-insensitive. |
| messages | Objects: id, sender, received_at, status (open/waiting/closed), needs_reply boolean, optional subject. |

## Example

```json
{
  "now": "2026-10-19T12:00:00+00:00",
  "sla_hours": 24,
  "vip_senders": [
    "partner@example.com"
  ],
  "messages": [
    {
      "id": "m1",
      "sender": "partner@example.com",
      "received_at": "2026-10-19T10:00:00Z",
      "status": "open",
      "needs_reply": true
    },
    {
      "id": "m2",
      "sender": "reader@example.com",
      "received_at": "2026-10-17T10:00:00Z",
      "status": "open",
      "needs_reply": true
    }
  ]
}
```

## Result

queues with reply_now, reply_later, review, waiting, closed. Items include age_hours, due_at, and reason.

See [the complete sample result](../examples/expected.json). Exit 0 means processing completed, not that all reported findings passed.

## Errors and side effects

The helper makes no network requests and executes no submitted commands. It reads the input and explicitly documented local paths. It writes only a requested new output file; stdout is the default. Invalid input exits 2. Existing output is preserved. An output write failure can leave a partial new file; remove that file before retrying. Installation is a separate explicit action.

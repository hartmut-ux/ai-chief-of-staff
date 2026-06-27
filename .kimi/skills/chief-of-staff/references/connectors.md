# Source Connectors

Each source subagent connects to a tool or API, fetches recent data, normalizes it, and writes a JSON cache file under `memory/source-cache/<source>.json`.

## Source JSON schema

Every cache file must use this top-level shape:

| Field       | Type     | Required | Description                                                        |
|-------------|----------|----------|--------------------------------------------------------------------|
| `source`    | string   | yes      | Source identifier: `email`, `calendar`, `tasks`, `web`, `custom`   |
| `fetched_at`| string   | yes      | ISO 8601 timestamp of when the fetch completed                     |
| `items`     | array    | yes      | Normalized items (see per-item schema below)                       |
| `errors`    | array    | no       | Non-fatal errors encountered while fetching/normalizing            |
| `metadata`  | object   | no       | Source-specific context (account, query, window, cursor, etc.)     |

### Item schema

Each object in `items` must contain:

| Field            | Type    | Required | Description                                                    |
|------------------|---------|----------|----------------------------------------------------------------|
| `id`             | string  | yes      | Stable source-specific identifier                              |
| `title`          | string  | yes      | Short human-readable headline                                  |
| `summary`        | string  | yes      | One to three sentence description                              |
| `priority`       | integer | yes      | 1 (low) to 5 (critical)                                        |
| `category`       | string  | yes      | One of: `inbox`, `calendar`, `task`, `news`, `custom`          |
| `action_required`| boolean | yes      | Whether the user needs to do something with this item          |
| `proposed_action`| string  | no       | Suggested next step if `action_required` is true               |
| `link`           | string  | no       | Deep link to email, event, task, article, etc.                 |

Optional useful fields:

- `sender` / `organizer` / `creator` (string)
- `participants` (array of strings)
- `start_at` / `end_at` / `due_at` (ISO 8601 strings)
- `labels` / `tags` (array of strings)
- `thread_id` / `project_id` (string)

---

## Email

**Connector:** Gmail MCP, Outlook MCP, or an IMAP/API script.

**Raw data shape:** Message list from the email API, including headers (`From`, `To`, `Subject`, `Date`), snippet/body, labels, and thread ID.

**Normalized schema (`memory/source-cache/email.json`):**

```json
{
  "source": "email",
  "fetched_at": "2026-06-27T08:00:00+02:00",
  "items": [
    {
      "id": "msg_1793a",
      "title": "Board deck feedback needed",
      "summary": "CFO shared the Q3 board deck and asked for comments by 14:00 today.",
      "priority": 5,
      "category": "inbox",
      "action_required": true,
      "proposed_action": "Review deck and reply with comments by 13:30.",
      "link": "https://mail.google.com/mail/u/0/#inbox/msg_1793a",
      "sender": "cfo@company.com",
      "received_at": "2026-06-27T07:15:00+02:00",
      "labels": ["INBOX", "IMPORTANT"]
    }
  ],
  "errors": [],
  "metadata": { "account": "work", "window": "since=yesterday" }
}
```

---

## Calendar

**Connector:** Google Calendar MCP, Outlook Calendar MCP, or CalDAV/API script.

**Raw data shape:** Event list with summary, start/end times, attendees, location, description, and organizer.

**Normalized schema (`memory/source-cache/calendar.json`):**

```json
{
  "source": "calendar",
  "fetched_at": "2026-06-27T08:00:00+02:00",
  "items": [
    {
      "id": "evt_4b82",
      "title": "Product sync",
      "summary": "Weekly product stand-up with engineering and design.",
      "priority": 4,
      "category": "calendar",
      "action_required": true,
      "proposed_action": "Prepare 2-min update on AI roadmap blockers.",
      "link": "https://calendar.google.com/calendar/event?eid=evt_4b82",
      "start_at": "2026-06-27T10:30:00+02:00",
      "end_at": "2026-06-27T11:00:00+02:00",
      "organizer": "pm@company.com",
      "participants": ["eng@company.com", "design@company.com"],
      "location": "Zoom"
    }
  ],
  "errors": [],
  "metadata": { "calendar": "primary", "window": "today" }
}
```

---

## Tasks

**Connector:** Notion MCP, Todoist MCP, Asana API, ClickUp API, or a local task file.

**Raw data shape:** Task objects with title, status, due date, project/section, assignee, and labels.

**Normalized schema (`memory/source-cache/tasks.json`):**

```json
{
  "source": "tasks",
  "fetched_at": "2026-06-27T08:00:00+02:00",
  "items": [
    {
      "id": "task_991c",
      "title": "Finalize vendor contract",
      "summary": "Legal review completed; awaiting final signature before EOD.",
      "priority": 5,
      "category": "task",
      "action_required": true,
      "proposed_action": "Send contract to vendor for signature and set reminder for 16:00.",
      "link": "https://notion.so/task_991c",
      "due_at": "2026-06-27T17:00:00+02:00",
      "status": "In review",
      "project": "Procurement",
      "tags": ["legal", "vendor"]
    }
  ],
  "errors": [],
  "metadata": { "tool": "notion", "filter": "open & due<=today+2" }
}
```

---

## Web

**Connector:** Kimi `SearchWeb` / `FetchURL`, or a custom RSS/news scraping script.

**Raw data shape:** Search results, article metadata, or RSS feed entries (title, URL, snippet/published date, source).

**Normalized schema (`memory/source-cache/web.json`):**

```json
{
  "source": "web",
  "fetched_at": "2026-06-27T08:00:00+02:00",
  "items": [
    {
      "id": "web_a1f7",
      "title": "EU AI Act compliance deadlines moved to 2027",
      "summary": "Regulators announced a phased enforcement timeline for high-risk AI systems.",
      "priority": 3,
      "category": "news",
      "action_required": false,
      "proposed_action": "Flag for legal review if we ship high-risk AI features.",
      "link": "https://example.com/eu-ai-act-2027",
      "published_at": "2026-06-26T18:00:00+02:00",
      "source_name": "TechPolicy Daily",
      "tags": ["regulation", "ai"]
    }
  ],
  "errors": [],
  "metadata": { "queries": ["EU AI Act", "AI agent regulation"], "window": "24h" }
}
```

---

## Custom

**Connector:** Any user-provided API script, MCP, webhook, or database query.

**Raw data shape:** Source-defined; document it in `memory/preferences.md` under `custom_sources`.

**Normalized schema (`memory/source-cache/custom.json`):**

```json
{
  "source": "custom",
  "fetched_at": "2026-06-27T08:00:00+02:00",
  "items": [
    {
      "id": "cust_220e",
      "title": "GitHub security alert: dependabot critical",
      "summary": "Repository `company/api` has a critical dependency vulnerability.",
      "priority": 5,
      "category": "custom",
      "action_required": true,
      "proposed_action": "Review dependabot PR #442 and merge or escalate.",
      "link": "https://github.com/company/api/security/dependabot/42",
      "source_name": "GitHub Security",
      "tags": ["security", "dependabot"]
    }
  ],
  "errors": [],
  "metadata": { "connector": "github_security.py", "repos": ["company/api"] }
}
```

---

## Error reporting

If a fetch or normalization error occurs, still write the cache file with an empty `items` array and an `errors` entry:

```json
{
  "source": "email",
  "fetched_at": "2026-06-27T08:00:00+02:00",
  "items": [],
  "errors": [
    { "code": "AUTH_FAILURE", "message": "Gmail MCP token expired", "recoverable": true }
  ],
  "metadata": { "account": "work" }
}
```

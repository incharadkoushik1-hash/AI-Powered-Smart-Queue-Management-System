# API Documentation

## AI-Based Queue Monitoring System

---

## Base URL

```
http://localhost:5000
```

For network access, replace `localhost` with the server's IP address.

---

## Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard HTML page |
| `/api/stats` | GET | Current queue statistics |
| `/api/stats/history` | GET | Historical count data |
| `/api/frame` | GET | Latest raw video frame |
| `/api/frame/annotated` | GET | Frame with detection overlay |
| `/api/health` | GET | System health check |
| `/api/config` | GET | Current configuration |
| `/api/reset` | POST | Reset statistics |

---

## GET /

Returns the main dashboard HTML page.

**Response:** HTML page (text/html)

---

## GET /api/stats

Returns current queue statistics and staffing recommendation.

**Response:**
```json
{
    "current_count": 5,
    "peak_count": 12,
    "average_count": 4.2,
    "wait_time_minutes": 1.5,
    "status": "NORMAL",
    "trend": "STABLE",
    "max_threshold": 10,
    "min_threshold": 3,
    "total_people": 142,
    "timestamp": "2026-04-12T19:30:00.000Z",
    "recommendation": {
        "current_staff": 2,
        "recommended_staff": 2,
        "staff_needed": 0,
        "action": "MAINTAIN",
        "message": "Current staffing (2) is adequate for 5 people in queue.",
        "queue_level": "MODERATE"
    }
}
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| current_count | int | Number of people currently in queue |
| peak_count | int | Highest queue count since start/reset |
| average_count | float | Average count over history |
| wait_time_minutes | float | Estimated wait time in minutes |
| status | string | CRITICAL/HIGH/NORMAL/LOW |
| trend | string | INCREASING/DECREASING/STABLE |
| max_threshold | int | Threshold for HIGH status |
| min_threshold | int | Threshold for LOW status |
| total_people | int | Cumulative people counted |
| timestamp | string | ISO 8601 timestamp |
| recommendation | object | Staffing recommendation |

---

## GET /api/stats/history

Returns historical queue count data.

**Response:**
```json
{
    "history": [
        {
            "count": 5,
            "timestamp": "2026-04-12T19:29:58.000Z"
        },
        {
            "count": 6,
            "timestamp": "2026-04-12T19:29:56.000Z"
        }
    ]
}
```

---

## GET /api/frame

Returns the latest raw video frame as JPEG image.

**Response:**
- Content-Type: `image/jpeg`
- Binary image data

**Note:** Returns 204 No Content if no frame available.

---

## GET /api/frame/annotated

Returns the latest video frame with detection bounding boxes and ROI overlay.

**Response:**
- Content-Type: `image/jpeg`
- Binary image data

**Features in annotated frame:**
- Green rectangles: Detected persons
- Blue polygon: ROI (Region of Interest)
- Count label: Current queue count

---

## GET /api/health

Returns system health status for monitoring.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2026-04-12T19:30:00.000Z",
    "camera_connected": true
}
```

---

## GET /api/config

Returns current system configuration.

**Response:**
```json
{
    "max_threshold": 10,
    "min_threshold": 3,
    "roi_points": [
        [200, 150],
        [1080, 150],
        [1080, 570],
        [200, 570]
    ],
    "avg_service_time": 120
}
```

---

## POST /api/reset

Resets all statistics (peak count, total people, history).

**Response:**
```json
{
    "status": "success",
    "message": "Statistics reset"
}
```

**Error Response (500):**
```json
{
    "status": "error",
    "message": "Analyzer not available"
}
```

---

## Status Values

| Status | Description | Threshold |
|--------|-------------|-----------|
| CRITICAL | Queue is too long, immediate action needed | >= max_threshold |
| HIGH | Queue is above acceptable level | >= 70% of max_threshold |
| NORMAL | Queue is within acceptable range | >= min_threshold and < 70% max |
| LOW | Queue is short, minimal wait | < min_threshold |

---

## Recommendation Actions

| Action | Description |
|--------|-------------|
| ADD_STAFF | More staff needed for current queue |
| MAINTAIN | Current staffing is adequate |
| REDUCE | Queue is light, can reduce staff |

---

## Queue Levels

| Level | Count Range |
|-------|------------|
| EMPTY | 0 |
| LIGHT | 1-3 |
| MODERATE | 4-7 |
| HEAVY | 8-12 |
| OVERLOADED | 13+ |

---

## Error Responses

All endpoints may return these error codes:

| Code | Description |
|------|-------------|
| 204 | No Content (frame not available) |
| 500 | Internal Server Error |

---

## Example Usage

### JavaScript (Fetch API)
```javascript
async function getQueueStats() {
    const response = await fetch('/api/stats');
    const data = await response.json();
    console.log(`Queue: ${data.current_count}`);
}
```

### Python (requests)
```python
import requests

response = requests.get('http://localhost:5000/api/stats')
data = response.json()
print(f"Queue count: {data['current_count']}")
```

### cURL
```bash
curl http://localhost:5000/api/stats
```

# RCCG Mount Zion NL - Landing Page API Contract

Scope: featured Bible verse, hero images, welcome section, and homepage event cover. Full event administration remains in Django Admin.

## Common conventions

- Base prefix: `/api/`
- Reads are public; writes are authenticated/admin-only.
- JSON for text-only requests; `multipart/form-data` whenever a `File` is included.
- Date-only values use `YYYY-MM-DD`.
- Backend mutation responses are canonical and are written directly into the frontend cache.

### Standard success envelope

```json
{
  "success": true,
  "data": {},
  "status_code": 200
}
```

### Standard error envelope

```json
{
  "success": false,
  "data": null,
  "errors": { "field_or_server": ["Human-readable error message"] },
  "status_code": 400
}
```

## Hero Bible verse

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/api/hero/bible-verse/` | Public | Get hero bible verse |
| POST| `/api/hero/bible-verse/` | Admin | Create hero if None |
| PATCH | `/api/hero/bible-verse/` | Admin | Update hero bible verse |

```ts
interface FeaturedBibleVerse {
  reference: string;
  text: string;
}
```

PATCH JSON request and response `data` use the same shape. Frontend limits: reference 100 chars, text 300 chars.

## Hero images

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/api/hero/images/` | Public | Get ordered image list (sort based on order)|
--
| POST | `/api/hero/images/` | Admin | Upload one image immediately |
| DELETE | `/api/hero/images/{id}/` | Admin | Delete one image immediately |
---
| PATCH | `/api/hero/images/order/` | Admin | Save ordering |

```ts
interface HeroImage {
  id: number;
  url: string;
  alt_text: string;
  order: number;
}
```

POST uses multipart: `image: File`, `alt_text?: string`. DELETE returns `{ "id": <deleted_id> }`. Order request:

```json
{ "image_ids": [4, 9, 2] }
```

Order response returns the complete canonical `HeroImage[]`. Maximum 10 images; maximum 1.5 MB each; JPEG/PNG/WebP/AVIF. Upload/delete persist immediately; reorder persists only when Save order is pressed.

## Welcome section

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/api/home-page/welcome/` | Public | Get welcome text and image |
| PATCH | `/api/home-page/welcome/` | Admin | Update text and optionally image |

```ts
interface WelcomeContent {
  text: string;
  image: { url: string; alt_text: string };
}
```

PATCH multipart request: `text: string`, `image?: File`. If image is omitted, keep the existing image. Response returns complete `WelcomeContent`. Frontend limits: 600 characters, image max 1.5 MB, JPEG/PNG/WebP/AVIF.

## Homepage event cover

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/api/events/?pagination` | Public | Get events |
| GET | `/api/events/upcoming` | Public | Get earliest upcoming event |
| POST | `/api/events/` | Admin | Create an event |
| PATCH | `/api/events/{id}/` | Admin | Edit the current event |

```ts
interface UpcomingEvent {
  id: number;
  title: string;
  description: string;
  start_date: string; // YYYY-MM-DD
  cover_image: { url: string; alt_text: string };
  external_url: string;
}
```

GET sorts by `start_date` ascending and returns only events with `start_date >= today`. With `limit=1`, `data` is an array of zero or one event. Empty array is valid and means no upcoming event.

POST multipart: `title`, `description`, `start_date`, `cover_image: File`.

PATCH multipart: `title`, `description`, `start_date`, `cover_image?: File`. If no new image is supplied, retain the existing cover. Response returns the complete updated event.

Frontend limits: title 120 chars, description 1000 chars, cover max 1.5 MB, JPEG/PNG/WebP/AVIF. Backend should reject past start dates.

## Latest sermon

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/api/sermon/?pagination` | Public | Get sermons |
| GET | `/api/sermon/{id}` | Get a single sermon |
| PATCH | `/api/sermon/{id}/` | Admin | Edit the current sermon |

```ts
interface Sermon {
  id: number;
  title: string;
  description: string;
  date: string; // YYYY-MM-DD
  cover_image: { url: string; alt_text: string };
  preacher: string;
  tags: string;
  external_url: string;
}
```

## Hero About

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/api/about/` | Public | Get About sections |
| POST | `/api/about/` | Admin | Create an About section with its image |
| PATCH | `/api/about/{id}/` | Admin | Update About text and optionally replace its image |

Create and update requests use `multipart/form-data`. Send the image in the same request as the other fields:

```text
title: About us
description: ...
image: <File>
image_alt_text: About us
mission: ...
vision: ...
```

`image` is required when creating an About section and optional when updating one. If it is omitted during an update, the existing image is retained. The response returns the complete canonical About object, including the generated `image_url`.

```ts
interface About {
  title: string;
  description: string;
  image: { url: string; alt_text: string };
  mission: string;
  vision: string;
}
```

## Hero Gallery
patch:

```ts
interface HeroGallery{
    image1: {url: string, alt_text: string}
    image2: {url: string, alt_text: string}
    image3: {url: string, alt_text: string}
    image4: {url: string, alt_text: string}
}
```


## Out of scope

- Event deletion from live edit mode
- Managing multiple events from the landing page
- Event schedules/times/locations/galleries/additional images/status workflows
- Full event CRUD/dashboard behavior; Django Admin handles these operations

## Backend checklist

- Keep response envelope consistent.
- Return canonical objects after successful writes.
- Enforce limits and validation server-side.
- Protect all write endpoints with admin/auth permissions.
- Use multipart only where files are accepted.
- Preserve these response shapes so frontend mocks can be swapped without component rewrites.

# Steganopy

## INSTALLATION

### Requirements

- Python >= 3.7
- Node.js >= 10.0.0
- Yarn
- Pipenv
- [Now CLI](https://www.npmjs.com/package/now)

### Instructions

```bash
$ yarn install # install Node.js deps
$ pipenv install # install Python deps
$ now dev # start in local development env
$ now # deploy to production env
```

## DOCUMENTATION

### Routes

#### 1. `/api`

> Just for testing.

##### Response body

- `iam`: "/api"

#### 2. POST `/api/conceal`

> Embed data into an image.

##### Request body (multipart/form-data)

- `files` (array): Array of 2 files: the former is the cover image, and the later is the payload data.

##### Response body (application/json)

- `url` (string): Public URL of the output image.

#### 3. POST `/api/reveal`

> Extract data from an image.

##### Request body (multipart/form-data)

- `files` (array): Array of 1 file: the image containing embeded data.

##### Response body (application/octet-stream)

The payload data as a binary file.

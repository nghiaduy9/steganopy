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

##### Response body (application/json)

- `iam`: "/api"

#### 2. POST `/api/conceal`

> Embed data into an image.

##### Request body (multipart/form-data)

- `files` (array): Array of 2 files: the former is the cover image, and the later is the payload data.

##### Response body (application/json)

- `url` (string | `undefined`): If the operation successes, this contains the URL of the output image. `undefined` otherwise.
- `error` (string | `undefined`): If the operation successes, this is `undefined`. Otherwise, it can be either "BAD_INPUT" or "PAYLOAD_TOO_LARGE".

#### 3. `/api/conceal/testing`

> Testing route for route #2.

##### Response body (application/json)

- `url` (string): URL of a sample image.

#### 4. POST `/api/reveal`

> Extract secret data from an image.

##### Request body (multipart/form-data)

- `files` (array): Array of 1 file: the image containing embeded data.

##### Response body (application/octet-stream | application/json)

If the operation successes, the response body contains the secret data as application/octet-stream. Otherwise, it is application/json with:

- `error` (string): Either "BAD_INPUT" or "PAYLOAD_NOT_EXISTS".

#### 5. `/api/reveal/testing`

> Testing route for route #4.

##### Response body (application/octet-stream)

A sample .zip file as the secret data.

#### 6. POST `/api/detect`

> Check if this image cannot contain any secret data.

##### Request body (multipart/form-data)

- `files` (array): Array of 1 file: the image containing embeded data.

##### Response body (application/json)

- `result` (boolean): `false` if this image cannot contain any secret data, `true` if it MAY contain.
- `error` (string | `undefined`): If the operation successes, this is `undefined`. Otherwise, it can be "BAD_INPUT".

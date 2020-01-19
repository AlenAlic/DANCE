# API Module

The API module abstracts interaction with API's.
It removes the complexities of networking and presents only a set of functions that return promises for API results.
Network errors and API error responses are generalized by rejected promises.

Additionally, the API modules **should** be documented with jsdoc comments to enable code-completion and (if your ide supports it) some type checking on invokes.

## Layout

Path | Purpose
--- | ---
`auth.js` | Abstraction for authentication and account management (activation, password reset, etc)
`backend.js` | Abstracts file fetching from the backend server that the app is hosted on.
`frontend.js` | Abstracts file fetching from the frontend server that the app is hosted on.
`util/` | Api logic that is not an abstraction
`util/interceptors.js` | Adds request and response interceptors to server instances. This is decoupled from the singleton instance creation so that it can import code that also uses the server instances (indirectly) to avoid circular dependencies.
`util/network-errors.js` | Functions for deducing network errors and generate generic error messages for network errors.
`util/servers.js` | Exposes singleton instances to all API hosts/servers
`util/token-storage.js` | Exposes functions to save and load API tokens



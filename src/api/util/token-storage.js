import { backendServer, frontendServer } from "./servers";

// Prefix for token storage
const TOKEN_PREFIX = "dance";

// This module manages api tokens for servers and backends

/**
 * @typedef {string} EncodedJwtToken
 */

/**
 * Gets the key under which to store a token for a given server
 * @param {AxiosInstance} server
 * @returns {string}
 * @throws Error - Thrown if the server is not a known instance
 */
function getStorageKey(server) {
  switch (server) {
    case backendServer:
      return `${TOKEN_PREFIX}.token.backend`;
    case frontendServer:
      return `${TOKEN_PREFIX}.token.frontend`;
    default: {
      const error = new Error("Unknown server");
      error.server = server;
      throw error;
    }
  }
}

/**
 * Gets the active token to be used for authentication against a given server
 * @param {AxiosInstance} server
 * @returns {?EncodedJwtToken}
 * @throws Error - Thrown if the server is not a known instance
 */
export function loadServerToken(server) {
  const key = getStorageKey(server);
  return localStorage.getItem(key);
}

/**
 * Sets the active token to be used for authentication against a given server
 * @param {AxiosInstance} server
 * @param {?EncodedJwtToken} token - The token to set for authentication, if null the saved token is removed.
 * @throws Error - Thrown if the server is not a known instance
 */
export function saveServerToken(server, token) {
  const key = getStorageKey(server);
  if (token) {
    localStorage.setItem(key, token);
  } else {
    localStorage.removeItem(key);
  }
}

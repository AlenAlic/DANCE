import decode from "jwt-decode";
import { backendServer } from "./util/servers";

/**
 * @typedef {Object} AuthenticatedUser
 * @property {number} id
 * @property {string} email
 * @property {string} username
 * @property {Date} expiresAt
 * @property {Date} issuedAt
 * @property {EncodedJwtToken} token
 */

export class AuthenticatedUser {
  /** @member {EncodedJwtToken} */
  token;
  /** @member {number} */
  id;
  /** @member {string} */
  email;
  /** @member {string} */
  username;
  /** @member {string} */
  tag;
  /** @member {number} */
  access;
  /** @member {Date} */
  expiresAt;
  /** @member {Date} */
  issuedAt;

  /**
   * @param {EncodedJwtToken} token
   */
  constructor(token) {
    this.token = token;
    const data = decode(token);
    this.id = data.id;
    this.email = data.email;
    this.access = data.access;
    this.username = data.username;
    this.tag = data.tag;
    // Assumption: exp and iat fields are number of milliseconds since 1970
    this.expiresAt = new Date(data.exp * 1000);
    this.issuedAt = new Date(data.iat * 1000);
  }

  /**
   * Indicates if the authenticated user instance is valid; requirements are:
   * - expiration moment is in the future
   * - issue moment before expiration moment
   * @returns {boolean}
   */
  get isValid() {
    return this.expiresAt > new Date() && this.expiresAt > this.issuedAt;
  }
}

export const authApi = {
  /**
   * Starts a new authenticated user session
   * @param {string} email - The email of the user that identifies them.
   * @param {string} password - The password to login with.
   * @param {boolean} remember_me - Toggle if the user should be remembered (longer lasting token)
   * @returns {Promise<void>}
   */
  async login(email, password, remember_me = false) {
    return await backendServer.post(`/auth/login`, {
      email: email,
      password: password,
      remember_me: remember_me
    });
  },
  /**
   * Ends the active user session
   * The interceptors are expected to inject the session token of the session that will be ended.
   * @returns {Promise<void>}
   */
  async logout() {
    await backendServer.delete(`/auth/logout`);
  },
  /**
   * Renews the authenticated user session, returns an updated token
   * @returns {Promise<AuthenticatedUser>}
   */
  async renew() {
    return await backendServer.get(`auth/renew`);
  }
};

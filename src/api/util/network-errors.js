import i18n from "@/languages";

/**
 * @typedef {number} NetworkErrorCode
 */

/**
 * Enum for network errors
 * @readonly
 */
export const ERROR_CODES = {
  NONE: -1,
  UNKNOWN: 0,
  SERVER_CORS: 1,
  NETWORK: 2,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  PAYLOAD_TOO_LARGE: 413,
  SERVER_ERROR: 500,
  SERVER_OFFLINE: 503,
  SERVER_TIMEOUT: 504
};

const HTTP_STATUS_MAPPING = {
  [400]: ERROR_CODES.BAD_REQUEST,
  [401]: ERROR_CODES.UNAUTHORIZED,
  [403]: ERROR_CODES.FORBIDDEN,
  [404]: ERROR_CODES.NOT_FOUND,
  [413]: ERROR_CODES.PAYLOAD_TOO_LARGE,
  [500]: ERROR_CODES.SERVER_ERROR,
  [503]: ERROR_CODES.SERVER_OFFLINE,
  [504]: ERROR_CODES.SERVER_TIMEOUT
};

/**
 * Returns true if Error is an AxiosError
 * @param {Error} error
 * @see {AxiosError}
 * @returns {boolean}
 */
function isAxiosError(error) {
  return error && error.hasOwnProperty("response");
}

/**
 * Returns true if Error is a result of a CORS error during the request
 * @param {AxiosError} error
 * @returns {boolean}
 */
function isNetworkError(error) {
  return error.response === undefined;
}

/**
 * Gets the NetworkErrorCode associated with a given error.
 * Returns ERROR_CODES.UNKNOWN if the error instance is not an AxiosError.
 * @param {Error | AxiosError} error
 * @returns {NetworkErrorCode}
 */
export function getNetworkErrorCode(error) {
  if (isAxiosError(error)) {
    /** @type {AxiosError} error */
    if (isNetworkError(error)) {
      return ERROR_CODES.NETWORK;
    } else {
      const status = error.response.status;
      return HTTP_STATUS_MAPPING[status] || ERROR_CODES.NETWORK;
    }
  } else {
    return ERROR_CODES.UNKNOWN;
  }
}

/**
 * Gets a generic error message for a network error code
 * @param {NetworkErrorCode} code
 * @returns {string | null}
 */
export function localizeNetworkErrorCode(code) {
  if (!code) {
    return null;
  }
  switch (code) {
    case ERROR_CODES.NONE:
      return null;
    case ERROR_CODES.NETWORK:
      return i18n.t("network-errors.network");
    case ERROR_CODES.SERVER_CORS:
      return i18n.t("network-errors.server-cors");
    case ERROR_CODES.BAD_REQUEST:
      return i18n.t("network-errors.bad-request");
    case ERROR_CODES.UNAUTHORIZED:
      return i18n.t("network-errors.credentials");
    case ERROR_CODES.FORBIDDEN:
      return i18n.t("network-errors.forbidden");
    case ERROR_CODES.NOT_FOUND:
      return i18n.t("network-errors.not-found");
    case ERROR_CODES.PAYLOAD_TOO_LARGE:
      return i18n.t("network-errors.payload-too-large");
    case ERROR_CODES.SERVER_ERROR:
      return i18n.t("network-errors.server-error");
    case ERROR_CODES.SERVER_OFFLINE:
      return i18n.t("network-errors.server-offline");
    case ERROR_CODES.SERVER_TIMEOUT:
      return i18n.t("network-errors.server-timeout");
    default:
      return i18n.t("network-errors.unknown");
  }
}

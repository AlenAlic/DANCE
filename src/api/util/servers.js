import axios from "axios/index";

/**
 * The axios instance which can be used to communicate with the backend.
 * @type {AxiosInstance}
 */
export const backendServer = axios.create();
backendServer.defaults.withCredentials = true;
backendServer.defaults.headers.common["Content-Type"] = "application/json";

/**
 * The axios instance which can be used to communicate with the frontend that hosts the app.
 * @type {AxiosInstance}
 */
export const frontendServer = axios.create();
frontendServer.defaults.baseURL = "/";
frontendServer.defaults.headers.common["Content-Type"] = "application/json";

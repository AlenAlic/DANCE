import { AuthenticatedUser, authApi } from "@/api/auth";
import { loadServerToken, saveServerToken } from "@/api/util/token-storage";
import { backendServer } from "@/api/util/servers";
import { TOURNAMENT_OFFICE_MANAGER, FLOOR_MANAGER, ADJUDICATOR, PRESENTER } from "@/constants";

const SET_USER = "AUTH: Set user";

const LOGIN = "LOGIN";
const LOGIN_REQUEST = "LOGIN: Login request sent.";
const LOGIN_SUCCESS = "LOGIN: Successful request.";
const LOGIN_ERROR = "LOGIN: Failed request.";

const LOGOUT = "LOGOUT";
const LOGOUT_REQUEST = "LOGOUT: Logout request sent.";
const LOGOUT_SUCCESS = "LOGOUT: Successful request.";
const LOGOUT_ERROR = "LOGOUT: Failed request.";

const RENEW = "RENEW";
const RENEW_REQUEST = "RENEW: Renew token request sent.";
const RENEW_SUCCESS = "RENEW: Successful request.";
const RENEW_ERROR = "RENEW: Failed request.";

export { LOGIN, LOGOUT, RENEW, SET_USER };

const getUser = () => {
  const token = loadServerToken(backendServer);
  const user = token ? new AuthenticatedUser(token) : null;
  return !!user && user.isValid ? user : null;
};

const setUser = token => {
  saveServerToken(backendServer, token);
  const user = token ? new AuthenticatedUser(token) : null;
  return !!user && user.isValid ? user : null;
};

export default {
  state: {
    user: getUser(),
    access: -1,
    loading: false
  },

  mutations: {
    [SET_USER](state, token) {
      let user = setUser(token);
      state.user = user;
      if (user) {
        state.access = user.access;
      }
    },

    [LOGIN_REQUEST](state) {
      state.loading = true;
    },
    [LOGIN_SUCCESS](state) {
      state.loading = false;
    },
    [LOGIN_ERROR](state) {
      state.loading = false;
    },

    [LOGOUT_REQUEST](state) {
      state.loading = true;
    },
    [LOGOUT_SUCCESS](state) {
      state.user = null;
      state.access = -1;
      state.loading = false;
    },
    [LOGOUT_ERROR](state) {
      state.loading = false;
    },

    [RENEW_REQUEST](state) {
      state.loading = true;
    },
    [RENEW_SUCCESS](state) {
      state.loading = false;
    },
    [RENEW_ERROR](state) {
      state.loading = false;
    }
  },
  actions: {
    // Sign a user in
    [LOGIN]({ commit }, { email, password, remember_me }) {
      commit(LOGIN_REQUEST);
      return authApi
        .login(email, password, remember_me)
        .then(response => {
          commit(SET_USER, response.data);
          commit(LOGIN_SUCCESS);
        })
        .catch(error => {
          commit(LOGIN_ERROR);
          throw error;
        });
    },
    // Set user
    [SET_USER]: ({ commit }, { token }) => {
      commit(SET_USER, token);
    },
    // Sign a user out
    [LOGOUT]: ({ commit }) => {
      commit(LOGOUT_REQUEST);
      return authApi
        .logout()
        .then(() => {
          commit(SET_USER, null);
          commit(LOGOUT_SUCCESS);
        })
        .catch(error => {
          commit(LOGOUT_ERROR);
          throw error;
        });
    },
    // Renew user token
    [RENEW]({ commit }) {
      commit(RENEW_REQUEST);
      return authApi
        .renew()
        .then(response => {
          commit(SET_USER, response.data);
          commit(RENEW_SUCCESS);
        })
        .catch(() => {
          commit(SET_USER, null);
          commit(RENEW_ERROR);
        });
    }
  },
  getters: {
    currentUser: state => {
      return state.user;
    },
    access: state => {
      return state.user ? state.user.access : -1;
    },
    isTournamentOfficeManager: state => {
      return state.user && state.user.access === TOURNAMENT_OFFICE_MANAGER;
    },
    isFloorManager: state => {
      return state.user && state.user.access === FLOOR_MANAGER;
    },
    isAdjudicator: state => {
      return state.user && state.user.access === ADJUDICATOR;
    },
    isPresenter: state => {
      return state.user && state.user.access === PRESENTER;
    }
  }
};

import store from "@/store";
import { LOGIN, LOGOUT, RENEW } from "@/store/modules/auth";

const AuthHandler = {
  install(Vue) {
    Vue.prototype.$auth = {
      /**
       * Get the currently signed in user.
       */
      get currentUser() {
        return store.getters.currentUser;
      },

      /**
       * Get the currently signed in user's access level.
       */
      get access() {
        return store.getters.access;
      },

      /**
       * Checks if the current user is authenticated
       */
      get isAuthenticated() {
        return !!this.currentUser;
      },

      /**
       * Checks if the current user is a tournament office manager
       */
      get isTournamentOfficeManager() {
        return store.getters.isTournamentOfficeManager;
      },
      /**
       * Checks if the current user is a floor manager
       */
      get isFloorManager() {
        return store.getters.isFloorManager;
      },
      /**
       * Checks if the current user is an adjudicator
       */
      get isAdjudicator() {
        return store.getters.isAdjudicator;
      },
      /**
       * Checks if the current user is a presenter
       */
      get isPresenter() {
        return store.getters.isPresenter;
      },

      /**
       * Sign in a user with a username and password.
       * @param email
       * @param password
       * @param remember_me
       * @returns {Promise}
       */
      signInWithUsernameAndPassword(email, password, remember_me) {
        return store.dispatch(LOGIN, { email, password, remember_me });
      },

      /**
       * Renew a user's session
       * @returns {Promise}
       */
      renew() {
        return store.dispatch(RENEW);
      },

      /**
       * Sign out the currently signed in user.
       * @returns {Promise}
       */
      signOut() {
        return store.dispatch(LOGOUT);
      }
    };
  }
};

export default AuthHandler;

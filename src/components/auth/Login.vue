<template>
  <v-card max-width="400">
    <v-form ref="form" v-model="valid" @submit.prevent="login">
      <v-card-title>{{ $t("auth.log_in") }}</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="username"
          :rules="usernameRules"
          :label="$t('auth.username')"
          required
          validate-on-blur
        ></v-text-field>
        <v-text-field
          v-model="password"
          :rules="passwordRules"
          :label="$t('auth.password')"
          required
          type="password"
        ></v-text-field>
        <v-checkbox v-model="rememberMe" :label="$t('auth.remember_me')" required></v-checkbox>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
          {{ $t("auth.log_in") }}
        </v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
import { ERROR_CODES, getNetworkErrorCode } from "@/api/util/network-errors";
import i18n from "@/languages";
import loadStore from "@/store/loader";
export default {
  data: function() {
    return {
      valid: false,
      username: "",
      usernameRules: [this.$form.fieldRequired],
      password: "",
      passwordRules: [this.$form.passwordRequired],
      rememberMe: false,
      errors: null,
      loading: false
    };
  },
  methods: {
    login: function() {
      this.error = null;
      this.loading = true;
      this.$auth
        .signInWithUsernameAndPassword(this.username, this.password, this.rememberMe)
        .then(() => {
          loadStore();
          this.$router.push({
            name: "dashboard"
          });
        })
        .catch(error => {
          const status = getNetworkErrorCode(error);
          if (status === ERROR_CODES.UNAUTHORIZED)
            this.$notify.error(i18n.t("auth.errors.invalid_login"));
          else if (status === ERROR_CODES.FORBIDDEN)
            this.$notify.error(i18n.t("auth.errors.inactive_account"));
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

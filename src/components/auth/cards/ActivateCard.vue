<template>
  <div class="mx-auto">
    <v-card max-width="400">
      <v-card-title>{{ $t("auth.activate.title") }}</v-card-title>
      <transition name="fade" mode="out-in">
        <div v-if="verifying">
          <v-card-text class="text-center">
            <div class="mb-3">{{ $t("auth.activate.verifying_token") }}</div>
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </v-card-text>
        </div>
        <div v-else-if="error">
          <v-card-text>
            {{ $t("auth.activate.verification_error") }}
          </v-card-text>
          <v-card-actions>
            <router-link tag="span" :to="{ name: 'home' }">
              <v-btn text color="primary">
                {{ $t("navigation.back_to_home_page") }}
              </v-btn>
            </router-link>
          </v-card-actions>
        </div>
        <div v-else>
          <v-form ref="form" lazy-validation @submit.prevent="activate">
            <v-card-text>
              {{ $t("auth.activate.set_password") }}
              <v-text-field
                v-model="password"
                :label="$t('auth.password')"
                required
                type="password"
              ></v-text-field>
              <v-text-field
                v-model="repeatPassword"
                :label="$t('auth.repeat_password')"
                required
                type="password"
              ></v-text-field>
              <password-requirements
                :password="password"
                :repeat_password="repeatPassword"
                @requirements="passwordRequirements"
              />
              <v-card-actions>
                <v-btn :disabled="!valid" :loading="loading" color="primary" text @click="activate">
                  {{ $t("auth.activate.activate") }}
                </v-btn>
              </v-card-actions>
            </v-card-text>
          </v-form>
        </div>
      </transition>
    </v-card>
  </div>
</template>

<script>
import { authApi } from "@/api/auth";
import { ERROR_CODES, getNetworkErrorCode } from "@/api/util/network-errors";
import i18n from "@/languages";
import PasswordRequirements from "@/components/auth/PasswordRequirements";
export default {
  name: "ActivateCard",
  components: { PasswordRequirements },
  data: function() {
    return {
      newPasswordSet: false,
      valid: false,
      password: "",
      repeatPassword: "",
      error: false,
      verifying: true,
      loading: false
    };
  },
  mounted: function() {
    this.$nextTick(function() {
      this.verifyActivationToken();
    });
  },
  methods: {
    verifyActivationToken: function() {
      authApi
        .verifyActivationToken(this.$route.params.token)
        .then(() => {
          this.verifying = false;
        })
        .catch(error => {
          setTimeout(() => {
            const status = getNetworkErrorCode(error);
            if (status === ERROR_CODES.NOT_FOUND) {
              this.$notify.warning(i18n.t("auth.activate.unknown_code"));
              this.$router.push({
                name: "home"
              });
            } else {
              this.error = true;
              this.verifying = false;
            }
          }, 500);
        });
    },
    passwordRequirements: function(valid) {
      this.valid = valid;
    },
    activate: function() {
      this.loading = true;
      this.$auth
        .activate(this.$route.params.token, this.password, this.repeatPassword)
        .then(() => {
          this.$router.push({
            name: "login"
          });
        })
        .catch(error => {
          const status = getNetworkErrorCode(error);
          if (status === ERROR_CODES.BAD_REQUEST) this.$notify.error(i18n.t("auth.activate.error"));
          this.loading = false;
        });
    }
  }
};
</script>

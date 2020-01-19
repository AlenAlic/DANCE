<template>
  <div class="mx-auto">
    <v-card max-width="400">
      <transition name="fade" mode="out-in">
        <v-form ref="form" lazy-validation v-if="!newPasswordSet" @submit.prevent="changePassword">
          <v-card-title>{{ $t("auth.change_password") }}</v-card-title>
          <v-card-text>
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
              ref="req"
              :password="password"
              :repeat_password="repeatPassword"
              @requirements="passwordRequirements"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn
              :disabled="!valid"
              :loading="loading"
              color="primary"
              text
              @click="changePassword"
            >
              {{ $t("auth.reset_password") }}
            </v-btn>
            <router-link tag="span" :to="{ name: 'login' }">
              <v-btn text>
                {{ $t("general.cancel") }}
              </v-btn>
            </router-link>
          </v-card-actions>
        </v-form>
        <div v-else>
          <v-card-title>{{ $t("auth.new_password_set.title") }}</v-card-title>
          <v-card-text>{{ $t("auth.new_password_set.text") }}</v-card-text>
          <v-card-actions>
            <router-link tag="span" :to="{ name: 'login' }">
              <v-btn text color="primary">
                {{ $t("navigation.back_to_login_page") }}
              </v-btn>
            </router-link>
          </v-card-actions>
        </div>
      </transition>
    </v-card>
  </div>
</template>

<script>
import PasswordRequirements from "@/components/auth/PasswordRequirements";
import { ERROR_CODES, getNetworkErrorCode } from "@/api/util/network-errors";
import i18n from "@/languages";
export default {
  name: "PasswordResetCard",
  components: { PasswordRequirements },
  data: function() {
    return {
      newPasswordSet: false,
      valid: false,
      token: "",
      password: "",
      repeatPassword: "",
      error: null,
      loading: false
    };
  },
  methods: {
    passwordRequirements: function(valid) {
      this.valid = valid;
    },
    changePassword: function() {
      this.loading = true;
      this.$auth
        .resetPassword(this.$route.params.token, this.password, this.repeatPassword)
        .then(() => {
          this.newPasswordSet = true;
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

<template>
  <div class="mx-auto">
    <v-card max-width="400">
      <transition name="fade" mode="out-in">
        <v-form
          ref="form"
          v-model="valid"
          v-if="!newPasswordSent"
          @submit.prevent="requestPassword"
        >
          <v-card-title>{{ $t("auth.request_new_password") }}</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="email"
              :rules="emailRules"
              :label="$t('auth.email')"
              required
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn
              :disabled="!valid"
              :loading="loading"
              color="primary"
              text
              @click="requestPassword"
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
          <v-card-title>{{ $t("auth.password_reset_email_sent.title") }}</v-card-title>
          <v-card-text>{{ $t("auth.password_reset_email_sent.text") }}</v-card-text>
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
import { authApi } from "@/api/auth";
export default {
  name: "PasswordForgottenCard",
  data: function() {
    return {
      newPasswordSent: false,
      valid: false,
      email: "",
      emailRules: [v => this.$util.isEmail(v) || this.$t("auth.errors.valid_email")],
      error: null,
      loading: false
    };
  },
  methods: {
    requestPassword: function() {
      this.loading = true;
      authApi.resetPasswordRequest(this.email).then(() => {
        this.newPasswordSent = true;
      });
    }
  }
};
</script>

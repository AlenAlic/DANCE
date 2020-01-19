<template>
  <v-form ref="form" v-model="valid" @submit.prevent="switchAccount">
    <v-card>
      <v-card-title>
        {{ $t("tournament_office.dashboard.switch_user.title") }}
      </v-card-title>
      <v-card-text>
        <v-select
          v-model="user"
          :items="users"
          :label="$t('tournament_office.dashboard.switch_user.user.label')"
          :rules="[$form.fieldRequired]"
          :loading="loading"
          item-value="id"
          item-text="username"
          clearable
        ></v-select>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn :disabled="!valid" :loading="switching" color="primary" text type="submit">
          {{ $t("tournament_office.dashboard.switch_user.submit") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { SET_USER } from "@/store/modules/auth";
import loadStore from "@/store/loader";
export default {
  props: {
    users: { type: Array, default: () => [] }
  },
  data: function() {
    return {
      valid: false,
      loading: false,
      user: null,
      switching: false
    };
  },
  methods: {
    switchAccount() {
      this.loading = true;
      Vue.axios
        .post("event/dashboard", {
          user_id: this.user
        })
        .then(response => {
          store.dispatch(SET_USER, { token: response.data }).then(() => {
            loadStore();
            this.$router.push({
              name: "home"
            });
          });
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

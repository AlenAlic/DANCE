<template>
  <form ref="form" method="POST" :action="url" target="_blank">
    <input type="hidden" name="token" :value="token" />
    <v-card>
      <v-card-title>
        {{ $t("tournament_office.dashboard.database.title") }}
      </v-card-title>
      <v-card-text>
        {{ $t("tournament_office.dashboard.database.text") }}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn :loading="loading" color="primary" text type="button" @click="openDatabase">
          {{ $t("tournament_office.dashboard.database.submit") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </form>
</template>

<script>
export default {
  data: function() {
    return {
      loading: false,
      url: this.$config.api.url.replace("/api", "/remote_login"),
      token: null
    };
  },
  methods: {
    openDatabase() {
      this.loading = true;
      new Promise(resolve => {
        this.token = this.$store.state.auth.user.token;
        resolve();
      })
        .then(() => {
          this.$refs.form.submit();
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

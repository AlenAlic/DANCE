<template>
  <v-card>
    <v-card-title>
      {{ $t("event.dancers.csv.title") }}
    </v-card-title>
    <v-card-subtitle>
      {{ $t("event.dancers.csv.subtitle") }}
    </v-card-subtitle>
    <v-card-text>
      <v-textarea v-model="csv" auto-grow dense :label="$t('event.dancers.csv.label')" />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="primary" text @click="addDancers" :loading="loading">
        {{ $t("event.dancers.csv.submit") }}
      </v-btn>
      <v-btn text @click="csv = ''">
        {{ $t("general.cancel") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { SET_DANCERS } from "@/store/modules/dancers";
export default {
  data: function() {
    return {
      loading: false,
      csv: ""
    };
  },
  methods: {
    addDancers() {
      this.loading = true;
      Vue.axios
        .post("dancers/csv", {
          csv: this.csv
        })
        .then(response => {
          store.commit(SET_DANCERS, response.data.dancers);
          this.$notify.success(this.$t("event.dancers.csv.added", { count: response.data.added }));
          this.csv = "";
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

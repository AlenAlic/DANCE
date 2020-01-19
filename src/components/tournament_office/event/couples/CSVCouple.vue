<template>
  <v-card>
    <v-card-title>
      {{ $t("event.couples.csv.title") }}
    </v-card-title>
    <v-card-subtitle>
      {{ $t("event.couples.csv.subtitle") }}
    </v-card-subtitle>
    <v-card-text>
      {{ $t("event.couples.csv.text") }}
    </v-card-text>
    <v-card-text>
      <v-textarea v-model="csv" auto-grow dense :label="$t('event.couples.csv.label')" />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="primary" text @click="addDancers" :loading="loading">
        {{ $t("event.couples.csv.submit") }}
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
import { SET_COUPLES } from "@/store/modules/couples";
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
        .post("couples/csv", {
          csv: this.csv
        })
        .then(response => {
          store.commit(SET_COUPLES, response.data.couples);
          this.$notify.success(this.$t("event.couples.csv.added", { count: response.data.added }));
          this.csv = "";
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

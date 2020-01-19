<template>
  <v-card>
    <v-card-title>
      {{ $t("event.adjudicators.delete_adjudicator.title") }}
    </v-card-title>
    <v-card-text>
      {{ $t("event.adjudicators.delete_adjudicator.text", { name: adjudicator.name }) }}
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="error" text @click="deleteAdjudicator" :loading="loading">
        {{ $t("event.adjudicators.delete_adjudicator.submit") }}
      </v-btn>
      <v-btn text @click="close">
        {{ $t("general.cancel") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { SET_ADJUDICATORS } from "@/store/modules/adjudicators";
export default {
  props: {
    adjudicator: { type: Object, default: () => null }
  },
  data: function() {
    return {
      loading: false
    };
  },
  methods: {
    deleteAdjudicator() {
      this.loading = true;
      Vue.axios
        .delete(`adjudicators/${this.adjudicator.adjudicator_id}`)
        .then(response => {
          store.commit(SET_ADJUDICATORS, response.data);
          this.close();
        })
        .finally(() => {
          this.loading = false;
        });
    },
    close() {
      this.$emit("close");
    }
  }
};
</script>

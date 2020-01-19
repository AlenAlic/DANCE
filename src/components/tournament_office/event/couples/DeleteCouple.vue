<template>
  <v-card>
    <v-card-title>
      {{ $t("event.couples.delete_couple.title") }}
    </v-card-title>
    <v-card-text>
      {{
        $t("event.couples.delete_couple.text", {
          number: couple.number,
          lead: couple.lead.name,
          follow: couple.follow.name
        })
      }}
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="error" text @click="deleteCouple" :loading="loading">
        {{ $t("event.couples.delete_couple.submit") }}
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
import { DELETE_COUPLE } from "@/store/modules/couples";
export default {
  props: {
    couple: { type: Object, default: () => null }
  },
  data: function() {
    return {
      loading: false
    };
  },
  methods: {
    deleteCouple() {
      this.loading = true;
      Vue.axios
        .delete(`couples/${this.couple.couple_id}`)
        .then(response => {
          store.commit(DELETE_COUPLE, response.data);
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

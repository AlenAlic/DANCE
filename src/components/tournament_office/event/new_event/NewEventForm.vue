<template>
  <v-form ref="form" v-model="valid" @submit.prevent="createEvent">
    <v-card>
      <v-card-title>
        {{ $t("event.create_new_event.title") }}
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="name"
          prepend-icon="mdi-lead-pencil"
          :rules="[$form.fieldRequired]"
          :label="$t('event.create_new_event.name')"
          required
        ></v-text-field>
        <v-dialog ref="dialog" v-model="modal" :return-value.sync="date" persistent width="290px">
          <template v-slot:activator="{ on }">
            <v-text-field
              v-model="date"
              prepend-icon="mdi-calendar-today"
              readonly
              v-on="on"
              :label="$t('event.setup.default.date.label')"
              :rules="[$form.fieldRequired]"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="date"
            scrollable
            first-day-of-week="1"
            :min="$util.nowString.substring(0, 10)"
          >
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="modal = false">
              {{ $t("general.cancel") }}
            </v-btn>
            <v-btn text color="primary" @click="$refs.dialog.save(date)">
              {{ $t("general.ok") }}
            </v-btn>
          </v-date-picker>
        </v-dialog>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
          {{ $t("event.create_new_event.submit") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { EVENTS } from "@/store/modules/events";
export default {
  data: function() {
    return {
      valid: false,
      name: "",
      modal: false,
      date: "",
      loading: false
    };
  },
  methods: {
    createEvent() {
      this.loading = true;
      Vue.axios
        .post("event", { name: this.name, date: this.date })
        .then(() => {
          store.dispatch(EVENTS).then(() => {
            this.$router.push({ name: "tournament_office.event.setup" });
          });
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

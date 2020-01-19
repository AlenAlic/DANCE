<template>
  <v-form ref="form" v-model="valid" @submit.prevent="createCompetition">
    <v-card>
      <v-card-title>
        {{ $t("event.setup.competition.title") }}
      </v-card-title>
      <v-card-text>
        {{ $t("event.setup.competition.text") }}
      </v-card-text>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" xl="4">
            <v-select
              v-model="discipline"
              :items="$store.state.dependencies.disciplines"
              :label="$t('competition.discipline.label')"
              :no-data-text="$t('competition.discipline.no_data')"
              :rules="[$form.fieldRequired]"
              item-value="discipline_id"
              item-text="name"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" xl="4">
            <v-select
              v-model="dancing_class"
              :items="$store.state.dependencies.classes"
              :label="$t('competition.dancing_class.label')"
              :no-data-text="$t('competition.dancing_class.no_data')"
              :rules="[$form.fieldRequired]"
              item-value="dancing_class_id"
              item-text="name"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" xl="4">
            <v-select
              v-model="mode"
              :items="$store.state.config.config.competition_modes"
              :label="$t('competition.mode.label')"
              :hint="$t('competition.mode.hint')"
              persistent-hint
              :rules="[$form.fieldRequired]"
              item-text="name"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" xl="4">
            <v-select
              v-model="qualification"
              :items="$store.state.competitions.competitions"
              :label="$t('competition.qualification.label')"
              :hint="$t('competition.qualification.hint')"
              persistent-hint
              item-text="name"
              item-value="competition_id"
            ></v-select>
          </v-col>
          <v-col cols="4">
            <v-select
              v-model="floors"
              :items="[1, 2, 3]"
              :label="$t('competition.floors.label')"
              :hint="$t('competition.floors.hint')"
              persistent-hint
              :rules="[$form.fieldRequired]"
            ></v-select>
          </v-col>
          <v-col cols="8" xl="4">
            <v-datetime-picker
              v-model="date"
              :label="$t('competition.date.label')"
              :hint="$t('competition.date.hint')"
              persistent-hint
              :rules="[$form.fieldRequired]"
            />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
          {{ $t("event.setup.competition.submit") }}
        </v-btn>
        <v-btn text @click="$refs.form.reset()">
          {{ $t("general.cancel") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { SET_COMPETITIONS } from "@/store/modules/competitions";
import VDatetimePicker from "@/components/general/datetime_picker/VDatetimePicker";
export default {
  components: { VDatetimePicker },
  data: function() {
    return {
      valid: false,
      loading: false,
      discipline: null,
      dancing_class: null,
      floors: 1,
      date: "",
      mode: null,
      qualification: null
    };
  },
  methods: {
    createCompetition() {
      this.loading = true;
      Vue.axios
        .post("competition", {
          discipline: this.discipline,
          dancing_class: this.dancing_class,
          floors: this.floors,
          date: this.$util.dateTimeToUTCString(this.date),
          mode: this.mode,
          qualification: this.qualification
        })
        .then(response => {
          store.commit(SET_COMPETITIONS, response.data);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

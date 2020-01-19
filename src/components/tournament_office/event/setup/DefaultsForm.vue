<template>
  <v-form ref="form" v-model="valid" @submit.prevent="createDefaults">
    <v-card>
      <v-card-title>
        {{ $t("event.setup.default.title") }}
      </v-card-title>
      <v-card-text>
        <p>{{ $t("event.setup.default.text1") }}</p>
        <p>
          <b>{{ $t("event.setup.default.warning") }}</b> {{ $t("event.setup.default.text2") }}
        </p>
        <div>{{ $t("event.setup.default.label") }}</div>
        <v-row
          no-gutters
          v-if="[$constants.XTDS, $constants.ODK].includes($store.state.config.config.tournament)"
        >
          <v-checkbox
            v-for="competition in $store.state.config.config.competitions"
            :key="competition"
            class="mr-3 mt-0 mb-2"
            v-model="competitions"
            :label="competition"
            :value="competition"
            hide-details
          ></v-checkbox>
        </v-row>
        <div v-else-if="sond_competitions">
          <div v-for="disc in Object.keys(sond_competitions)" :key="disc">
            <div v-for="age in Object.keys(sond_competitions[disc])" :key="age">
              <span class="subtitle-2">{{ disc }} {{ age }}</span>
              <v-row no-gutters>
                <v-checkbox
                  v-for="competition in sond_competitions[disc][age]"
                  :key="competition.value"
                  class="mr-3 mt-0 mb-2"
                  v-model="competitions"
                  :label="competition.label"
                  :value="competition.value"
                  hide-details
                ></v-checkbox>
              </v-row>
            </div>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
          {{ $t("event.setup.default.submit") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { SET_ALL_DEPENDENCIES } from "@/store/modules/dependencies";
import { SET_COMPETITIONS } from "@/store/modules/competitions";
export default {
  data: function() {
    return {
      valid: false,
      loading: false,
      competitions: this.$store.state.config.config.competitions,
      modal: false
    };
  },
  computed: {
    sond_competitions() {
      if (this.$store.state.config.config.tournament === this.$constants.SOND) {
        const comps = this.$store.state.config.config.competitions;
        const STANDARD = this.$constants.STANDARD;
        const LATIN = this.$constants.LATIN;
        const JUNIOREN = this.$constants.JUNIOREN;
        const SENIOREN = this.$constants.SENIOREN;
        const ballroom_junioren = comps
          .filter(c => c.startsWith(STANDARD) && c.endsWith(JUNIOREN))
          .map(c => ({
            label: c.replace(`${STANDARD}&`, "").replace(` ${JUNIOREN}`, ""),
            value: c
          }));
        const ballroom_senioren = comps
          .filter(c => c.startsWith(STANDARD) && c.endsWith(SENIOREN))
          .map(c => ({
            label: c.replace(`${STANDARD}&`, "").replace(` ${SENIOREN}`, ""),
            value: c
          }));
        const latin_junioren = comps
          .filter(c => c.startsWith(LATIN) && c.endsWith(JUNIOREN))
          .map(c => ({
            label: c.replace(`${LATIN}&`, "").replace(` ${JUNIOREN}`, ""),
            value: c
          }));
        const latin_senioren = comps
          .filter(c => c.startsWith(LATIN) && c.endsWith(SENIOREN))
          .map(c => ({
            label: c.replace(`${LATIN}&`, "").replace(` ${SENIOREN}`, ""),
            value: c
          }));
        return {
          [STANDARD]: {
            [JUNIOREN]: ballroom_junioren,
            [SENIOREN]: ballroom_senioren
          },
          [LATIN]: {
            [JUNIOREN]: latin_junioren,
            [SENIOREN]: latin_senioren
          }
        };
      } else {
        return null;
      }
    }
  },
  methods: {
    createDefaults() {
      this.loading = true;
      Vue.axios
        .post("event/defaults", { competitions: this.competitions })
        .then(response => {
          store.commit(SET_ALL_DEPENDENCIES, response.data);
          store.commit(SET_COMPETITIONS, response.data.competitions);
          this.$refs.form.reset();
          this.competitions = this.$store.state.config.config.competitions;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

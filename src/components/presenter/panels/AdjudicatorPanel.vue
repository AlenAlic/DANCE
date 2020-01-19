<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <span>
        <span class="mr-2">
          {{ $t("presenter.panel.adjudicators") }}
        </span>
        <span v-if="adjudicators.length > 0">
          {{ `${adjudicators.filter(a => a.present).length}/${adjudicators.length}` }}
        </span>
        <v-icon class="mr-1" v-if="timer" small>mdi-refresh</v-icon>
        <v-progress-circular
          class="ml-2"
          indeterminate
          color="primary"
          size="12"
          width="3"
          v-if="loading"
        />
      </span>
    </v-expansion-panel-header>
    <v-expansion-panel-content v-if="round.floors.length <= 1">
      <div
        v-for="adj in adjudicators"
        :key="adj.adjudicator_id"
        :class="[adj.present ? 'success--text' : 'error--text']"
      >
        <span class="mr-4">{{ adj.name }}</span>
        <span class="mr-2" v-if="adj.present && adj.dance">{{ adj.dance }}</span>
      </div>
    </v-expansion-panel-content>
    <v-expansion-panel-content v-else>
      <table>
        <tbody>
          <template v-for="floor in round.floors">
            <tr :key="floor">
              <th class="text-left font-weight-black subtitle-2">
                {{ $t("round.reports.header.floor") }} {{ floor }}
              </th>
            </tr>
            <tr v-for="adj in adjudicatorsOnFloor(floor)" :key="`${adj.adjudicator_id}-${floor}`">
              <td :class="[adj.present ? 'success--text' : 'error--text']">
                <span class="mr-4">{{ adj.name }}</span>
                <span class="mr-2" v-if="adj.present && adj.dance">{{ adj.dance }}</span>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import Vue from "vue";
import { RELOAD_TIMER_SHORT } from "@/constants";
export default {
  props: {
    round: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      adjudicators: [],
      timer: null
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get(`round/${this.round.round_id}/presenter/adjudicators`)
        .then(response => {
          this.adjudicators = response.data;
          if (
            (this.adjudicators.filter(a => !a.present).length > 0 && this.round.is_active) ||
            this.round.type === this.$constants.GENERAL_LOOK
          ) {
            if (!this.timer) this.timer = setInterval(this.getData, RELOAD_TIMER_SHORT);
          } else {
            clearInterval(this.timer);
            this.timer = null;
          }
        })
        .catch(() => {
          clearInterval(this.timer);
          this.timer = null;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    adjudicatorsOnFloor(floor) {
      return this.adjudicators.filter(a => a.floor === floor);
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
  }
};
</script>

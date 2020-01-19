<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <span>
        <span>
          {{ $t("presenter.panel.couples_present") }}
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
    <v-expansion-panel-content>
      <table>
        <tbody>
          <template v-for="dance in dances">
            <tr :key="dance.dance_id">
              <td></td>
              <td>
                <b>{{ dance.name }}</b>
              </td>
            </tr>
            <template v-if="round.mode !== $constants.CHANGE_PER_DANCE">
              <template v-for="heat in Object.keys(data[dance.dance_id])">
                <tr :key="`${dance.dance_id}-${heat}`">
                  <td>
                    <b class="mr-5">{{ heat }}</b>
                  </td>
                  <td>
                    <span
                      class="number"
                      v-for="couple in data[dance.dance_id][heat]"
                      :key="couple.number"
                    >
                      <span :class="[couple.present ? 'success--text' : 'error--text']">
                        {{ couple.number }}
                      </span>
                    </span>
                  </td>
                </tr>
              </template>
            </template>
            <template v-else>
              <template v-for="heat in Object.keys(data[dance.dance_id])">
                <tr :key="`${dance.dance_id}-${heat}`">
                  <td>
                    <b class="mr-5">{{ heat }}</b>
                  </td>
                  <td>
                    <div
                      class="number partner"
                      v-for="dancer in data[dance.dance_id][heat]"
                      :key="dancer.number"
                    >
                      <span :class="[dancer.present ? 'success--text' : 'error--text']">
                        <b>{{ dancer.number }}:</b>
                        <span> {{ partnerMapping[dance.dance_id][dancer.number] }}</span>
                      </span>
                    </div>
                  </td>
                </tr>
              </template>
            </template>
          </template>
        </tbody>
      </table>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import Vue from "vue";
import { RELOAD_TIMER } from "@/constants";
export default {
  props: {
    round: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      data: {},
      partnerMapping: {},
      dances: [],
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
        .get(`round/${this.round.round_id}/presenter/couples_present`)
        .then(response => {
          this.data = response.data.heat_mapping;
          this.partnerMapping = response.data.partner_mapping;
          this.dances = response.data.dances;
          if (!this.timer && this.round.is_active) {
            this.timer = setInterval(this.getData, RELOAD_TIMER);
          } else if (
            !response.data.round.is_active &&
            this.round.type !== this.$constants.GENERAL_LOOK
          ) {
            clearInterval(this.timer);
            this.timer = null;
            this.$emit("updated", response.data.round);
          }
        })
        .catch(() => {
          clearInterval(this.timer);
          this.timer = null;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
  }
};
</script>

<style scoped lang="scss">
.number {
  display: inline-block;
  width: 2.5rem;
  text-align: left;

  &.partner {
    b {
      width: 2.5rem;
      display: inline-block;
      text-align: right;
    }
    width: 6rem;
  }
}
</style>

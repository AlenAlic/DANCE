<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <span>
        <span class="mr-3">
          {{ $t("presenter.panel.starting_list") }}
        </span>
        <v-progress-circular indeterminate color="primary" size="12" width="3" v-if="loading" />
      </span>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <table>
        <tbody v-if="round.mode !== $constants.CHANGE_PER_DANCE">
          <tr v-for="couple in shuffleArray(couples)" :key="couple.couple_id">
            <td class="text-right">
              <b class="mr-3">{{ couple.number }}</b>
            </td>
            <td>{{ couple.name }} ({{ couple.team }})</td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr>
            <td colspan="2">
              <b>{{ $t("presenter.leads") }}</b>
            </td>
          </tr>
          <tr v-for="dancer in shuffleArray(leads)" :key="dancer.dancer_id">
            <td class="text-right">
              <b class="mr-3">{{ dancer.number }}</b>
            </td>
            <td>{{ dancer.name }} ({{ dancer.team }})</td>
          </tr>
          <tr>
            <td colspan="2" class="pt-5">
              <b>{{ $t("presenter.follows") }}</b>
            </td>
          </tr>
          <tr v-for="dancer in shuffleArray(follows)" :key="dancer.dancer_id">
            <td class="text-right">
              <b class="mr-3">{{ dancer.number }}</b>
            </td>
            <td>{{ dancer.name }} ({{ dancer.team }})</td>
          </tr>
        </tbody>
      </table>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import Vue from "vue";
export default {
  props: {
    round: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      couples: [],
      leads: [],
      follows: []
    };
  },
  created() {
    this.getData();
  },
  computed: {
    shuffle() {
      return this.round && this.round.type === this.$constants.FINAL && !this.round.completed;
    }
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get(`round/${this.round.round_id}/presenter/starting_list`)
        .then(response => {
          if (this.round.mode === this.$constants.CHANGE_PER_DANCE) {
            this.leads = response.data.leads;
            this.follows = response.data.follows;
          } else {
            this.couples = response.data;
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
    shuffleArray(couples) {
      if (this.shuffle) {
        const original = [...couples];
        for (let i = original.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * i);
          const temp = original[i];
          original[i] = original[j];
          original[j] = temp;
        }
        return original;
      } else {
        return couples;
      }
    }
  }
};
</script>

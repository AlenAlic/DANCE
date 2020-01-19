<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <span>
        <span class="mr-3">
          {{ $t("presenter.panel.no_re_dance") }}
        </span>
        <v-progress-circular indeterminate color="primary" size="12" width="3" v-if="loading" />
      </span>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <table>
        <tbody v-if="round.mode !== $constants.CHANGE_PER_DANCE">
          <tr v-for="couple in couples" :key="couple.couple_id">
            <td class="text-right">
              <b class="mr-3">{{ couple.number }}</b>
            </td>
            <td>{{ couple.name }}</td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr>
            <td colspan="2">
              <b>{{ $t("presenter.leads") }}</b>
            </td>
          </tr>
          <tr v-for="dancer in leads" :key="dancer.dancer_id">
            <td class="text-right">
              <b class="mr-3">{{ dancer.number }}</b>
            </td>
            <td>{{ dancer.name }}</td>
          </tr>
          <tr>
            <td colspan="2" class="pt-5">
              <b>{{ $t("presenter.follows") }}</b>
            </td>
          </tr>
          <tr v-for="dancer in follows" :key="dancer.dancer_id">
            <td class="text-right">
              <b class="mr-3">{{ dancer.number }}</b>
            </td>
            <td>{{ dancer.name }}</td>
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
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get(`round/${this.round.round_id}/presenter/no_re_dance_couples`)
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
    }
  }
};
</script>

<template>
  <div class="table-ranking-wrapper">
    <table class="pt-1 table-ranking">
      <thead>
        <tr class="highlighted-col">
          <td rowspan="2" class="rank table-ranking--bottom">
            {{ $t("round.reports.ranking_report.rank") }}
          </td>
          <td rowspan="2" v-if="changePerDance" class="couple text-left">
            {{ $t("round.reports.ranking_report.dancer") }}<br />
            {{ $t("round.reports.ranking_report.team") }}
          </td>
          <td rowspan="2" v-else class="couple text-left">
            {{ $t("round.reports.ranking_report.couple") }}<br />
            {{ $t("round.reports.ranking_report.teams") }}
          </td>
          <td rowspan="2" class="number table-ranking--bottom">
            {{ $t("round.reports.ranking_report.number") }}
          </td>
          <td rowspan="2" class="round table-ranking--bottom">
            {{ $t("round.reports.ranking_report.round") }}
          </td>
          <td
            v-for="d in data.dances"
            :key="d.dance_id"
            :colspan="dancesExpanded[d.dance_id] ? data.adjudicators.length + 1 : 1"
            @click="toggleDance(d.dance_id)"
            class="is-clickable"
          >
            {{ dancesExpanded[d.dance_id] ? d.name : d.tag }}
          </td>
          <td rowspan="2" class="total table-ranking--bottom">
            {{ $t("round.reports.ranking_report.total") }}
          </td>
        </tr>
        <tr>
          <template v-for="d in data.dances">
            <td
              v-for="a in data.adjudicators"
              :key="`${d.dance_id}-${a.adjudicator_id}`"
              class="highlighted-col"
              :class="{
                hidden: !dancesExpanded[d.dance_id],
                adjudicator: dancesExpanded[d.dance_id]
              }"
            >
              <v-tooltip bottom color="primary" dark>
                <template v-slot:activator="{ on }">
                  <span v-on="on" class="is-clickable">{{ a.tag }}</span>
                </template>
                <span>{{ a.name }}</span>
              </v-tooltip>
            </td>
            <td :key="`${d.dance_id}-sum`" class="highlighted-col sum">
              {{ $t("round.reports.ranking_report.sum") }}
            </td>
          </template>
        </tr>
        <tr class="table-ranking--padding"></tr>
      </thead>
      <template v-for="rank in data.rank">
        <tbody :key="rank.number">
          <tr>
            <td :rowspan="rowSpan(rank)" class="rank highlighted-col">{{ rank.rank }}</td>
            <td :rowspan="rowSpan(rank)" class="couple text-left">
              {{ rank.name }}<br />
              {{ rank.team }}
            </td>
            <td :rowspan="rowSpan(rank)" class="number highlighted-col">{{ rank.number }}</td>
            <td class="round">{{ data.rounds[finalRound(rank)].tag }}</td>
            <template v-for="d in data.dances">
              <template v-if="!!data.results[rank.number][finalRound(rank)][d.dance_id]">
                <td
                  v-for="a in data.adjudicators"
                  :key="`${rank.number}-${finalRound(rank)}-${d.dance_id}-${a.adjudicator_id}`"
                  :class="{
                    hidden: !dancesExpanded[d.dance_id],
                    adjudicator: dancesExpanded[d.dance_id]
                  }"
                >
                  {{ data.results[rank.number][finalRound(rank)][d.dance_id][a.adjudicator_id] }}
                </td>
                <td
                  :key="`${rank.number}-${finalRound(rank)}-${d.dance_id}-sum`"
                  class="sum highlighted-col"
                >
                  {{ data.results[rank.number][finalRound(rank)][d.dance_id].sum }}
                </td>
              </template>
            </template>
            <td :key="`${rank.number}-${finalRound(rank)}-total`" class="total total-col">
              {{ data.results[rank.number][finalRound(rank)].total }}
            </td>
          </tr>
          <tr v-for="r in roundRows(rank)" :key="`${rank.number}-${r}`">
            <td class="round">{{ data.rounds[r].tag }}</td>
            <template v-for="d in data.dances">
              <template v-if="!!data.results[rank.number][r][d.dance_id]">
                <td
                  v-for="a in data.adjudicators"
                  :key="`${rank.number}-${r}-${d.dance_id}-${a.adjudicator_id}`"
                  :class="{
                    hidden: !dancesExpanded[d.dance_id],
                    adjudicator: dancesExpanded[d.dance_id]
                  }"
                >
                  {{ data.results[rank.number][r][d.dance_id][a.adjudicator_id] }}
                </td>
                <td :key="`${rank.number}-${r}-${d.dance_id}-sum`" class="sum highlighted-col">
                  {{ data.results[rank.number][r][d.dance_id].sum }}
                </td>
              </template>
            </template>
            <td :key="`${rank.number}-${r}-total`" class="total total-col">
              {{ data.results[rank.number][r].total }}
            </td>
          </tr>
        </tbody>
        <tbody :key="`${rank.number}-pad`">
          <tr class="table-ranking--padding"></tr>
        </tbody>
      </template>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      dancesExpanded: Object.assign(
        ...this.data.dances.map(d => ({
          [d.dance_id]: false
        }))
      )
    };
  },
  computed: {
    changePerDance() {
      return this.round.competition.mode === this.$constants.CHANGE_PER_DANCE;
    }
  },
  methods: {
    rowSpan(rank) {
      return Object.values(this.data.results[rank.number]).length;
    },
    rounds(rank) {
      return Object.keys(this.data.results[rank.number]).sort((a, b) => b - a);
    },
    finalRound(rank) {
      return this.rounds(rank)[0];
    },
    roundRows(rank) {
      let rounds = [...this.rounds(rank)];
      rounds.shift();
      return rounds;
    },
    toggleDance(dance_id) {
      this.dancesExpanded[dance_id] = !this.dancesExpanded[dance_id];
      Object.keys(this.dancesExpanded)
        .filter(k => k !== String(dance_id))
        .forEach(k => (this.dancesExpanded[k] = false));
    }
  }
};
</script>

<style
  src="../../../../../assets/css/components/table-ranking/table-ranking.scss"
  lang="scss"
></style>

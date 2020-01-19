<template>
  <div v-if="round">
    <template v-if="!createNextRound">
      <v-row>
        <v-col cols="12" md="8" lg="12" xl="8" v-if="round">
          <progress-table
            v-if="round.competition.mode !== $constants.CHANGE_PER_DANCE"
            :round="round"
            :data="data"
            :competitors="competitors"
            :loading="loading"
          />
          <progress-table
            v-else
            :round="round"
            :data="data"
            :leads="competitors.leads"
            :follows="competitors.follows"
            :loading="loading"
          />
        </v-col>
        <v-col cols="12" md="4" lg="12" xl="4" v-if="round">
          <next-round-after-general-look
            :round="round"
            :progress-loading="loading"
            v-if="round.type === $constants.GENERAL_LOOK"
            @updated="updateRound"
          />
          <add-remove-couple-card class="mb-5" v-if="showAddRemoveCouple" @update="updateData" />
          <delete-round-card class="mb-5" :round="round" />
        </v-col>
      </v-row>
    </template>
    <next-round
      v-else
      :round="round"
      :data="data"
      :cutoffs="cutoffs"
      :progress-loading="loading"
      @updated="updateRound"
    />
  </div>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import Loading from "@/components/general/loading/Loading";
import ProgressTable from "@/components/tournament_office/round/progress/progress_table/ProgressTable";
import NextRound from "@/components/tournament_office/round/progress/NextRound";
import DeleteRoundCard from "@/components/tournament_office/round/progress/DeleteRoundCard";
import AddRemoveCoupleCard from "@/components/tournament_office/round/progress/AddRemoveCoupleCard";
import NextRoundAfterGeneralLook from "@/components/tournament_office/round/progress/NextRoundAfterGeneralLook";
export default {
  components: {
    NextRoundAfterGeneralLook,
    AddRemoveCoupleCard,
    DeleteRoundCard,
    NextRound,
    ProgressTable,
    Loading
  },
  data: function() {
    return {
      loading: false,
      round: null,
      data: null,
      competitors: null,
      cutoffs: null
    };
  },
  created() {
    this.getRound();
  },
  computed: {
    createNextRound() {
      return this.round && this.round.completed;
    },
    showAddRemoveCouple() {
      return (
        this.round &&
        this.round.type !== this.$constants.FINAL &&
        this.round.competition.rounds === 1 &&
        this.round.competition.mode !== this.$constants.CHANGE_PER_DANCE
      );
    }
  },
  methods: {
    getRound() {
      this.loading = true;
      Vue.axios
        .get(`round/${this.$route.params.round_id}/progress`)
        .then(response => {
          const res = response.data;
          this.round = res.round;
          this.data = res.data;
          this.competitors = res.competitors;
          let cutoffs = res.cutoffs;
          if (cutoffs) {
            cutoffs.find(x => x.value === -1).text = this.$t("round.new_round.cutoff.all_couples");
            this.cutoffs = res.cutoffs;
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
    updateData(data) {
      this.data = data.data;
      this.competitors = data.competitors;
    },
    updateRound(round) {
      this.round = round;
    }
  },
  watch: {
    $route: function() {
      this.getRound();
    }
  }
};
</script>

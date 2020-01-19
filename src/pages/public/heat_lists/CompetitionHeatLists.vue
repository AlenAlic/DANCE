<template>
  <v-card class="fill-height" v-if="!loading">
    <v-card-text v-if="!!round">
      <heats-by-starting-no
        v-if="round.competition.mode !== $constants.CHANGE_PER_DANCE"
        :round="round"
        :data="data.heat_mapping"
        :competitors="data.competitors"
      />
      <heats-by-starting-no
        v-else
        :round="round"
        :data="data.heat_mapping"
        :leads="data.competitors.leads"
        :follows="data.competitors.follows"
        :partner-mapping="data.partner_mapping"
        change-partner-mode
      />
    </v-card-text>
    <template v-else>
      <v-card-text>
        {{ $t("public.heat_lists.no_heat_lists", { competition: competition.name }) }}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text exact :to="{ name: 'heat_lists' }">
          {{ $t("public.heat_lists.back") }}
        </v-btn>
      </v-card-actions>
    </template>
  </v-card>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import Loading from "@/components/general/loading/Loading";
import HeatsByStartingNo from "@/components/tournament_office/round/reports/heats_by_starting_number/HeatsByStartingNo";
import { ERROR_CODES, getNetworkErrorCode } from "@/api/util/network-errors";
export default {
  components: { HeatsByStartingNo, Loading },
  data: function() {
    return {
      loading: false,
      round: null,
      data: null,
      competition: null
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get(`competition/heat_lists/${this.$route.params.competition_id}`)
        .then(response => {
          this.round = response.data.round;
          this.data = response.data.data;
        })
        .catch(error => {
          const status = getNetworkErrorCode(error);
          if (status === ERROR_CODES.BAD_REQUEST) {
            this.competition = error.response.data;
          } else {
            this.$router.push({
              name: "heat_lists"
            });
          }
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

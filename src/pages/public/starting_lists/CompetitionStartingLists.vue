<template>
  <v-card class="fill-height" v-if="!loading">
    <v-card-text v-if="competition && competitors">
      <qualified-starts
        v-if="competition.mode === $constants.SINGLE_PARTNER"
        :competition="competition"
        :competitors="competitors"
      />
      <qualified-starts
        v-else
        :competition="competition"
        :leads="competitors.leads"
        :follows="competitors.follows"
        change-partner-mode
      />
    </v-card-text>
    <template v-else>
      <v-card-text>
        {{ $t("public.starting_lists.no_starting_lists", { competition: competition.name }) }}
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text exact :to="{ name: 'starting_lists' }">
          {{ $t("public.starting_lists.back") }}
        </v-btn>
      </v-card-actions>
    </template>
  </v-card>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import Loading from "@/components/general/loading/Loading";
import QualifiedStarts from "@/components/tournament_office/round/reports/qualified_starts/QualifiedStarts";
import { ERROR_CODES, getNetworkErrorCode } from "@/api/util/network-errors";
export default {
  components: { QualifiedStarts, Loading },
  data: function() {
    return {
      loading: false,
      competition: null,
      competitors: null
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get(`competition/starting_lists/${this.$route.params.competition_id}`)
        .then(response => {
          this.competition = response.data.competition;
          this.competitors = response.data.competitors;
        })
        .catch(error => {
          const status = getNetworkErrorCode(error);
          if (status === ERROR_CODES.BAD_REQUEST) {
            this.competition = error.response.data;
          } else {
            this.$router.push({
              name: "starting_lists"
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

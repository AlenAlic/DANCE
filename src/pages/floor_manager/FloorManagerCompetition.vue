<template>
  <v-card v-if="round" class="fill-height">
    <v-card-title>
      {{ round.competition.name }} ({{ round.mode }}) / {{ round.name }}
    </v-card-title>
    <v-tabs v-model="tab" centered hide-slider show-arrows v-if="round" @change="changeTab">
      <v-tab v-for="dance in round.dances" :key="dance.dance_id" :href="`#${dance.dance_id}`">
        {{ dance.name }}
      </v-tab>
    </v-tabs>
    <v-divider />
    <template v-if="round.floors.length > 1">
      <v-tabs v-model="floor" centered hide-slider show-arrows v-if="round">
        <v-tab v-for="f in round.floors" :key="f" :href="`#${f}`" @click="changeTab">
          {{ $t("round.floor_management.floor") }} {{ f }}
        </v-tab>
      </v-tabs>
      <v-divider />
    </template>
    <v-card-text>
      <v-progress-linear indeterminate v-if="loading" />
    </v-card-text>
    <v-tabs-items v-model="tab" v-if="round">
      <v-tab-item v-for="dance in round.dances" :key="dance.dance_id" :value="`${dance.dance_id}`">
        <template v-if="data && round.floors.length > 1">
          <v-card flat tile v-for="heat in Object.keys(data)" :key="heat">
            <v-card-title>{{ $t("round.floor_management.heat") }} {{ heat }}</v-card-title>
            <v-card-text>
              <v-row v-if="round.floors.length > 1" no-gutters>
                <check-present
                  v-for="couple in data[heat][floor]"
                  :key="couple.couple_present_id"
                  :couple="couple"
                />
              </v-row>
            </v-card-text>
          </v-card>
        </template>
        <template v-else-if="data">
          <v-card flat tile v-for="heat in Object.keys(data)" :key="heat">
            <v-card-title>{{ $t("round.floor_management.heat") }} {{ heat }}</v-card-title>
            <v-card-text>
              <v-row no-gutters>
                <check-present
                  v-for="couple in data[heat]"
                  :key="couple.couple_present_id"
                  :couple="couple"
                />
              </v-row>
            </v-card-text>
          </v-card>
        </template>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
  <loading v-else-if="loading" />
  <v-card v-else class="fill-height">
    <v-card-title>
      {{ $t("floor_manager.not_available", { competition: competition.name }) }}
    </v-card-title>
    <v-card-actions>
      <v-btn text color="primary" @click="getRound">
        {{ $t("floor_manager.reload") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import Vue from "vue";
import Loading from "@/components/general/loading/Loading";
import CheckPresent from "@/components/floor_manager/CheckPresent";
import { ERROR_CODES, getNetworkErrorCode } from "@/api/util/network-errors";
export default {
  components: { CheckPresent, Loading },
  data: function() {
    return {
      loading: false,
      round: null,
      tab: null,
      data: {},
      floor: null,
      competition: null
    };
  },
  created() {
    this.getRound();
  },
  methods: {
    getRound() {
      this.loading = true;
      Vue.axios
        .get(`competition/floor_manager/${this.$route.params.competition_id}`)
        .then(response => {
          const round = response.data.round;
          const data = response.data.data;
          this.round = round;
          this.data = data.mapping;
          this.tab = String(round.first_dance.dance_id);
        })
        .catch(error => {
          const status = getNetworkErrorCode(error);
          if (status === ERROR_CODES.BAD_REQUEST) {
            this.competition = error.response.data;
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getData() {
      this.loading = true;
      Vue.axios
        .get(`round/${this.round.round_id}/floor_management/dance/${this.tab}`)
        .then(response => {
          this.data = response.data.mapping;
        })
        .catch(() => {})
        .finally(() => {
          this.loading = false;
        });
    },
    changeTab() {
      this.data = null;
      this.getData();
    }
  },
  watch: {
    $route: function() {
      this.getRound();
      this.round = null;
      this.tab = null;
      this.data = {};
      this.floor = null;
    }
  }
};
</script>

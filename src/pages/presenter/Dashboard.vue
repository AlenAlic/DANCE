<template>
  <v-card class="fill-height" v-if="!loading">
    <v-card-title class="justify-center">
      {{ $t("presenter.title") }}
    </v-card-title>
    <v-card-text v-if="!!competitions">
      <v-row no-gutters>
        <v-checkbox
          v-for="comp in competitions"
          :key="comp.competition_id"
          v-model="selectedCompetitions"
          :label="comp.name"
          :value="comp"
          hide-details
          class="my-1 mr-4"
          :disabled="disableCheckBox(comp)"
        ></v-checkbox>
      </v-row>
      <v-row>
        <v-col v-for="comp in selectedCompetitions" :key="comp.competition_id">
          <round-card :competition="comp" />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import Loading from "@/components/general/loading/Loading";
import RoundCard from "@/components/presenter/RoundCard";
export default {
  components: { RoundCard, Loading },
  data: function() {
    return {
      loading: false,
      competitions: [],
      selectedCompetitions: []
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get("competition/presenter")
        .then(response => {
          this.competitions = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    disableCheckBox(comp) {
      return (
        this.selectedCompetitions.length >= 3 &&
        !this.selectedCompetitions.find(c => c.competition_id === comp.competition_id)
      );
    }
  }
};
</script>

<template>
  <v-row>
    <v-col
      cols="12"
      v-if="
        $store.state.events.activeEvent &&
          $store.state.competitions.competitions.length === 0 &&
          !$store.state.competitions.loading
      "
    >
      <defaults-form />
    </v-col>
    <v-col cols="12" xl="8" v-if="$store.state.config.config">
      <new-competition-form />
    </v-col>
    <v-col cols="12" xl="4">
      <save-event-results class="mb-3" />
      <reset-database-card />
    </v-col>
  </v-row>
</template>

<script>
import ResetDatabaseCard from "@/components/tournament_office/event/ResetDatabaseCard";
import DefaultsForm from "@/components/tournament_office/event/setup/DefaultsForm";
import NewCompetitionForm from "@/components/tournament_office/event/setup/NewCompetitionForm";
import SaveEventResults from "@/components/tournament_office/event/SaveEventResults";
export default {
  components: { SaveEventResults, NewCompetitionForm, DefaultsForm, ResetDatabaseCard }
};
</script>

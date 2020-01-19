<template>
  <v-card>
    <v-card-title>
      {{ $t("event.assignments.title") }}
    </v-card-title>
    <v-card-text>
      <span v-if="edited && !loading">{{ $t("event.assignments.text") }}</span>
    </v-card-text>
    <v-card-actions>
      <v-btn text color="primary" @click="saveAssignments" :disabled="saving || loading">
        {{ $t("event.assignments.save") }}
      </v-btn>
      <v-spacer />
      <v-btn text color="primary" @click="checkAll" :disabled="saving || loading">
        <span v-if="showCheckAll">{{ $t("event.assignments.check") }}</span>
        <span v-else>{{ $t("event.assignments.uncheck") }}</span>
      </v-btn>
    </v-card-actions>
    <v-card-text>
      <v-progress-linear indeterminate v-if="saving || loading" />
    </v-card-text>
    <v-card-text v-if="!loading">
      <v-simple-table>
        <template v-slot:default>
          <template v-for="day in days">
            <thead :key="`head-${day}`">
              <tr>
                <td colspan="2"></td>
                <td :colspan="competitionsOnDay[day].length">
                  <span class="title">{{ day }}</span>
                </td>
              </tr>
              <tr>
                <td colspan="2"></td>
                <td
                  v-for="comp in competitionsOnDay[day]"
                  :key="`adj-${comp.competition_id}`"
                  class="text-center"
                >
                  {{ comp.adjudicators.length }}
                </td>
              </tr>
            </thead>
            <tbody :key="`body-${day}`">
              <tr>
                <td class="subtitle-2">{{ $t("event.assignments.adjudicator") }}</td>
                <td class="subtitle-2">{{ $t("event.assignments.number") }}</td>
                <td
                  v-for="comp in competitionsOnDay[day]"
                  :key="comp.competition_id"
                  class="text-center subtitle-2"
                >
                  {{ `${comp.discipline.tag} ${comp.dancing_class.tag}` }}
                </td>
              </tr>
              <template v-for="adj in $store.state.adjudicators.adjudicators">
                <tr :key="adj.adjudicator_id">
                  <td>{{ adj.name }}</td>
                  <td>
                    {{
                      adj.competitions.filter(
                        c =>
                          !!competitionsOnDay[day].find(x => x.competition_id === c.competition_id)
                      ).length
                    }}
                  </td>
                  <td v-for="comp in competitionsOnDay[day]" :key="comp.competition_id">
                    <v-checkbox
                      v-model="assigned"
                      :value="`${comp.competition_id}-${adj.adjudicator_id}`"
                      class="mx-3 mt-3 py-0 justify-center"
                      :class="{ 'is-disabled': comp.has_rounds }"
                      :disabled="comp.has_rounds"
                      color="primary"
                      @change="edited = true"
                    ></v-checkbox>
                  </td>
                </tr>
              </template>
            </tbody>
          </template>
        </template>
      </v-simple-table>
    </v-card-text>
  </v-card>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { SET_COMPETITIONS } from "@/store/modules/competitions";
import { SET_ADJUDICATORS } from "@/store/modules/adjudicators";
export default {
  created() {
    this.setAssigned();
  },
  data: function() {
    return {
      assigned: [],
      saving: false,
      edited: false
    };
  },
  computed: {
    competitions() {
      return this.$store.state.competitions.competitions;
    },
    openCompetitions() {
      return this.competitions.filter(c => !c.has_rounds);
    },
    closedCompetitions() {
      return this.competitions.filter(c => c.has_rounds);
    },
    closedAssignments() {
      return this.closedCompetitions
        .map(c => c.adjudicators.map(a => `${c.competition_id}-${a.adjudicator_id}`))
        .flat();
    },
    openAssignments() {
      return this.openCompetitions
        .map(c =>
          this.$store.state.adjudicators.adjudicators.map(
            a => `${c.competition_id}-${a.adjudicator_id}`
          )
        )
        .flat();
    },
    // originalAssignments() {
    //   return this.$store.state.adjudicators.adjudicators
    //     .map(a => a.competitions.map(c => `${c.competition_id}-${a.adjudicator_id}`))
    //     .flat()
    //     .sort();
    // },
    // currentAssignments() {
    //   return [...this.assigned].sort();
    // },
    // hasNewAssignments() {
    //   return JSON.stringify(this.originalAssignments) !== JSON.stringify(this.currentAssignments);
    // },
    loading() {
      return this.$store.state.competitions.loading || this.$store.state.adjudicators.loading;
    },
    days() {
      const comps = this.competitions;
      return [...new Set(comps.map(c => this.$util.dateTimeFromUTC(c.date).toFormat("DDDD")))];
    },
    competitionsOnDay() {
      let days = {};
      this.days.forEach(
        day =>
          (days[day] = this.competitions.filter(
            c => this.$util.dateTimeFromUTC(c.date).toFormat("DDDD") === day
          ))
      );
      return days;
    },
    showCheckAll() {
      return this.assigned.length < [...this.openAssignments, ...this.closedAssignments].length;
    }
  },
  methods: {
    setAssigned() {
      this.assigned = this.competitions
        .map(c => c.adjudicators.map(a => `${c.competition_id}-${a.adjudicator_id}`))
        .flat();
    },
    checkAll() {
      if (this.showCheckAll) {
        this.assigned = [...this.openAssignments, ...this.closedAssignments];
      } else {
        this.assigned = this.closedAssignments;
      }
    },
    saveAssignments() {
      this.saving = true;
      Vue.axios
        .patch("event/assignments", {
          assignments: this.assigned
        })
        .then(response => {
          store.commit(SET_COMPETITIONS, response.data.competitions);
          store.commit(SET_ADJUDICATORS, response.data.adjudicators);
        })
        .finally(() => {
          this.saving = false;
        });
    }
  },
  watch: {
    competitions: function() {
      this.setAssigned();
    }
  }
};
</script>

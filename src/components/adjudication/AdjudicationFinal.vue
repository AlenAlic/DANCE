<template>
  <v-row>
    <v-col cols="auto">
      <v-row
        v-for="placing in placings"
        :key="`${placing.final_placing_id}-${placing.final_placing}`"
        no-gutters
        justify="start"
        class="my-2"
      >
        <adjudication-final-button
          :adjudicator="adjudication.adjudicator"
          :placing="placing"
          :disabled="disabled"
          v-model="couple"
        />
      </v-row>
    </v-col>
    <v-col>
      <v-row
        v-for="placing in placings"
        :key="`${placing.final_placing_id}-${placing.final_placing}`"
        no-gutters
        justify="space-between"
        class="my-2"
      >
        <div :style="{ flexGrow: (placing.final_placing - 1) / (placings.length - 1) }"></div>
        <div>
          <v-btn disabled v-if="placing.final_placing > 0">
            {{ placing.final_placing }}
          </v-btn>
          <v-btn v-else text disabled></v-btn>
        </div>
        <div :style="{ flexGrow: 1 - (placing.final_placing - 1) / (placings.length - 1) }"></div>
      </v-row>
    </v-col>
    <v-col cols="auto">
      <v-row
        v-for="place in Array.from(Array(placings.length).keys()).map(x => x + 1)"
        :key="place"
        no-gutters
        justify="end"
        class="my-2"
      >
        <v-btn @click="placeCouple(place)" depressed color="primary" :disabled="disabled">
          {{ place }}
        </v-btn>
      </v-row>
      <v-row no-gutters justify="end" class="my-2">
        <v-btn @click="placeCouple(0)" outlined color="error" :disabled="disabled">
          x
        </v-btn>
      </v-row>
    </v-col>
    <toast v-if="error" :message="error" @closed="error = null" />
  </v-row>
</template>

<script>
import Vue from "vue";
import AdjudicationFinalButton from "@/components/adjudication/AdjudicationFinalButton";
import { SET_PLACINGS, SET_ADJUDICATION } from "@/store/modules/adjudication";
import { ERROR_CODES, getNetworkErrorCode } from "@/api/util/network-errors";
import Toast from "@/components/general/toast/Toast";
export default {
  components: { Toast, AdjudicationFinalButton },
  props: {
    adjudication: { type: Object, default: () => {} },
    disabled: { type: Boolean, default: true }
  },
  data: function() {
    return {
      loading: false,
      couple: 0,
      placings: this.adjudication.placings,
      error: null
    };
  },
  methods: {
    placeCouple(place) {
      const placings = [...this.placings];
      const placing = placings.find(p => p.final_placing_id === this.couple);
      let placeToUpdate, finalPlacingsToUpdate;
      if (place < placing.final_placing) {
        placing.final_placing = place;
        if (place > 0) {
          placeToUpdate = place;
          finalPlacingsToUpdate = placings.filter(
            p => p.final_placing === placeToUpdate && p.final_placing_id !== this.couple
          );
          while (finalPlacingsToUpdate.length > 0 && placeToUpdate !== 0) {
            placeToUpdate = (placeToUpdate + 1) % (placings.length + 1);
            finalPlacingsToUpdate[0].final_placing = placeToUpdate;
            finalPlacingsToUpdate = placings.filter(
              p =>
                p.final_placing === placeToUpdate &&
                p.final_placing_id !== finalPlacingsToUpdate[0].final_placing_id
            );
          }
        }
      } else if (place > placing.final_placing) {
        placing.final_placing = place;
        if (place > 0) {
          placeToUpdate = place;
          finalPlacingsToUpdate = placings.filter(
            p => p.final_placing === placeToUpdate && p.final_placing_id !== this.couple
          );
          while (finalPlacingsToUpdate.length > 0 && placeToUpdate !== 0) {
            placeToUpdate = (placeToUpdate - 1) % (placings.length + 1);
            finalPlacingsToUpdate[0].final_placing = placeToUpdate;
            finalPlacingsToUpdate = placings.filter(
              p =>
                p.final_placing === placeToUpdate &&
                p.final_placing_id !== finalPlacingsToUpdate[0].final_placing_id
            );
          }
        }
      }
      this.placings = placings;
      this.couple = 0;
      this.sendPlacings();
    },
    sendPlacings() {
      if (!this.disabled) {
        this.loading = true;
        Vue.axios
          .patch(
            `adjudication/round/${this.$route.params.round_id}/dance/${this.$route.params.dance_id}/placings`,
            {
              placings: this.placings
            }
          )
          .then(response => {
            this.$store.commit(SET_PLACINGS, response.data);
          })
          .catch(error => {
            const status = getNetworkErrorCode(error);
            if (status === ERROR_CODES.BAD_REQUEST) {
              const adjudication = error.response.data;
              this.$store.commit(SET_ADJUDICATION, adjudication);
              this.placings = adjudication.placings;
              this.error = this.$t("adjudicator.errors.round_closed");
            }
          })
          .finally(() => {
            this.loading = false;
          });
      }
    }
  }
};
</script>

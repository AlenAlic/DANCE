<template>
  <v-app-bar dark app :color="color">
    <div class="status_bar" :class="{ loading: adjudication.loading }">
      <div class="status__cell start">
        <v-btn
          v-if="!!adjudication.previous_dance"
          :disabled="adjudication.loading"
          outlined
          small
          @click="switchPage(adjudication.previous_dance)"
        >
          {{ adjudication.previous_dance.name }}
        </v-btn>
        <v-btn
          v-else
          :disabled="adjudication.loading"
          outlined
          small
          :to="{ name: 'adjudicator.dashboard' }"
        >
          {{ $t("adjudicator.header.exit") }}
        </v-btn>
        <span v-if="showTarget" class="overline mt-1">
          {{ $t("adjudicator.header.target", { target: adjudication.round.target_marks }) }}
        </span>
      </div>

      <div class="status__cell center is-clickable" v-if="!!adjudication.dance" @click="refresh">
        <div>
          {{ adjudication.dance.name }}
        </div>
        <span v-if="!adjudication.dance.is_active" class="overline">
          {{ $t("adjudicator.header.closed") }}
        </span>
        <span v-if="showTarget" class="overline">
          {{ `${marked}/${marksList.length}` }}
        </span>
        <span v-if="showPlacedCouples" class="overline">
          {{ `${placed}/${placingsList.length}` }}
        </span>
      </div>

      <div class="status__cell end">
        <v-btn
          v-if="!!adjudication.next_dance"
          :disabled="adjudication.loading"
          outlined
          small
          @click="switchPage(adjudication.next_dance)"
        >
          {{ adjudication.next_dance.name }}
        </v-btn>
        <v-btn
          v-else
          :disabled="adjudication.loading"
          outlined
          small
          :to="{ name: 'adjudicator.dashboard' }"
        >
          {{ $t("adjudicator.header.exit") }}
        </v-btn>
        <span v-if="showTarget" class="overline mt-1">
          {{ $t("adjudicator.header.noted", { noted: noted }) }}
        </span>
      </div>
    </div>
  </v-app-bar>
</template>

<script>
import store from "@/store";
import { ADJUDICATION } from "@/store/modules/adjudication";
export default {
  props: {
    adjudication: { type: Object, default: () => {} }
  },
  computed: {
    final() {
      return this.adjudication.round && this.adjudication.round.type === this.$constants.FINAL;
    },
    color() {
      if (this.adjudication.loading) return "primary";
      if (!this.final) {
        if (
          this.marked >= this.adjudication.round.min_marks &&
          this.marked <= this.adjudication.round.max_marks
        ) {
          if (this.noted > 0) return "info";
          return "success";
        } else if (
          this.marked <= this.adjudication.round.min_marks ||
          this.marked >= this.adjudication.round.max_marks
        ) {
          return "error";
        }
      } else {
        return this.placingsList.length === this.placed ? "success" : "error";
      }
      return "grey";
    },
    showTarget() {
      return !!this.adjudication.round && !this.final;
    },
    marksList() {
      return Object.values(this.adjudication.marks).flat();
    },
    marked() {
      return this.marksList.filter(m => m.mark).length;
    },
    noted() {
      return this.marksList.filter(m => m.notes > 0).length;
    },
    showPlacedCouples() {
      return !!this.adjudication.round && this.final;
    },
    placingsList() {
      return this.adjudication.placings;
    },
    placed() {
      return this.placingsList.filter(p => p.final_placing !== 0).length;
    }
  },
  methods: {
    switchPage(dance) {
      const round_id = this.adjudication.round.round_id;
      const dance_id = dance.dance_id;
      store.dispatch(ADJUDICATION, {
        round_id: round_id,
        dance_id: dance_id
      });
      this.$router.push({
        name: "adjudicator.dance",
        params: {
          round_id: round_id,
          dance_id: dance_id
        }
      });
    },
    refresh() {
      store.dispatch(ADJUDICATION, {
        round_id: this.adjudication.round.round_id,
        dance_id: this.adjudication.dance.dance_id
      });
    }
  }
};
</script>

<style scoped lang="scss">
@import "../../assets/css/general/flex";
.status_bar {
  @extend .flex;
  width: 100%;

  &.loading {
    color: rgba(white, 0.3);
  }

  .status__cell {
    @extend .flex;
    @extend .flex-column;
    @extend .align-items-center;
    flex: 1;
    @extend .align-self-center;

    &.start {
      @extend .align-items-start;
    }

    &.end {
      @extend .align-items-end;
    }
  }
}
</style>

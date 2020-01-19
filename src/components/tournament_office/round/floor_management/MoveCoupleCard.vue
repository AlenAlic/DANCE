<template>
  <v-card>
    <v-card-title>
      {{ $t("round.floor_management.move_couple.modal.title") }}
    </v-card-title>
    <v-card-subtitle>
      {{ $t("round.floor_management.move_couple.modal.subtitle") }}
    </v-card-subtitle>
    <v-card-text>
      <v-select
        v-model="fromHeat"
        :items="fromHeats"
        :label="$t('round.floor_management.move_couple.modal.from.label')"
        :hint="$t('round.floor_management.move_couple.modal.from.hint')"
        persistent-hint
        :no-data-text="$t('general.loading')"
        :loading="loading"
        item-value="heat_id"
        item-text="number"
      ></v-select>
      <v-select
        v-model="couple"
        :items="couplesList"
        :label="$t('round.floor_management.move_couple.modal.couple.label')"
        :hint="$t('round.floor_management.move_couple.modal.couple.hint')"
        persistent-hint
        :no-data-text="$t('general.loading')"
        :loading="loading"
        item-value="couple_id"
        item-text="number"
      ></v-select>
      <v-select
        v-model="toHeat"
        :items="toHeats"
        :label="$t('round.floor_management.move_couple.modal.to.label')"
        :hint="$t('round.floor_management.move_couple.modal.to.hint')"
        persistent-hint
        :no-data-text="$t('general.loading')"
        :loading="loading"
        item-value="heat_id"
        item-text="number"
      ></v-select>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        :loading="loading"
        :disabled="!complete"
        color="primary"
        text
        @click="$emit('move', returnData)"
      >
        {{ $t("round.floor_management.move_couple.modal.move") }}
      </v-btn>
      <v-btn text @click="$emit('cancel')">
        {{ $t("general.cancel") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import Vue from "vue";
export default {
  props: {
    round: { type: Object, default: () => {} },
    dance_id: { type: String, default: null }
  },
  data: function() {
    return {
      loading: false,
      data: null,
      fromHeat: null,
      toHeat: null,
      couple: null
    };
  },
  created() {
    this.loading = true;
    Vue.axios
      .get(`round/${this.$route.params.round_id}/floor_management/dance/${this.dance_id}/move`)
      .then(response => {
        this.data = response.data;
      })
      .finally(() => {
        this.loading = false;
      });
  },
  computed: {
    returnData() {
      return {
        couple_id: this.couple,
        from_id: this.fromHeat,
        to_id: this.toHeat
      };
    },
    complete() {
      return this.fromHeat && this.toHeat && this.couple;
    },
    fromHeats() {
      return this.data ? this.data.map(d => d.heat) : [];
    },
    couplesList() {
      return this.data && this.fromHeat
        ? this.data.find(d => d.heat.heat_id === this.fromHeat).couples
        : [];
    },
    toHeats() {
      return this.data ? this.data.map(d => d.heat).filter(h => h.heat_id !== this.fromHeat) : [];
    }
  }
};
</script>

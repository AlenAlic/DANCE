<template>
  <div class="cell_container">
    <div
      class="cell number is-clickable subtitle-2"
      :class="{ disabled: disabled }"
      @click.stop="setNotes"
    >
      <b>{{ number }}</b>
    </div>
    <div
      class="cell mark"
      :class="{ loading: loading, disabled: disabled, marked: mark.mark, noted: mark.notes > 0 }"
      @click.stop="giveMark"
    >
      {{ ".".repeat(mark.notes) }}
    </div>
    <toast v-if="error" :message="error" @closed="error = null" />
  </div>
</template>

<script>
import Vue from "vue";
import { SET_ADJUDICATION, SET_MARKS } from "@/store/modules/adjudication";
import { ERROR_CODES, getNetworkErrorCode } from "@/api/util/network-errors";
import Toast from "@/components/general/toast/Toast";
export default {
  components: { Toast },
  props: {
    adjudicator: { type: Object, default: () => {} },
    mark: { type: Object, default: () => {} },
    disabled: { type: Boolean, default: true }
  },
  data: function() {
    return {
      loading: false,
      error: null
    };
  },
  computed: {
    number() {
      return this.adjudicator.assignment === this.$constants.ADJUDICATION_FOLLOW
        ? this.mark.follow_number
        : this.mark.number;
    }
  },
  methods: {
    giveMark() {
      if (!this.disabled) {
        this.loading = true;
        Vue.axios
          .patch(`adjudication/mark/${this.mark.mark_id}/mark`, {
            mark: !this.mark.mark
          })
          .then(response => {
            this.$store.commit(SET_MARKS, response.data);
          })
          .catch(error => {
            const status = getNetworkErrorCode(error);
            if (status === ERROR_CODES.BAD_REQUEST) {
              this.$store.commit(SET_ADJUDICATION, error.response.data);
              this.error = this.$t("adjudicator.errors.round_closed");
            }
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
    setNotes() {
      if (!this.disabled && !this.mark.mark) {
        this.loading = true;
        Vue.axios
          .patch(`adjudication/mark/${this.mark.mark_id}/notes`, {
            notes: this.mark.notes + 1
          })
          .then(response => {
            this.$store.commit(SET_MARKS, response.data);
          })
          .catch(error => {
            const status = getNetworkErrorCode(error);
            if (status === ERROR_CODES.BAD_REQUEST) {
              this.$store.commit(SET_ADJUDICATION, error.response.data);
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

<style
  src="../../assets/css/components/adjudication-cell/adjudication-cell.scss"
  lang="scss"
></style>

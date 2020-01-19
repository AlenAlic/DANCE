<template>
  <v-checkbox
    class="ml-3 mr-5 my-3"
    hide-details
    color="success"
    :label="`${couple.number}`"
    :indeterminate="loading"
    v-model="present"
    @change="markPresent"
  >
  </v-checkbox>
</template>

<script>
import Vue from "vue";
export default {
  props: {
    couple: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      present: this.couple.present
    };
  },
  methods: {
    markPresent() {
      this.loading = true;
      Vue.axios
        .patch(`floor_manager/${this.couple.couple_present_id}`, {
          present: this.present
        })
        .then(response => {
          this.present = response.data.present;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

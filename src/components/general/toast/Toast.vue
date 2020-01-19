<template>
  <v-snackbar
    v-model="active"
    :absolute="absolute"
    :bottom="bottom"
    :color="color"
    :left="left"
    :multi-line="multiLine"
    :right="right"
    :timeout="timeout"
    :top="top"
    :vertical="vertical"
    @click="dismiss"
    @input="close"
  >
    <div>
      <v-icon dark left v-if="!!computedIcon">
        {{ computedIcon }}
      </v-icon>
      <slot>{{ message }}</slot>
    </div>
    <v-btn :icon="!closeText" :text="!!closeText" v-if="dismissable" @click="close">
      <v-icon v-if="dismissable && !closeText">{{ closeIcon }}</v-icon>
      <span v-if="dismissable && !!closeText">{{ closeText }}</span>
    </v-btn>
  </v-snackbar>
</template>

<script>
export default {
  props: {
    absolute: { type: Boolean, default: false },
    bottom: { type: Boolean, default: false },
    left: { type: Boolean, default: false },
    multiLine: { type: Boolean, default: false },
    right: { type: Boolean, default: false },
    timeout: { type: Number, default: 6000 },
    top: { type: Boolean, default: true },
    vertical: { type: Boolean, default: false },
    info: { type: Boolean, default: false },
    success: { type: Boolean, default: false },
    error: { type: Boolean, default: false },
    warning: { type: Boolean, default: false },
    closeIcon: { type: String, default: "mdi-close" },
    closeText: { type: String, default: "" },
    message: { type: String, default: "" },
    dismissable: { type: Boolean, default: true }
  },
  computed: {
    type() {
      if (this.error) return "error";
      if (this.success) return "success";
      if (this.warning) return "warning";
      if (this.info) return "info";
      return "";
    },
    color() {
      return this.type;
    },
    computedIcon() {
      switch (this.type) {
        case "error":
          return "mdi-alert-circle";
        case "success":
          return `mdi-checkbox-marked-circle`;
        case "warning":
          return "mdi-alert";
        case "info":
          return "mdi-information";
        default: {
          return "";
        }
      }
    }
  },
  data: function() {
    return {
      active: false
    };
  },
  mounted() {
    this.$nextTick(() => this.show());
  },
  methods: {
    show() {
      this.active = true;
    },

    close() {
      this.$emit("closed");
      this.active = false;
    },

    dismiss() {
      if (this.dismissable) {
        this.close();
      }
    }
  }
};
</script>

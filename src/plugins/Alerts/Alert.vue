<template>
  <div :class="'notify-' + options.position" :style="{ width: width }" class="notify">
    <transition-group name="notify" tag="div" @enter="slideDown" @leave="slideUp">
      <div v-for="(item, key) in items" :key="item.text" class="notify-item">
        <div :class="item.options.itemClass">
          <button
            v-if="item.options.closeButtonClass"
            :class="item.options.closeButtonClass"
            type="button"
            @click="removeItem(key)"
          >
            <span class="mdi mdi-close-circle"></span>
          </button>
          <span v-if="item.options.iconClass" :class="item.options.iconClass"></span>
          <template>{{ item.text }}</template>
        </div>
      </div>
    </transition-group>
  </div>
</template>
<style lang="scss" scoped>
$icon-padding: 4rem;
$icon-font-size: 1.25rem;
$alert-padding: 1rem;
$center-width: 800px;
$indent-small: 0.4rem;
$indent-large: 1rem;

.notify {
  z-index: 1001;

  .notify-item {
    max-width: $center-width;
    margin: auto;
  }

  &.notify-top {
    top: 2rem !important;
  }
}
.notification {
  position: relative;
  padding: $icon-font-size $icon-padding $alert-padding $icon-padding;

  .alert_icon {
    position: absolute;
    left: $alert-padding;
    top: $alert-padding;
    font-size: $icon-font-size;
  }

  .alert_close {
    position: absolute;
    right: $alert-padding;
    top: $alert-padding;
    opacity: 1;
    margin-left: $icon-font-size;
    font-size: $icon-font-size;
  }

  .alert_close:not(:disabled):not(.disabled):focus,
  .alert_close:not(:disabled):not(.disabled):hover {
    opacity: 0.75;
  }

  button.alert_close {
    padding: 0;
    background-color: transparent;
    border: 0;
    appearance: none;
  }

  .alert_close:hover {
    color: rgba(white, 0.9);
    text-decoration: none;
  }

  [type="button"]:not(:disabled),
  button:not(:disabled) {
    cursor: pointer;
  }

  button {
    text-transform: none;
    margin: 0;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
    border-radius: 0;
  }
}

.notify-top,
.notify-top-right,
.notify-top-left,
.notify-bottom,
.notify-bottom-right,
.notify-bottom-left {
  position: fixed;
}

.notify-top {
  top: $indent-small;
  left: $indent-large;
  right: $indent-large;
}
.notify-bottom {
  bottom: $indent-small;
  left: $indent-large;
  right: $indent-large;
}
.notify-top-right {
  top: $indent-small;
  right: $indent-large;
}
.notify-top-left {
  top: $indent-small;
  left: $indent-large;
}
.notify-bottom-left {
  bottom: $indent-small;
  left: $indent-large;
}
.notify-bottom-right {
  bottom: $indent-small;
  right: $indent-large;
}

.notify-top,
.notify-top-right,
.notify-top-left {
  .notify-item:not(:last-child) {
    margin-bottom: $indent-small;
  }
}

.notify-bottom,
.notify-bottom-right,
.notify-bottom-left {
  .notify-item :not(:first-child) {
    margin-top: $indent-small;
  }
}
</style>
<script>
import Vue from "vue";
import Velocity from "velocity-animate";
export default {
  data() {
    return {
      types: {
        info: { itemClass: "alert--info", iconClass: "alert_icon mdi mdi-information" },
        error: { itemClass: "alert--error", iconClass: "alert_icon mdi mdi-alert-circle" },
        warning: { itemClass: "alert--warning", iconClass: "alert_icon mdi mdi-alert" },
        success: {
          itemClass: "alert--success",
          iconClass: "alert_icon mdi mdi-checkbox-marked-circle"
        }
      },
      options: {
        itemClass: "notification",
        duration: 400,
        visibility: 8000,
        position: "top",
        enter: "slideDown",
        leave: "slideUp",
        closeButtonClass: "alert_close",
        width: "300px"
      },
      items: {},
      idx: 0
    };
  },
  computed: {
    width() {
      if (this.options.position === "top" || this.options.position === "bottom") {
        return "auto";
      } else {
        return this.options.width;
      }
    }
  },
  methods: {
    setTypes(types) {
      this.types = types;
    },
    addItem(type, msg, options) {
      let defaultOptions = {
        iconClass: this.types[type].iconClass,
        itemClass: [this.options.itemClass, this.types[type].itemClass],
        visibility: this.options.visibility,
        closeButtonClass: this.options.closeButtonClass
      };
      let itemOptions = Object.assign({}, defaultOptions, options);
      // get idx
      let idx = this.idx;
      // check if this message is already shown
      for (let key in this.items) {
        /* ignore else */
        if (this.items.hasOwnProperty(key)) {
          if (this.items[key].text === msg) {
            return;
          }
        }
      }
      // add it to the queue (if it's not already there)
      Vue.set(this.items, this.idx, { type: type, text: msg, options: itemOptions });
      // increment key
      this.idx++;
      // remove item from array
      setTimeout(() => {
        this.removeItem(idx);
      }, this.options.duration + itemOptions.visibility);
    },
    slideDown(el) {
      Velocity(el, this.options.enter, { duration: this.options.duration });
    },
    slideUp(el, done) {
      Velocity(el, this.options.leave, { duration: this.options.duration, complete: done });
    },
    removeItem(index) {
      // console.log(index);
      Vue.delete(this.items, index);
    },
    removeAll() {
      this.items = {};
    }
  }
};
</script>

<template>
  <v-dialog persistent v-model="show" :max-width="dialogWidth">
    <template v-slot:activator="{ on }">
      <v-text-field
        v-bind="textFieldProps"
        :disabled="disabled"
        :loading="loading"
        :label="label"
        :value="formattedDatetime"
        v-on="on"
        readonly
        :hint="hint"
        :persistent-hint="persistentHint"
        :rules="rules"
      >
      </v-text-field>
    </template>

    <v-card class="dtp-tweak">
      <v-card-text class="px-0 py-0">
        <v-tabs fixed-tabs v-model="activeTab">
          <v-tab key="calendar">
            <v-icon>mdi-calendar</v-icon>
          </v-tab>
          <v-tab key="timer" :disabled="dateSelected">
            <v-icon>mdi-clock</v-icon>
          </v-tab>
          <v-tab-item key="calendar">
            <v-date-picker
              v-model="date"
              class="dtp-tweak"
              color="primary dtp-tweak"
              @input="showTimePicker"
              full-width
              first-day-of-week="1"
              :min="minDate"
              v-bind="datePickerProps"
            ></v-date-picker>
          </v-tab-item>
          <v-tab-item key="timer">
            <v-time-picker
              ref="timer"
              class="dtp-tweak"
              v-model="time"
              format="24hr"
              full-width
              color="primary"
              :allowed-minutes="allowedMinutes(5)"
              :min="minTime"
              v-bind="timePickerProps"
            ></v-time-picker>
          </v-tab-item>
        </v-tabs>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="warning" text @click.native="clearHandler">{{ clearText }}</v-btn>
        <v-btn text @click="cancelHandler">{{ cancelText }}</v-btn>
        <v-btn color="primary" text @click="okHandler">{{ okText }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { DateTime } from "luxon";
const DEFAULT_DATE = "";
const DEFAULT_TIME = "";
const DEFAULT_DATE_FORMAT = "yyyy-MM-dd";
const DEFAULT_TIME_FORMAT = "HH:mm";
const DEFAULT_DIALOG_WIDTH = 340;
const DEFAULT_CLEAR_TEXT = "CLEAR";
const DEFAULT_OK_TEXT = "OK";
const DEFAULT_CANCEL_TEXT = "CANCEL";
export default {
  name: "v-datetime-picker",
  model: {
    prop: "datetime",
    event: "input"
  },
  props: {
    datetime: { type: [DateTime, String], default: null },
    disabled: { type: Boolean },
    loading: { type: Boolean },
    label: { type: String, default: "" },
    hint: { type: String, default: "" },
    persistentHint: { type: Boolean, default: false },
    rules: { type: Array, default: () => [] },
    dialogWidth: { type: Number, default: DEFAULT_DIALOG_WIDTH },
    dateFormat: { type: String, default: DEFAULT_DATE_FORMAT },
    timeFormat: { type: String, default: DEFAULT_TIME_FORMAT },
    clearText: { type: String, default: DEFAULT_CLEAR_TEXT },
    okText: { type: String, default: DEFAULT_OK_TEXT },
    cancelText: { type: String, default: DEFAULT_CANCEL_TEXT },
    textFieldProps: { type: Object },
    datePickerProps: { type: Object },
    timePickerProps: { type: Object },
    min: { type: String }
  },
  data: function() {
    return {
      show: false,
      activeTab: 0,
      date: DEFAULT_DATE,
      time: DEFAULT_TIME
    };
  },
  mounted() {
    this.init();
  },
  computed: {
    formattedDatetime() {
      return this.selectedDatetime ? this.selectedDatetime.toFormat("dd/LL/yyyy HH:mm") : "";
    },
    selectedDatetime() {
      if (this.date && this.time) {
        return this.$util.dateTime(`${this.date} ${this.time}:00`);
      } else {
        return null;
      }
    },
    dateSelected() {
      return !this.date;
    },
    minDate() {
      if (this.min) return this.min.substring(0, 10);
      return null;
    },
    minTime() {
      if (this.min && this.date === this.minDate) return this.min.substring(11, 16);
      return null;
    }
  },
  methods: {
    init() {
      let currentDate = this.datetime;
      if (!this.datetime) {
        // currentDate = this.$util.nowString;
        // this.date = currentDate.substring(0, 10);
        // this.time = currentDate.substring(11, 16);
        return;
      }
      if (this.datetime instanceof DateTime) {
        this.date = currentDate.toFormat("yyyy-LL-dd");
        this.time = currentDate.toFormat("HH:mm");
      } else if (typeof this.datetime === "string" || this.datetime instanceof String) {
        // see https://stackoverflow.com/a/9436948
        currentDate = this.$util.dateTimeFromUTC(currentDate);
        this.date = currentDate.toFormat("yyyy-LL-dd");
        this.time = currentDate.toFormat("HH:mm");
      }
    },
    okHandler() {
      this.resetPicker();
      this.$emit("input", this.selectedDatetime);
    },
    clearHandler() {
      this.resetPicker();
      this.date = DEFAULT_DATE;
      this.time = DEFAULT_TIME;
      this.$emit("input", null);
    },
    cancelHandler() {
      this.resetPicker();
    },
    resetPicker() {
      this.show = false;
      this.activeTab = 0;
      if (this.$refs.timer) {
        this.$refs.timer.selectingHour = true;
      }
    },
    showTimePicker() {
      this.activeTab = 1;
    },
    allowedMinutes(delimiter) {
      let res = [];
      for (let i = 0; i <= 59; i += delimiter) res.push(i);
      return res;
    }
  },
  watch: {
    datetime: function() {
      this.init();
    }
  }
};
</script>

<style scoped lang="scss">
.dtp-tweak {
  border-radius: 0 !important;
}
</style>

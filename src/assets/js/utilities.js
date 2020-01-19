import { DateTime, Duration } from "luxon";

const UtilitiesHandler = {
  install(Vue) {
    /**
     * Utilities used in multiple components
     */
    Vue.prototype.$util = {
      /**
       * Check if valid email
       */
      isEmail: function(email) {
        return isEmail(email);
      },

      /**
       * Get a DateTime object.
       * @returns {DateTime}
       */
      dateTime(date) {
        return DateTime.fromFormat(date, "yyyy-LL-dd HH:mm:ss");
      },
      /**
       * Get a DateTime object.
       * @returns {DateTime}
       */
      dateTimeFromUTC(date) {
        return dateTimeFromUTC(date);
      },
      /**
       * Convert a DateTime to the UTC String representation.
       * @returns {String}
       */
      dateTimeToUTCString(dt) {
        return dt.toUTC().toFormat("yyyy-LL-dd HH:mm:ss");
      },
      /**
       * Convert a date String to the UTC String representation.
       * @returns {String}
       */
      dateStringToUTCString(date) {
        return this.dateTime(date)
          .toUTC()
          .toFormat("yyyy-LL-dd HH:mm:ss");
      },
      /**
       * Get the duration between two DateTime objects.
       * @returns {Duration}
       */
      duration(startDate, endDate) {
        return Duration.fromObject({
          milliseconds: endDate.toMillis() - startDate.toMillis()
        }).shiftTo("hours", "minutes");
      },
      /**
       * Get the current DateTime
       * @returns {DateTime}
       */
      get now() {
        return DateTime.local();
      },
      /**
       * Get the string representation of the current DateTime
       * @returns {String}
       */
      get nowString() {
        return this.now.toISO({ includeOffset: false });
      }
    };
  }
};

export default UtilitiesHandler;

export const dateTimeFromUTC = date =>
  DateTime.fromMillis(DateTime.fromFormat(date, "yyyy-LL-dd HH:mm:ss", { zone: "utc" }).ts);

export const isEmail = email => {
  // eslint-disable-next-line no-useless-escape
  let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
};

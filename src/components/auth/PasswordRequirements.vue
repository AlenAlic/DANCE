<template>
  <div class="password-requirements">
    <div class="mb-2">{{ $t("password_requirements.title") }}</div>
    <ul :class="checkPasswordRequirements('all_requirements')">
      <li :class="checkPasswordRequirements('minimum_character_count')">
        {{ $t("password_requirements.minimum_character_count", { num: 16 }) }}
      </li>
      <li :class="checkPasswordRequirements('lowercase_letter')">
        {{ $t("password_requirements.lowercase_letter") }}
      </li>
      <li :class="checkPasswordRequirements('uppercase_letter')">
        {{ $t("password_requirements.uppercase_letter") }}
      </li>
      <li :class="checkPasswordRequirements('number')">
        {{ $t("password_requirements.number") }}
      </li>
      <li :class="checkPasswordRequirements('match')">
        {{ $t("password_requirements.match") }}
      </li>
      <li :class="checkPasswordRequirements('not_old_password')" v-if="useOldPassword">
        {{ $t("password_requirements.not_old_password") }}
      </li>
    </ul>
  </div>
</template>

<script>
const MINIMUM_CHARACTER_COUNT = "minimum_character_count";
const LOWERCASE_LETTER = "lowercase_letter";
const UPPERCASE_LETTER = "uppercase_letter";
const NUMBER = "number";
const MATCH = "match";
const NOT_OLD_PASSWORD = "not_old_password";
const ALL_REQUIREMENTS = "all_requirements";

const CONDITION_MET = "condition_met";

const MINIMUM_PASSWORD_LENGTH = 16;

export default {
  name: "PasswordRequirements",
  props: {
    password: String,
    repeat_password: String,
    old_password: String,
    useOldPassword: { type: Boolean, default: false }
  },
  watch: {
    password: function() {
      return this.$emit("requirements", this.checkPasswordRequirements(ALL_REQUIREMENTS));
    },
    repeat_password: function() {
      return this.$emit("requirements", this.checkPasswordRequirements(ALL_REQUIREMENTS));
    },
    old_password: function() {
      return this.$emit("requirements", this.checkPasswordRequirements(ALL_REQUIREMENTS));
    }
  },
  methods: {
    checkPasswordRequirements: function(requirement) {
      let re;
      switch (requirement) {
        case MINIMUM_CHARACTER_COUNT:
          return this.password.length >= MINIMUM_PASSWORD_LENGTH ? CONDITION_MET : "";
        case LOWERCASE_LETTER:
          re = new RegExp("(?=.*[a-z])");
          return re.test(this.password) ? CONDITION_MET : "";
        case UPPERCASE_LETTER:
          re = new RegExp("(?=.*[A-Z])");
          return re.test(this.password) ? CONDITION_MET : "";
        case NUMBER:
          re = new RegExp("(?=.*[0-9])");
          return re.test(this.password) ? CONDITION_MET : "";
        case MATCH:
          return this.password === this.repeat_password && this.password !== ""
            ? CONDITION_MET
            : "";
        case NOT_OLD_PASSWORD:
          return this.password !== this.old_password &&
            this.password !== "" &&
            this.old_password !== ""
            ? CONDITION_MET
            : "";
        case ALL_REQUIREMENTS:
          re = new RegExp("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])");
          if (this.useOldPassword) {
            return (
              re.test(this.password) &&
              this.password.length >= MINIMUM_PASSWORD_LENGTH &&
              this.password === this.repeat_password &&
              this.password !== this.old_password &&
              this.old_password !== ""
            );
          } else {
            return (
              re.test(this.password) &&
              this.password.length >= MINIMUM_PASSWORD_LENGTH &&
              this.password === this.repeat_password
            );
          }
        default:
          return "";
      }
    }
  }
};
</script>

<style scoped lang="scss">
@import "../../assets/css/general/settings";
.password-requirements {
  background-color: #f2f3f4;
  padding: 1rem;
  margin: 1rem 0;
}
ul {
  list-style-type: none;
  margin: 0.5rem 0;
  padding: 0;

  li {
    padding-left: 0.25rem;
    clear: both;

    &.condition_met {
      color: $success;
    }

    &:before {
      font-family: "Material Design Icons";
      font-size: 1rem;
      content: "\F5E0";
      float: left;
      width: 1rem;
      margin-right: 1rem;
    }
  }
}
</style>

export const TOURNAMENT_OFFICE_MANAGER = 0;
export const FLOOR_MANAGER = 2;
export const ADJUDICATOR = 4;
export const PRESENTER = 10;

export const BALLROOM = "Ballroom";
export const STANDARD = "Standard";
export const LATIN = "Latin";
export const JUNIOREN = "Junioren";
export const SENIOREN = "Senioren";

export const XTDS = "xTDS";
export const ODK = "ODK";
export const SOND = "SOND";

export const LEAD = "Lead";
export const FOLLOW = "Follow";

export const TEST = "TEST";

export const ADJUDICATION_LEAD = "lead";
export const ADJUDICATION_FOLLOW = "follow";
export const ADJUDICATION_BOTH = "both";

export const SINGLE_PARTNER = "single_partner";
export const RANDOM_SINGLE_PARTNER = "random_single_partner";
export const CHANGE_PER_ROUND = "change_per_round";
export const CHANGE_PER_DANCE = "change_per_dance";

export const QUALIFICATION = "qualification";
export const GENERAL_LOOK = "general_look";
export const FIRST_ROUND = "first_round";
export const RE_DANCE = "re_dance";
export const INTERMEDIATE_ROUND = "intermediate_round";
export const EIGHT_FINAL = "eight_final";
export const QUARTER_FINAL = "quarter_final";
export const SEMI_FINAL = "semi_final";
export const FINAL = "final";

export const HEATS_BY_STARTING_NUMBER = "heats_by_starting_number";
export const HEATS_BY_DANCE = "heats_by_dance";
export const QUALIFIED_STARTS = "qualified_starts";
export const NO_RE_DANCE = "no_re_dance";
export const ADJUDICATORS = "adjudicators";
export const ADJUDICATION_SHEETS = "adjudication_sheets";
export const PLACINGS_AFTER_ROUND = "placings_after_round";
export const EVALUATION_OF_FINAL = "final_evaluation";
export const COMPETITION_RESULT = "tournament_result";
export const RANKING_REPORT = "ranking_report";

export const RELOAD_TIMER_SHORT = 2000;
export const RELOAD_TIMER = 3000;
export const RELOAD_TIMER_LONG = 5000;

const ConstantsHandler = {
  install(Vue) {
    /**
     * Constants
     */
    Vue.prototype.$constants = {
      get TOURNAMENT_OFFICE_MANAGER() {
        return TOURNAMENT_OFFICE_MANAGER;
      },
      get FLOOR_MANAGER() {
        return FLOOR_MANAGER;
      },
      get ADJUDICATOR() {
        return ADJUDICATOR;
      },
      get PRESENTER() {
        return PRESENTER;
      },
      get BALLROOM() {
        return BALLROOM;
      },
      get STANDARD() {
        return STANDARD;
      },
      get LATIN() {
        return LATIN;
      },
      get XTDS() {
        return XTDS;
      },
      get ODK() {
        return ODK;
      },
      get SOND() {
        return SOND;
      },
      get JUNIOREN() {
        return JUNIOREN;
      },
      get SENIOREN() {
        return SENIOREN;
      },
      get LEAD() {
        return LEAD;
      },
      get FOLLOW() {
        return FOLLOW;
      },
      get TEST() {
        return TEST;
      },
      get ADJUDICATION_LEAD() {
        return ADJUDICATION_LEAD;
      },
      get ADJUDICATION_FOLLOW() {
        return ADJUDICATION_FOLLOW;
      },
      get ADJUDICATION_BOTH() {
        return ADJUDICATION_BOTH;
      },
      get SINGLE_PARTNER() {
        return SINGLE_PARTNER;
      },
      get RANDOM_SINGLE_PARTNER() {
        return RANDOM_SINGLE_PARTNER;
      },
      get CHANGE_PER_ROUND() {
        return CHANGE_PER_ROUND;
      },
      get CHANGE_PER_DANCE() {
        return CHANGE_PER_DANCE;
      },
      get GENERAL_LOOK() {
        return GENERAL_LOOK;
      },
      get QUALIFICATION() {
        return QUALIFICATION;
      },
      get RE_DANCE() {
        return RE_DANCE;
      },
      get SEMI_FINAL() {
        return SEMI_FINAL;
      },
      get FINAL() {
        return FINAL;
      },
      get HEATS_BY_STARTING_NUMBER() {
        return HEATS_BY_STARTING_NUMBER;
      },
      get HEATS_BY_DANCE() {
        return HEATS_BY_DANCE;
      },
      get QUALIFIED_STARTS() {
        return QUALIFIED_STARTS;
      },
      get NO_RE_DANCE() {
        return NO_RE_DANCE;
      },
      get ADJUDICATORS() {
        return ADJUDICATORS;
      },
      get ADJUDICATION_SHEETS() {
        return ADJUDICATION_SHEETS;
      },
      get PLACINGS_AFTER_ROUND() {
        return PLACINGS_AFTER_ROUND;
      },
      get EVALUATION_OF_FINAL() {
        return EVALUATION_OF_FINAL;
      },
      get COMPETITION_RESULT() {
        return COMPETITION_RESULT;
      },
      get RANKING_REPORT() {
        return RANKING_REPORT;
      }
    };
  }
};

export default ConstantsHandler;

import i18n from "@/languages";
import { isEmail } from "@/assets/js/utilities";

const FormRulesHandler = {
  install(Vue) {
    Vue.prototype.$form = {
      get fieldRequired() {
        return fieldRequired;
      },
      get passwordRequired() {
        return passwordRequired;
      },
      get fieldIsEmail() {
        return fieldIsEmail;
      },
      min(f) {
        return v => min(v, f);
      },
      max(f) {
        return v => max(v, f);
      },
      minCharacterCount(f) {
        return v => minCharacterCount(v, f);
      },
      maxCharacterCount(f) {
        return v => maxCharacterCount(v, f);
      },
      noExistingAttribute(l, a) {
        return v => noExistingAttribute(v, l, a);
      }
    };
  }
};

export default FormRulesHandler;

export const fieldRequired = v => !!v || i18n.t("form_validation.errors.required");
export const fieldIsEmail = v => isEmail(v) || i18n.t("auth.errors.valid_email");
export const passwordRequired = v => !!v || i18n.t("auth.errors.password_required");
export const min = (v, o) => v >= o || `Must be greater than ${o}`;
export const max = (v, o) => v <= o || `Must be smaller than ${o}`;
export const minCharacterCount = (v, o) => v.length >= o || `Must have at least ${o} characters`;
export const maxCharacterCount = (v, o) => v.length <= o || `Cannot have more than ${o} characters`;
export const noExistingAttribute = (v, l, a) =>
  l.length === 0 || i18n.t("form_validation.errors.no_existing_attribute", { attribute: a });

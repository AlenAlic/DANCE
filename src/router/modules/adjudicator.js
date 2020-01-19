import { ADJUDICATOR } from "@/constants";

const RouteWrapper = () => import("@/components/general/page_wrappers/RouteWrapper");
const Dashboard = () => import("@/pages/adjudicator/Dashboard");
const Dance = () => import("@/pages/adjudicator/Dance");

const adjudicatorPages = {
  path: "/adjudicator",
  component: RouteWrapper,
  meta: {
    auth: true,
    access: ADJUDICATOR
  },
  children: [
    {
      path: "dashboard",
      name: "adjudicator.dashboard",
      component: Dashboard
    },
    {
      path: "round/:round_id/dance/:dance_id",
      name: "adjudicator.dance",
      component: Dance
    }
  ]
};
export default adjudicatorPages;

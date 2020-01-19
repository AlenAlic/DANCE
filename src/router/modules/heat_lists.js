const RouteWrapper = () => import("@/components/general/page_wrappers/RouteWrapper");
const HeatLists = () => import("@/pages/public/heat_lists/HeatLists");
const CompetitionHeatLists = () => import("@/pages/public/heat_lists/CompetitionHeatLists");

const heatListsPages = {
  path: "/heat_lists",
  component: RouteWrapper,
  redirect: { name: "heat_lists" },
  children: [
    {
      path: "",
      name: "heat_lists",
      component: HeatLists
    },
    {
      path: ":competition_id",
      name: "heat_lists.competition",
      component: CompetitionHeatLists
    }
  ]
};
export default heatListsPages;

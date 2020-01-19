const RouteWrapper = () => import("@/components/general/page_wrappers/RouteWrapper");
const ResultsList = () => import("@/pages/public/results/ResultsList");
const CompetitionResults = () => import("@/pages/public/results/CompetitionResults");

const resultsPages = {
  path: "/results",
  component: RouteWrapper,
  redirect: { name: "results" },
  children: [
    {
      path: "",
      name: "results",
      component: ResultsList
    },
    {
      path: ":competition_id",
      name: "results.competition",
      component: CompetitionResults
    }
  ]
};
export default resultsPages;

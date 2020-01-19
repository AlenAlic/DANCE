const RouteWrapper = () => import("@/components/general/page_wrappers/RouteWrapper");
const StartingLists = () => import("@/pages/public/starting_lists/StartingLists");
const CompetitionStartingLists = () =>
  import("@/pages/public/starting_lists/CompetitionStartingLists");

const startingListsPages = {
  path: "/starting_lists",
  component: RouteWrapper,
  redirect: { name: "starting_lists" },
  children: [
    {
      path: "",
      name: "starting_lists",
      component: StartingLists
    },
    {
      path: ":competition_id",
      name: "starting_lists.competition",
      component: CompetitionStartingLists
    }
  ]
};
export default startingListsPages;

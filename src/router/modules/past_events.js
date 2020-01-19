const RouteWrapper = () => import("@/components/general/page_wrappers/RouteWrapper");
const EventsList = () => import("@/pages/public/past_events/EventsList");
const EventResultsList = () => import("@/pages/public/past_events/EventResultsList");
const EventCompetitionResults = () => import("@/pages/public/past_events/EventCompetitionResults");

const pastEventPages = {
  path: "/events",
  component: RouteWrapper,
  redirect: { name: "events" },
  children: [
    {
      path: "",
      name: "events",
      component: EventsList
    },
    {
      path: ":event_id",
      component: RouteWrapper,
      redirect: { name: "events.results" },
      children: [
        {
          path: "",
          name: "events.results",
          component: EventResultsList
        },
        {
          path: "result/:event_result_id",
          name: "events.results.result",
          component: EventCompetitionResults
        }
      ]
    }
  ]
};
export default pastEventPages;

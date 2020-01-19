import { TOURNAMENT_OFFICE_MANAGER } from "@/constants";

const ContainerWrapper = () => import("@/components/general/page_wrappers/ContainerWrapper");
const RouteWrapper = () => import("@/components/general/page_wrappers/RouteWrapper");
const Dashboard = () => import("@/pages/tournament_office/Dashboard");
const NewEvent = () => import("@/pages/tournament_office/event/NewEvent");
const Setup = () => import("@/pages/tournament_office/event/Setup");
const Dances = () => import("@/pages/tournament_office/event/Dances");
const Disciplines = () => import("@/pages/tournament_office/event/Disciplines");
const Classes = () => import("@/pages/tournament_office/event/Classes");
const Adjudicators = () => import("@/pages/tournament_office/event/Adjudicators");
const Assignments = () => import("@/pages/tournament_office/event/Assignments");
const Dancers = () => import("@/pages/tournament_office/event/Dancers");
const Couples = () => import("@/pages/tournament_office/event/Couples");
const FinalResults = () => import("@/pages/tournament_office/event/FinalResults");
const Competition = () => import("@/pages/tournament_office/competition/Competition");
const Progress = () => import("@/pages/tournament_office/round/Progress");
const Reports = () => import("@/pages/tournament_office/round/Reports");
const FloorManagement = () => import("@/pages/tournament_office/round/FloorManagement");
const Adjudication = () => import("@/pages/tournament_office/round/Adjudication");

const tournamentOfficePages = {
  path: "/tournament_office",
  component: ContainerWrapper,
  meta: {
    auth: true,
    access: TOURNAMENT_OFFICE_MANAGER
  },
  children: [
    {
      path: "dashboard",
      name: "tournament_office.dashboard",
      component: Dashboard
    },
    {
      path: "event",
      name: "tournament_office.event",
      component: RouteWrapper,
      redirect: { name: "tournament_office.event.new_event" },
      meta: {
        event: true
      },
      children: [
        {
          path: "new_event",
          name: "tournament_office.event.new_event",
          component: NewEvent
        },
        {
          path: "setup",
          name: "tournament_office.event.setup",
          component: Setup
        },
        {
          path: "dances",
          name: "tournament_office.event.dances",
          component: Dances
        },
        {
          path: "disciplines",
          name: "tournament_office.event.disciplines",
          component: Disciplines
        },
        {
          path: "classes",
          name: "tournament_office.event.classes",
          component: Classes
        },
        {
          path: "adjudicators",
          name: "tournament_office.event.adjudicators",
          component: Adjudicators
        },
        {
          path: "assignments",
          name: "tournament_office.event.assignments",
          component: Assignments
        },
        {
          path: "dancers",
          name: "tournament_office.event.dancers",
          component: Dancers
        },
        {
          path: "couples",
          name: "tournament_office.event.couples",
          component: Couples
        },
        {
          path: "results",
          name: "tournament_office.event.results",
          component: FinalResults
        }
      ]
    },
    {
      path: "competition/:competition_id",
      name: "tournament_office.competition",
      component: Competition
    },
    {
      path: "competition/:competition_id/round/:round_id",
      name: "tournament_office.round",
      component: RouteWrapper,
      redirect: { name: "tournament_office.round.progress" },
      meta: {
        event: true
      },
      children: [
        {
          path: "progress",
          name: "tournament_office.round.progress",
          component: Progress
        },
        {
          path: "reports",
          name: "tournament_office.round.reports",
          component: Reports
        },
        {
          path: "floor_management",
          name: "tournament_office.round.floor_management",
          component: FloorManagement
        },
        {
          path: "adjudication",
          name: "tournament_office.round.adjudication",
          component: Adjudication
        }
      ]
    }
  ]
};
export default tournamentOfficePages;

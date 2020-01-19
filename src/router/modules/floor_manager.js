import { FLOOR_MANAGER } from "@/constants";

const RouteWrapper = () => import("@/components/general/page_wrappers/RouteWrapper");
const Dashboard = () => import("@/pages/floor_manager/Dashboard");
const FloorManagerCompetition = () => import("@/pages/floor_manager/FloorManagerCompetition");

const floorManagerPages = {
  path: "/floor_manager",
  component: RouteWrapper,
  meta: {
    auth: true,
    access: FLOOR_MANAGER
  },
  children: [
    {
      path: "dashboard",
      name: "floor_manager.dashboard",
      component: Dashboard
    },
    {
      path: ":competition_id",
      name: "floor_manager.competition",
      component: FloorManagerCompetition
    }
  ]
};
export default floorManagerPages;

import { PRESENTER } from "@/constants";

const Dashboard = () => import("@/pages/presenter/Dashboard");

const presenterPages = {
  path: "/presenter",
  name: "presenter.dashboard",
  component: Dashboard,
  meta: {
    auth: true,
    access: PRESENTER
  }
};
export default presenterPages;

import SignUp from "./SignUp";
//import VerifyCornellStatus from "./VerifyCornellStatus";
//import VerifyOrg from "./VerifyOrg";
//import VerifyDone from "./VerifyDone";
import MyEvents from "./MyEvents";
import Profile from "./Profile";
import Login from "./Login";
import ChangePassword from "./ChangePassword";
import ChangeOrgEmail from "./ChangeOrgEmail";
import Landing from "./Landing";

export default {
  auth: {
    logout: { route: "/logout/", component: null },
    profile: { route: "/profile/", component: Profile },
    changePassword: { route: "/change_password/", component: ChangePassword },
    changeOrgEmail: { route: "/change_org_email/", component: ChangeOrgEmail },
    myEvents: { route: "/events/:id(\\d+)", component: MyEvents },
    myEventsDefault: { route: "/events/", component: MyEvents }
    //onboarding
    //describeTags: { route: "/app/describe", component: DescribeOrg }
  },
  noAuth: {
    home: { route: "/", component: Landing },
    signup: { route: "/signup/", component: SignUp },
    login: { route: "/login/", component: Login }
  }
  //verifyCornellStatus: { route: "/verifyCornellStatus/", component: VerifyCornellStatus },
  //verifyOrg: { route: "/verifyOrg", component: VerifyOrg },
  //verifyDone: { route: "/verifyDone", component: VerifyDone }
};

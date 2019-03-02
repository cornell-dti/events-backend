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
		logout: { route: "/app/logout/", component: null },
		profile: { route: "/app/profile/", component: Profile },
		changePassword: { route: "/app/change_password/", component: ChangePassword },
		changeOrgEmail: { route: "/app/change_org_email/", component: ChangeOrgEmail },
		myEvents: { route: "/app/events/", component: MyEvents },
		//onboarding
	},
	noAuth: {
		home: { route: "/app/", component: Landing },
		signup: { route: "/app/signup/", component: SignUp },
		login: { route: "/app/login/", component: Login }
	}	
	//verifyCornellStatus: { route: "/app/verifyCornellStatus/", component: VerifyCornellStatus },
	//verifyOrg: { route: "/app/verifyOrg", component: VerifyOrg },
	//verifyDone: { route: "/app/verifyDone", component: VerifyDone }
};
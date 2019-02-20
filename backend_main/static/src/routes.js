import CreateOrg from "./CreateOrg";
import VerifyCornellStatus from "./VerifyCornellStatus";
import VerifyOrg from "./VerifyOrg";
import VerifyDone from "./VerifyDone";
import MyEvents from "./MyEvents";
import Profile from "./Profile";
import Login from "./Login";
import Settings from "./Settings";

export default {
	login: { route: "/accounts/login/", component: Login },
	logout: { route: "/accounts/logout/", component: null },
	profile: { route: "/profile", component: Profile },
	settings: { route: "/settings/", component: Settings },
	myEvents: { route: "/post/event/", component: MyEvents },
	//onboarding
	createOrg: { route: "/signup/", component: CreateOrg },
	verifyCornellStatus: { route: "/verifyCornellStatus/", component: VerifyCornellStatus },
	verifyOrg: { route: "/verifyOrg", component: VerifyOrg },
	verifyDone: { route: "/verifyDone", component: VerifyDone }
};
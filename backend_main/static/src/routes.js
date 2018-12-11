import CreateOrg from "./CreateOrg";
import VerifyCornellStatus from "./VerifyCornellStatus";
import VerifyOrg from "./VerifyOrg";
import VerifyDone from "./VerifyDone";
import MyEvents from "./MyEvents";
import Profile from "./Profile";
import Login from "./Login";
import Settings from "./Settings";

export default {
	login: { route: "/app/accounts/login/", component: Login },
	logout: { route: "/app/accounts/logout/", component: null },
	profile: { route: "/app/profile", component: Profile },
	settings: { route: "/app/settings/", component: Settings },
	myEvents: { route: "/app/post/event/", component: MyEvents },
	//onboarding
	createOrg: { route: "/app/signup/", component: CreateOrg },
	verifyCornellStatus: { route: "/app/verifyCornellStatus/", component: VerifyCornellStatus },
	verifyOrg: { route: "/app/verifyOrg", component: VerifyOrg },
	verifyDone: { route: "/app/verifyDone", component: VerifyDone }
};
import CreateOrg from "./CreateOrg";
import VerifyCornellStatus from "./VerifyCornellStatus";
import VerifyOrg from "./VerifyOrg";
import VerifyDone from "./VerifyDone";
import MyEvents from "./MyEvents";
import Profile from "./Profile";

export default {
	profile: { route: "/app/profile", component: Profile },
	myEvents: { route: "/app/myEvents", component: MyEvents },
	//onboarding
	createOrg: { route: "/app/createOrg", component: CreateOrg },
	verifyCornellStatus: { route: "/app/verifyCornellStatus", component: VerifyCornellStatus },
	verifyOrg: { route: "/app/verifyOrg", component: VerifyOrg },
	verifyDone: { route: "/app/verifyDone", component: VerifyDone }
};
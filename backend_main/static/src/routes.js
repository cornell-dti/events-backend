import CreateOrg from "./CreateOrg";
import VerifyCornellStatus from "./VerifyCornellStatus";
import VerifyOrg from "./VerifyOrg";
import VerifyDone from "./VerifyDone";
import MyEvents from "./MyEvents";
import Profile from "./Profile";

export default {
	profile: {route: "/profile", component: Profile},
	myEvents: {route: "/myEvents", component: MyEvents},
	//onboarding
	createOrg: {route: "/createOrg", component: CreateOrg},
	verifyCornellStatus: {route: "/verifyCornellStatus", component: VerifyCornellStatus},
	verifyOrg: {route: "/verifyOrg", component: VerifyOrg},
	verifyDone: {route: "/verifyDone", component: VerifyDone}
};
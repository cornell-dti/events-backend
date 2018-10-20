export const SET_ORG_NAME = "SET_ORG_NAME";
export const SET_ORG_EMAIL = "SET_ORG_EMAIL";
export const SET_PASSWORD = "SET_PASSWORD";
export const SET_NAME = "SET_NAME";
export const SET_NET_ID = "SET_NET_ID";
export const SET_FB = "SET_FB";
export const SET_WEBSITE = "SET_WEBSITE";

const initState = {
	orgName: "",
	orgEmail: "admin-david", //TODO remove
	password: "admin-david", //TODO remove
	name: "",
	netid: "",
	facebookLink: "",
	website: ""
};

/**
 *
 * @param {{orgName: string, orgEmail: string, password: string, name: string, netid: string, facebookLink: string, website: string}} state
 * @param {{type: string, value: string}} action
 * @returns {{orgName: string, orgEmail: string, password: string, name: string, netid: string, facebookLink: string, website: string}} New state
 */
export function user(state = initState, action)
{
	switch (action.type)
	{
		case SET_ORG_NAME:
			return {...state, orgName: action.value};
		case SET_ORG_EMAIL:
			return {...state, orgEmail: action.value};
		case SET_PASSWORD:
			return {...state, password: action.value};
		case SET_NAME:
			return {...state, name: action.value};
		case SET_NET_ID:
			return {...state, netid: action.value};
		case SET_FB:
			return {...state, facebookLink: action.value};
		case SET_WEBSITE:
			return {...state, website: action.value};
		default:
			return state;
	}
}
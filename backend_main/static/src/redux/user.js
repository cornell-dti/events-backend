export const SET_ORG_NAME = "SET_ORG_NAME";
export const SET_ORG_EMAIL = "SET_ORG_EMAIL";
export const SET_NAME = "SET_NAME";
export const SET_NET_ID = "SET_NET_ID";

const initState = {
	orgName: "",
	orgEmail: "",
	name: "",
	netid: ""
};

/**
 *
 * @param {{orgName: string, orgEmail: string, name: string, netid: string}} state
 * @param {{type: string, value: string}} action
 * @returns {{orgName: string, orgEmail: string, name: string, netid: string}} New state
 */
export function user(state = initState, action)
{
	switch (action.type)
	{
		case SET_ORG_NAME:
			return {...state, orgName: action.value};
		case SET_ORG_EMAIL:
			return {...state, orgEmail: action.value};
		case SET_NAME:
			return {...state, name: action.value};
		case SET_NET_ID:
			return {...state, netid: action.value};
		default:
			return state;
	}
}
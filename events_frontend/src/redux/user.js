export const SET_ORG_NAME = "SET_ORG_NAME";
export const SET_ORG_EMAIL = "SET_ORG_EMAIL";
export const SET_ORG_BIO = "SET_ORG_BIO";
export const SET_ORG_WEBSITE = "SET_ORG_WEBSITE";

const initState = {
  orgName: "",
  orgEmail: "",
  orgBio: "",
  orgWebsite: ""
};

/**
 *
 * @param {{orgName: string, orgEmail: string, name: string, netid: string}} state
 * @param {{type: string, value: string}} action
 * @returns {{orgName: string, orgEmail: string, name: string, netid: string}} New state
 */
export function user(state = initState, action) {
  switch (action.type) {
    case SET_ORG_NAME:
      return { ...state, orgName: action.value };
    case SET_ORG_EMAIL:
      return { ...state, orgEmail: action.value };
    case SET_ORG_BIO:
      return { ...state, orgBio: action.value };
    case SET_ORG_WEBSITE:
      return { ...state, orgWebsite: action.value };
    default:
      return state;
  }
}

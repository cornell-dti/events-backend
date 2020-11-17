export const SET_EVENT_NAME = "SET_EVENT_NAME";
export const SET_EVENT_DESCRIPTION = "SET_EVENT_DESCRIPTION";
export const SET_EVENT_START_DATE = "SET_EVENT_START_DATE";
export const SET_EVENT_END_DATE = "SET_EVENT_END_DATE";
export const SET_EVENT_PUBLIC = "SET_EVENT_PUBLIC";
export const SET_EVENT_ROOM = "SET_EVENT_ROOM";
export const SET_EVENT_LOCATION = "SET_EVENT_LOCATION";

const initState = {
    eventName: "",
    eventDesc: "",
    startDate: "",
    endDate: "",
    isPublic: true,
    room: "",
    location: ""
};

/**
 *
 * @param {{eventName: string, eventDesc: string, startDate: string, endDate: string, isPublic: boolean, room: string, location: string}} state
 * @param {{type: string, value: string}} action
 * @returns {{eventName: string, eventDesc: string, startDate: string, endDate: string, isPublic: boolean, room: string, location: string}} New state
 */
export function event(state = initState, action) {
    switch (action.type) {
        case SET_EVENT_NAME:
            return { ...state, eventName: action.value };
        case SET_EVENT_DESCRIPTION:
            return { ...state, eventDesc: action.value };
        case SET_EVENT_START_DATE:
            return { ...state, startDate: action.value };
        case SET_EVENT_END_DATE:
            return { ...state, endDate: action.value };
        case SET_EVENT_PUBLIC:
            return { ...state, isPublic: action.value };
        case SET_EVENT_ROOM:
            return { ...state, room: action.value };
        case SET_EVENT_LOCATION:
            return { ...state, location: action.value };
        default:
            return state;
    }
}

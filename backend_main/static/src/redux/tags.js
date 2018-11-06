import {GET_TAGS} from "./dataService";

export const ADD_TAG = "ADD_TAG";

const initState = {
	tags: []
};

export function tags(state = initState, action)
{
	switch (action.type)
	{
		case ADD_TAG:
			if (state.tags.includes(action.tag))
				return state;
			state.tags.push(action.tag);
			return state;
		case `${GET_TAGS}_RECEIVED`:
			console.log(JSON.stringify(action.data));
			if (Array.isArray(action.data))
				return {...state, tags: action.data};
	}
	return state;
}
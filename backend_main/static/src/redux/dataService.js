export const GET_TAGS = "GET_TAGS";

const DATABASE = "https://cuevents-app.herokuapp.com/app";
export const dataService = store => next => action =>
{
	next(action);
	switch (action.type)
	{
		case GET_TAGS:
			fetchFromURL(`${DATABASE}/tag/all/`, next, GET_TAGS);
			break;
	}
};

function fetchFromURL(url, next, actionType)
{
	fetch(url)
		.then(res => res.json())
		.then(json => next({type: `${actionType}_RECEIVED`, data: json}))
		.catch(err => next({type: `${actionType}_ERROR`, error: err}))
}
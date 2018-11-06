import {combineReducers} from "redux";
import {user} from "./user";
import {tags} from "./tags";

export default combineReducers({user, tags});
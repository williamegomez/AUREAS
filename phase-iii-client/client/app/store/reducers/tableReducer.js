import { CHANGE_SELECTION } from '../actions/action-types';

const initialState = {
  selected: {}
};

function tableReducer(state = initialState, action) {
  if (action.type === CHANGE_SELECTION) {
    return { ...state, selected: { ...state.selected, ...action.payload } };
  }
  return state;
}

export default tableReducer;

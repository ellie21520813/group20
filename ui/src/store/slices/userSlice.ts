import { createAction, createSlice, PrepareAction } from '@reduxjs/toolkit';
import { UserModel } from '@app/domain/UserModel';
import { persistUser, readUser } from '@app/services/localStorage.service';

export interface UserState {
  user: UserModel | null;
}

const initialState: UserState = {
  user: readUser(),
};

export const setUser = createAction<PrepareAction<UserModel>>('user/setUser', (newUser) => {
  const user: UserModel = {
    id: newUser.id,
    userName: newUser.username,
    email: {
      name: newUser.email,
      verified: newUser.email_verified,
    },
    firstName: newUser.first_name,
    lastName: newUser.last_name,
    sex: newUser.sex == 0 ? 'female' : 'male',
    birthday: newUser.birthday,
    phone: {
      number: newUser.phone,
      verified: newUser.phone_verified,
    },
    lang: newUser.language,
    imgUrl: newUser.avatar,
  };
  persistUser(user);

  return {
    payload: user,
  };
});

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(setUser, (state, action) => {
      state.user = action.payload;
    });
  },
});

export default userSlice.reducer;

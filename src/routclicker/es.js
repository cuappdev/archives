// @flow
import React from 'react';
import { Route, IndexRoute, Redirect } from 'react-router';

import App from './components/App';
import Home from './components/Home';
import SignIn from './components/SignIn';
import Profile from './components/Profile';
import LectureProfessor from './components/lecture/LectureProfessor';
import LectureStudent from './components/lecture/LectureStudent';
import Page404 from './components/Page404'

const routes: React.Element<any> = (
  <Route path='/' component={App}>
    <IndexRoute component={Home} />
    <Route path='/signin' component={SignIn} />
    <Route path='/profile' component={Profile} />
    <Route path='/professor' component={LectureProfessor} />
    <Route path='/student' component={LectureStudent} />
    <Redirect from='/lecture' to='/student' />
    <Route path='*' exact={true} component={Page404} />
  </Route>
);

export default routes;

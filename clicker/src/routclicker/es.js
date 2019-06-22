// @flow
import React from 'react';
import { Route, IndexRoute, Redirect } from 'react-router';

import App from './components/App';
import Home from './components/Home';
import SignIn from './components/SignIn';
import Profile from './components/Profile';
import ProfessorDashboard from './components/dashboard/ProfessorDashboard';
import LectureStudent from './components/lecture/LectureStudent';
import LecturePage from './components/lecture/LecturePage';
import Page404 from './components/Page404'

const routes: React.Element<any> = (
  <Route path='/' component={App}>
    <IndexRoute component={Home} />
    <Route path='/signin' component={SignIn} />
    <Route path='/profile' component={Profile} />
    <Route path='/professor' component={ProfessorDashboard} />
    <Route path='/student' component={LectureStudent} />
    <Redirect from='/dashboard' to='/professor' />
    <Route path='/lecture/create' component={LecturePage} />
    <Route path='*' exact={true} component={Page404} />
  </Route>
);

export default routes;

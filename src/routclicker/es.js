// @flow
import React from 'React';
import { Route, IndexRoute, Redirect } from 'react-router';

import App from './components/App';
import Home from './components/Home';
import SignIn from './components/SignIn';
import Profile from './components/Profile';
import LectureProfessor from './components/lecture/LectureProfessor';
import LectureStudent from './components/lecture/LectureStudent';

const routes: React.Element<any> = (
  <Route path='/' component={App}>
    <IndexRoute component={Home} />
    <Route path='/signin' component={SignIn} />
    <Route path='/profile' component={Profile} />
    <Route path='/professor' component={LectureProfessor} />
    <Route path='/student' component={LectureStudent} />
    <Redirect from='/lecture' to='/student' />
  </Route>
);

export default routes;

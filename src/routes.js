import React from 'react';
import { Route, IndexRoute, Redirect } from 'react-router';

/* Routes */
import PageLayout from './components/PageLayout';
import Home from './components/Home';
import Lecture from './components/Lecture';

function requireAuth(nextState, replace) {
  if (true) {
    replace({ pathname: '/' });
  }
}

export default (
  <Route path='/' component={PageLayout}>
    <IndexRoute component={Home} />
    <Route path='lecture/student' component={() => (<Lecture userType='students' />)} />
    <Route path='lecture/professor' component={() => (<Lecture userType='professors' />)} onEnter={requireAuth}/>
    <Redirect from='lecture' to='lecture/student' />
  </Route>
);

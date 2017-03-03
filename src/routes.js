import React from 'react';
import { Route, IndexRoute, Redirect } from 'react-router';

/* Routes */
import PageLayout from './components/PageLayout';
import Home from './components/Home';
import Lecture from './components/Lecture';
import NotFound from './components/NotFound';

const requireAuth = (nextState, replace) => {
  if (false) {
    replace({ pathname: '/' });
  }
};

export default (
  <Route path='/' component={PageLayout}>
    <IndexRoute component={Home} />
    <Route path='lecture/student' component={() => (<Lecture userType='students' />)} />
    <Route path='lecture/professor' component={() => (<Lecture userType='professors' />)} onEnter={requireAuth}/>
    <Redirect from='lecture' to='lecture/student' />
    <Route path='*' component={NotFound} />
  </Route>
);

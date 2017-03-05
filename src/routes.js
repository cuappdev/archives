import React from 'react';
import { Route, IndexRoute, Redirect } from 'react-router';

/* Routes */
import PageLayout from './components/PageLayout';
import Home from './components/Home';
import Lecture from './components/Lecture';
import NotFound from './components/NotFound';
import Login from './components/Login';

const requireAuth = (nextState, replace) => {
  if (localStorage.getItem('password') !== 'shipit') {
    replace({ pathname: '/login' });
  }
};

export default (
  <Route path='/' component={PageLayout}>
    <IndexRoute component={Home} />
    <Route path='lecture/student' component={() => (<Lecture userType='students' />)} />
    <Route path='lecture/professor' component={() => (<div></div>)} onEnter={requireAuth}/>
    <Route path='lecture/professor-appdev' component={() => (<Lecture userType='professors' />)}/>
    <Route path='login' component={Login} />
    <Redirect from='lecture' to='lecture/student' />
    <Route path='*' component={NotFound} />
  </Route>
);

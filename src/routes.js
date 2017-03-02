import React from 'react';
import { Route, IndexRoute, Router } from 'react-router';

/* Routes */
import PageLayout from './components/PageLayout';
import Home from './components/Home';
import Lecture from './components/Lecture';

export default (
  <Route path='/' component={PageLayout}>
    <IndexRoute component={Home} />
    <Route path='/lecture' component={Lecture} />
  </Route>
);

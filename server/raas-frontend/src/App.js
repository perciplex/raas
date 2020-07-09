import React from 'react';
import Jobs from './Jobs.jsx'
import Hardware from './Hardware.jsx'
import Submit from './Submit.jsx'
import Job from './Job.jsx'

import 'bootstrap/dist/css/bootstrap.min.css';
//import 'bootswatch/dist/flatly/bootstrap.min.css';
import './App.css';
import banner from './banner_small.png'
import { Container, Image } from 'react-bootstrap';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";


function App() {
  return (
    <div className="App">
      <Container>
        <a href="/">
          <Image src={banner} fluid></Image>
        </a>
      </Container>
      <Router>
        <Switch>
          <Route path="/status">
            <Hardware></Hardware></Route>
          <Route path="/submit">
            <Submit></Submit></Route>
          <Route path="/job/:jobId" component={Job}>
            <Job></Job></Route>
          <Route path="/">
            <Jobs></Jobs></Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;

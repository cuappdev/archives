import React, { Component } from 'react';
import { ButtonToolbar, DropdownButton, MenuItem } from 'react-bootstrap';
const BarChart = require('react-chartjs').Bar;

import utils from '../utils';

class LectureVisualizer extends Component {
  constructor(props) {
    super(props);

    this.state = {
      scaleSteps: 10,
      scaleStepWidth: 5
    };
  }

  handleScaleSteps(i, e) {
    this.setState({
      scaleSteps: i
    });

    this.forceUpdate();
  }

  handleScaleStepWidth(i, e) {
    this.setState({
      scaleStepWidth: i
    });

    this.forceUpdate();
  }

  render() {
    const chartProps = {
      data: {
        labels: this.props.choices.map((choice, i) => utils.alphabet[i]),
        datasets: [
            {
                fillColor: 'rgba(52, 152, 219,0.5)',
                strokeColor: 'rgba(52, 152, 219,1.0)',
                highlightFill: 'rgba(52, 152, 219,1.0)',
                highlightStroke: 'rgba(52, 152, 219,1.0)',
                data: this.props.choices.map((choice, i) => this.props.responseCounts[choice] || 0)
            }
        ]
      },
			options: {
        barStrokeWidth: 1,
        barValueSpacing: 10,
				responsive: true,
        scaleOverride: true,
        scaleSteps: this.state.scaleSteps,
        scaleStepWidth: this.state.scaleStepWidth,
        scaleStartValue: 0
			}
    };

    const scaleStepsMenu = Array(10).fill().map((_, i) => (
      <MenuItem
        key={i + 1}
        eventKey={i + 1}
        onSelect={(i, e) => this.handleScaleSteps(i, e)}
        active={this.state.scaleSteps === i + 1}>
        {i + 1}
      </MenuItem>
    ));

    const scaleStepWidthMenu = Array(10).fill().map((_, i) => (
      <MenuItem
        key={i + 1}
        eventKey={i + 1}
        onSelect={(i, e) => this.handleScaleStepWidth(i, e)}
        active={this.state.scaleStepWidth === i + 1}>
        {i + 1}
      </MenuItem>
    ));

    const toolbar = (
      <ButtonToolbar>
        <DropdownButton title={`Steps: ${this.state.scaleSteps}`} id={'scalesteps-dropdown'}>
          {scaleStepsMenu}
        </DropdownButton>
        <DropdownButton title={`Interval: ${this.state.scaleStepWidth}`} id={'scalestepwidth-dropdown'}>
          {scaleStepWidthMenu}
        </DropdownButton>
      </ButtonToolbar>
    );

    return <BarChart {...chartProps} />
  }
}

export default LectureVisualizer;

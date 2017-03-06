import React, { Component } from 'react';
const BarChart = require('react-chartjs').Bar;

class LectureVisualizer extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const chartProps = {
      data: {
        labels: this.props.choices,
        datasets: [
            {
                fillColor: 'rgba(220,220,220,0.5)',
                strokeColor: 'rgba(220,220,220,0.8)',
                highlightFill: 'rgba(220,220,220,0.75)',
                highlightStroke: 'rgba(220,220,220,1)',
                data: this.props.choices.map((choice, i) => this.props.responseCounts[choice] || 0)
            }
        ]
      },
			options: {
        barValueSpacing: 10,
				responsive: true
			}
    };

    return (
      <div>
        <h3>Response Visualization</h3>
        <BarChart {...chartProps} />
      </div>
    )
  }
}

export default LectureVisualizer;

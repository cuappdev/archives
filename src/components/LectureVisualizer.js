import React, { Component } from 'react';
const BarChart = require('react-chartjs').Bar;

class LectureVisualizer extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const chartProps = {
      data: {
        labels: Object.keys(this.props.responseCounts),
        datasets: [
            {
                label: "My First dataset",
                fillColor: "rgba(220,220,220,0.5)",
                strokeColor: "rgba(220,220,220,0.8)",
                highlightFill: "rgba(220,220,220,0.75)",
                highlightStroke: "rgba(220,220,220,1)",
                data: Object.keys(this.props.responseCounts).map((response, i) => this.props.responseCounts[response])
            }
        ]
      },
			options: {
				responsive: true
			}
    };

    return (
      <BarChart {...chartProps} />
    )
  }
}

export default LectureVisualizer;

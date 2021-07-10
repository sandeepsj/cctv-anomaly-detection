import { useTheme } from '@material-ui/core/styles';
import React from 'react';
import { Label, Line, LineChart, ResponsiveContainer, XAxis, YAxis } from 'recharts';
import Title from './Title';

function getPaddedData(dataGraph, padding){
  // const data = []
  // for(var i = 0; i < dataGraph.length; i++){
  //   data.push({
  //     frame: dataGraph[i].frame,
  //     reconstructionCost: dataGraph[i].reconstructionCost - padding
  //   })
  // }
  // return(data)
  return dataGraph
}
export default function Chart(props) {
  const theme = useTheme();
  return (
    <React.Fragment>
      <Title>Frame vs Anomaly Score </Title>
      <ResponsiveContainer>
        <LineChart
          data={getPaddedData(props.graphData, props.padding)}
          margin={{
            top: 16,
            right: 16,
            bottom: 0,
            left: 24,
          }}
        >
          <XAxis dataKey="frame" stroke={theme.palette.text.secondary} />
          <YAxis stroke={theme.palette.text.secondary} domain={[0, 100]}>
            <Label
              angle={270}
              position="left"
              style={{ textAnchor: 'middle', fill: theme.palette.text.primary }}
            >
              Reconstruction Cost
            </Label>
          </YAxis>
          <Line type="monotone" dataKey="reconstructionCost" stroke={theme.palette.primary.main} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}
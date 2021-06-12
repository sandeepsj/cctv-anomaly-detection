import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import DashboardIcon from '@material-ui/icons/Dashboard';
import BarChartIcon from '@material-ui/icons/BarChart';
import LayersIcon from '@material-ui/icons/Layers';
import AssignmentIcon from '@material-ui/icons/Assignment';
import List from '@material-ui/core/List';
import CONST from  "./constants";

export default function SideBar(props) {
  const mainListItems = (
    <div>
      <ListItem button onClick={() => props.handleSetPage(CONST.PAGES_DASHBOARD)}>
        <ListItemIcon>
          <DashboardIcon />
        </ListItemIcon>
        <ListItemText primary="Dashboard" />
      </ListItem>
      <ListItem button onClick={() => props.handleSetPage(CONST.PAGES_DETECTOR)}>
        <ListItemIcon>
          <BarChartIcon />
        </ListItemIcon>
        <ListItemText primary="Detect Anomaly" />
      </ListItem>
      <ListItem button onClick={() => props.handleSetPage(CONST.PAGES_TRAINER)}>
        <ListItemIcon>
          <LayersIcon />
        </ListItemIcon>
        <ListItemText primary="Train Your Model" />
      </ListItem>
    </div>
  );

  const secondaryListItems = (
    <div>
      <ListSubheader inset>Config Editor</ListSubheader>
      <ListItem button onClick={() => props.handleSetPage(CONST.PAGES_PATH_CONFIGS)}>
        <ListItemIcon>
          <AssignmentIcon />
        </ListItemIcon>
        <ListItemText primary="Path Configs" />
      </ListItem>
      <ListItem button onClick={() => props.handleSetPage(CONST.PAGES_MODEL_CONFIGS)}>
        <ListItemIcon>
          <AssignmentIcon />
        </ListItemIcon>
        <ListItemText primary="Model Configs" />
      </ListItem>
      <ListItem button onClick={() => props.handleSetPage(CONST.PAGES_OTHER_CONFIGS)}>
        <ListItemIcon>
          <AssignmentIcon />
        </ListItemIcon>
        <ListItemText primary="Other Configs" />
      </ListItem>
    </div>
  );
  return (
    <div>
      <List>{mainListItems}</List>
      <List>{secondaryListItems}</List>
    </div>
  );

}

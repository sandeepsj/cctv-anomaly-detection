import AppBar from '@material-ui/core/AppBar';
import Badge from '@material-ui/core/Badge';
import CssBaseline from '@material-ui/core/CssBaseline';
import Divider from '@material-ui/core/Divider';
import Drawer from '@material-ui/core/Drawer';
import IconButton from '@material-ui/core/IconButton';
import { makeStyles } from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import MenuIcon from '@material-ui/icons/Menu';
import NotificationsIcon from '@material-ui/icons/Notifications';
import axios from "axios";
import clsx from 'clsx';
import React from 'react';
import { defConfig } from "./Configs";
import CONST from "./constants";
import SideBar from "./listItems";
import Dashboard from "./pages/dashboard/Dashboard";
import Detector from './pages/detector/detector';
import ModelConfigs from "./pages/modelConfigs/configForm";
import OtherConfigs from "./pages/otherConfigs/configForm";
import PathConfigs from "./pages/pathConfigs/configForm";
const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  toolbar: {
    paddingRight: 24, // keep right padding when drawer closed
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: 36,
  },
  menuButtonHidden: {
    display: 'none',
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing(7),
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing(9),
    },
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    height: '100vh',
    overflow: 'auto',
  },
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  fixedHeight: {
    height: 240,
  },
}));

function createDataPoint(frame, reconstructionCost) {
  return { frame, reconstructionCost };
}
const firstAnomalousFrame = {};

export default function Main() {
  const classes = useStyles();
  const [open, setOpen] = React.useState(true);
  const [page, setPage] = React.useState(CONST.PAGES_DETECTOR);
  const [configs, setConfig] = React.useState(defConfig);
  const [curFrame, setCurFrame] = React.useState(1);
  const [graphData, setGraphData] = React.useState([])
  const [anomalyRange, setAnomalyRange] = React.useState({})
  
  const playVideo = (cur, end) =>{
    console.log(cur, end, "here");
    if(cur<=end){
      setTimeout(() => {
        setCurFrame(cur + 1);
        playVideo(cur+1, end);
      }, 200);
    }
  }

  const startVideoAndDetectAnomaly = (frame) => {
    if (frame < 200) {
      axios.post('/getRecustructionCost', {frame: frame, test_set_path: configs.TESTSET_PATH, test_case:configs.SINGLE_TEST_CASE_NAME})
      .then(
        response => {
          const frameCount = response.data.frame;
          const rc = response.data.rc;
          graphData.push(createDataPoint(frameCount, rc));
          if(rc>defConfig.THRESHOLD_VALUE){
            firstAnomalousFrame[frameCount] = firstAnomalousFrame[frameCount-1];
            if (firstAnomalousFrame[frameCount] === undefined){
              firstAnomalousFrame[frameCount] = frameCount;
            }
            anomalyRange[firstAnomalousFrame[frameCount]] = frameCount;
          }
          setAnomalyRange(anomalyRange);
          setGraphData([...graphData]);
          setCurFrame(frame + 1);
          startVideoAndDetectAnomaly(frame+1)
        }
      );      
      // setTimeout(() => , 300);
    }

  }
  const handleDrawerOpen = () => {
    setOpen(true);
  };
  const handleDrawerClose = () => {
    setOpen(false);
  };
  const handleSetPage = (page) => {
    setPage(page)
  }
  const fixedHeightPaper = clsx(classes.paper, classes.fixedHeight);

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar position="absolute" className={clsx(classes.appBar, open && classes.appBarShift)}>
        <Toolbar className={classes.toolbar}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            className={clsx(classes.menuButton, open && classes.menuButtonHidden)}
          >
            <MenuIcon />
          </IconButton>
          <Typography component="h1" variant="h6" color="inherit" noWrap className={classes.title}>
            Anomaly Detection from CCTV footage using Machine learning model.
          </Typography>
          <IconButton color="inherit">
            <Badge badgeContent={4} color="secondary">
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        classes={{
          paper: clsx(classes.drawerPaper, !open && classes.drawerPaperClose),
        }}
        open={open}
      >
        <div className={classes.toolbarIcon}>
          <IconButton onClick={handleDrawerClose}>
            <ChevronLeftIcon />
          </IconButton>
        </div>
        <Divider />
        <SideBar handleSetPage={handleSetPage} />

      </Drawer>
      <main className={classes.content}>
        <div className={classes.appBarSpacer} />

        {page === CONST.PAGES_MODEL_CONFIGS ?
          <ModelConfigs classes={classes} configs={configs} setConfig={setConfig} />
          : page === CONST.PAGES_PATH_CONFIGS ?
            <PathConfigs setAnomalyRange={setAnomalyRange} setGraphData={setGraphData} classes={classes} configs={configs} setConfig={setConfig} setCurFrame={setCurFrame}/>
            : page === CONST.PAGES_OTHER_CONFIGS ?
              <OtherConfigs classes={classes} configs={configs} setConfig={setConfig} />
              : page === CONST.PAGES_DETECTOR ?
                <Detector graphData={graphData} fixedHeightPaper={fixedHeightPaper} classes={classes} configs={configs} setConfig={setConfig} curFrame={curFrame} startVideoAndDetectAnomaly={startVideoAndDetectAnomaly} anomalyRange={anomalyRange} playVideo={playVideo}/>
                :
                <Dashboard fixedHeightPaper={fixedHeightPaper} classes={classes} configs={configs} setConfig={setConfig} />


        }
      </main>
    </div>

  );
}

import * as React from 'react';
import AppBar from '@material-ui/core/AppBar';
import { makeStyles } from '@material-ui/core/styles';
import { Link } from 'react-router-dom';
import Box from '@material-ui/core/Box';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import Menu from '@material-ui/core/Menu';
import MenuIcon from '@material-ui/icons/Menu';
import Container from '@material-ui/core/Container';
// import Avatar from '@mui/material/Avatar';
import Button from '@material-ui/core/Button';
import Tooltip from '@material-ui/core/Tooltip';
import MenuItem from '@material-ui/core/MenuItem';
import AccountCircle from '@material-ui/icons/AccountCircle';
// import AdbIcon from '@material-ui/icons/AdbIcon';
const settings = ['Dashboard','Profile', 'Friends', 'Logout'];

export default function TopAppBar() {
  const [anchorElUser, setAnchorElUser] = React.useState(null);

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  return (
    // *MUI DOCUMENTATION REFERENCED, https://mui.com/material-ui/react-app-bar/#MenuAppBar.js
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            edge="start"
            variant="h5"
            style={{marginLeft:'2%'}}
          >
            Social.ly
          </Typography>

          <Box>
            <IconButton onClick={handleOpenUserMenu}>
              <AccountCircle fontSize='medium' style={{ color: 'white' }}></AccountCircle>
            </IconButton>
            <Menu
              sx={{ mt: '45px' }}
              id="user_menu"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
               <MenuItem onClick={handleCloseUserMenu} component={Link} to="/main">
                <Typography textAlign="center">Dashboard</Typography>
              </MenuItem>
                <MenuItem onClick={handleCloseUserMenu} component={Link} to="/profile">
                <Typography textAlign="center">Profile</Typography>
              </MenuItem>
              <MenuItem onClick={handleCloseUserMenu} component={Link} to="/followers">
                <Typography textAlign="center">Followers</Typography>
              </MenuItem>
              <MenuItem onClick={handleCloseUserMenu} component={Link} to="/">
                <Typography textAlign="center">Logout</Typography>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
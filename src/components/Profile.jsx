import * as React from 'react';
import { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Button, Card, CardActions, CardContent, CardMedia, TextField, Typography } from '@material-ui/core';
//import { Link } from 'react-router-dom';
import AppBar from '../MainPage/AppBar';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'float',
    justifyContent: 'center',
    alignItems: 'center',
    textAlign: 'center',
    padding: theme.spacing(10),
  },
  card: {
    maxWidth: 600,
    margin: '0 auto',
    marginTop: theme.spacing(4),
  },
  media: {
    height: 200,
    width : 200,
    margin: '0 auto',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    margin: theme.spacing(2),
  },
  formField: {
    margin: theme.spacing(1),
  },
  cardActions: {
    display: 'float',
    justifyContent: 'space-between',
  },
}));

function Profile({ user, onSave }) {
  const classes = useStyles();
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState(user.name);
  const [bio, setBio] = useState(user.bio);
  const [image, setImage] = useState(user.image);

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleBioChange = (event) => {
    setBio(event.target.value);
  };

  const handleImageChange = (event) => {
    setImage(event.target.value);
  };

  const handleEditProfile = () => {
    setEditing(true);
  };

  const handleSaveProfile = () => {
    const newUser = { ...user, name, bio, image };
    onSave(newUser);
    setEditing(false);
  };

  return (
    <div className={classes.root}>
      <AppBar /> 
      {editing ? (
        <div className={classes.form}>
          <TextField
            className={classes.formField}
            label="Name"
            value={name}
            onChange={handleNameChange}
          />
          <TextField
            className={classes.formField}
            label="Bio"
            value={bio}
            onChange={handleBioChange}
          />
          <TextField
            className={classes.formField}
            label="Image URL"
            value={image}
            onChange={handleImageChange}
          />
          <Button variant="contained" color="primary" onClick={handleSaveProfile}>
            Save
          </Button>
        </div>
      ) : (
        <Card className={classes.card}>
          <CardMedia className={classes.media} image={user.image} title="Profile Image" />
          <CardContent>
            <Typography variant="h5" component="h2">
              {user.name}
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              {user.bio}
            </Typography>
          </CardContent>
          <CardActions>
            <Button size="small" color="primary" onClick={handleEditProfile}>
              Edit Profile
            </Button>
          </CardActions>
        </Card>
      )}
    </div>
  );
}
export default Profile;

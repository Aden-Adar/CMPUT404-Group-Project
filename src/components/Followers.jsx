import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AppBar from '../MainPage/AppBar';
import { Button, Card, CardActions, CardContent, CardMedia, TextField, Typography } from '@material-ui/core';

//const AUTHOR_ID = window.localStorage.getItem("UUID")
const GROUP1URL = "https://social-distribution-w23-t17.herokuapp.com/"
const GROUP1CREDS = btoa("remote-user-t22:pZHAe3PWukpd3Nv")

function FollowersPage() {
  const [followers, setFollowers] = useState(null);
  const [displayName, setDisplayName] = useState('');
  const [selectedUser, setSelectedUser] = useState(null);
  const [allAuthors, setAuthors] = useState(null);
  const current_author = JSON.parse(window.localStorage.getItem("Author"));
  const AUTHOR_ID = current_author.id;


  useEffect(() => {
    const fetchFollowers = async () => {
      const response = await axios.get(AUTHOR_ID+'followers/');
      setFollowers(response.data.items);
    };

    fetchFollowers();
  }, [AUTHOR_ID]);

  useEffect(() => {
    const fetchAuthors = async () => {
      const response = await axios.get('/service/authors/');
      setAuthors(response.data.items);
    };

    fetchAuthors();
  }, []);

  // const handleShowAuthors = async () => {
  //   const author_response =  await axios.get('/service/authors/');
  //   const auth_list = author_response.response.data.items;
  //   const authorList = auth_list.map(author => (
  //     <p key={author.id}>{author.displayName}</p>
  //   ));
  //   setAuthors(authorList);
  // };

  let followersList = null;
  if (followers) {
    followersList = followers.map((follower) => {
    let splitID = follower.id.split('/');
    let foreignID = splitID[splitID.length - 2];
  return (
      <Card key={follower.id}>
      <CardContent>
        <Typography variant="h5" component="h2">
          {follower.displayName}
        </Typography>
        <button onClick={() => fetch(AUTHOR_ID+'followers/'+foreignID+'/',{method:'DELETE'})}>Unfollow</button>
      </CardContent>
    </Card>
    )
  });
  } else {
    followersList = <p>No followers</p>
  }

  let authorsList = null;
  if (allAuthors) {
    authorsList = allAuthors.map((author) => {
  return (
      <Card key={author.id}>
      <CardContent>
        <Typography variant="h5" component="h2">
          {author.displayName}
        </Typography>
      </CardContent>
    </Card>
    )
  });
  } 

  const handleAddFriend = async () => {
    const response = await axios.get('/service/authors/');
    const group1Res = await fetch(GROUP1URL+'authors/', {
      method: 'GET',
      headers: {
          'Authorization': 'Basic ' + GROUP1CREDS,
          'Access-Control-Request-Method': 'GET' 
      }
    })
    const group1Authors = await group1Res.json()
    console.log(group1Authors)
    const followRemoteUser = group1Authors.items.find((item) => item.displayName === displayName);
    const followUser = response.data.items.find((item) => item.displayName === displayName);
    const FOREIGN_AUTHOR_ID = followUser.id;
    const current_author = JSON.parse(window.localStorage.getItem("Author"));
    const current_author_id = current_author.id;
    const currentUser = response.data.items.find((item) => item.id === current_author_id);
    console.log('user to follow:', followUser);
    console.log('CURRENT USER:', currentUser);
    if (followUser) {
      
      setSelectedUser(followUser);
      await axios.post(FOREIGN_AUTHOR_ID+'inbox/', {
        type: 'Follow',
        summary: `${currentUser.displayName} wants to follow ${followUser.displayName}`,
        actor: currentUser,
        object: followUser,
      });

    }
    else if (followRemoteUser) {
    //   const followRemoteUser = group1Authors.items.find((item) => item.displayName === displayName);
        const FOREIGN_AUTHOR_ID = followRemoteUser.id;
    //   console.log(FOREIGN_AUTHOR_ID);
    //   const currentUser = JSON.parse(window.localStorage.getItem("Author"))
    //   console.log('user to follow:', followRemoteUser);
    //   console.log('CURRENT USER:', currentUser);

     setSelectedUser(followRemoteUser);
      let followBody = {
        'type': 'followers',
        'summary': `${currentUser.displayName} wants to follow ${followRemoteUser.displayName}`,
        'actor': currentUser,
        'object': followRemoteUser,
      }
      await fetch(GROUP1URL + `authors/${FOREIGN_AUTHOR_ID}/inbox/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Basic ' + GROUP1CREDS,
          'Access-Control-Request-Method': 'POST' 
        },
        body: JSON.stringify(followBody)
      });


    } else {
      console.log(`User with display name ${displayName} not found`);
    }
  };

  return (
    <div>
      <AppBar />
    <div>
      <input 
      type="text" value={displayName} onChange={(e) => setDisplayName(e.target.value)} 
      style={{ border: '2px solid #ccc', padding: '8px', backgroundColor: 'lightgray', color: 'black'}} />
      <button onClick={handleAddFriend}>Add Friend</button>
    </div>
    <h2>Followers</h2>
    {selectedUser && (
      <div>
        <h3>
        Follow request sent to:<p>{selectedUser.displayName}</p>
        </h3>
      </div>
    )}
    <Card>{followersList}</Card>
    <h2>All Authors</h2>
    <Card>{authorsList}</Card>

  
  </div>
  );
};

export default FollowersPage;

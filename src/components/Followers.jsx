import React, { useState, useEffect } from 'react';
import { Buffer } from "buffer"
import axios from 'axios';
import AppBar from '../MainPage/AppBar';
import { Button, Card, CardActions, CardContent, CardMedia, TextField, Typography } from '@material-ui/core';

//const AUTHOR_ID = window.localStorage.getItem("UUID")
const GROUP1URL = "https://social-distribution-w23-t17.herokuapp.com/"
const GROUP1CREDS = Buffer.from("remote-user-t22:pZHAe3PWukpd3Nv").toString('base64')

const GROUP2URL = "https://floating-fjord-51978.herokuapp.com/"
const GROUP2CREDS = Buffer.from("admin:admin").toString('base64')

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
      let authors = []
      for (let i = 0; i < response.data.items.length; i++) {
        if (!response.data.items[i].id.includes(GROUP1URL) && !response.data.items[i].id.includes(GROUP2URL)) {
          authors.push(response.data.items[i])
        }
      } 
      setAuthors(authors);
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
    const group1Authors = await axios.get(GROUP1URL+'authors/?page=1&size=150', {
      headers: {
          'Authorization': 'Basic ' + GROUP1CREDS,
          'Access-Control-Request-Method': 'GET' 
      }
    })
    const group2Authors = await axios.get(GROUP2URL+'authors/?page=1&size=150', {
      headers: {
          'Authorization': 'Basic ' + GROUP2CREDS,
          'Access-Control-Request-Method': 'GET' 
      }
    })
    const Group1RemoteUser = group1Authors.data.items.find((item) => item.displayName === displayName);
    const Group2RemoteUser = group2Authors.data.items.find((item) => item.displayName === displayName);
    const localUser = response.data.items.find((item) => item.displayName === displayName);
    const current_author = JSON.parse(window.localStorage.getItem("Author"));
    const current_author_id = current_author.id;
    const currentUser = response.data.items.find((item) => item.id === current_author_id);
    console.log('user to follow:', localUser);
    console.log('group 1 user to follow:', Group1RemoteUser);
    console.log('group 2 user to follow:', Group2RemoteUser);
    console.log('CURRENT USER:', currentUser);
    if (localUser) {

      const FOREIGN_AUTHOR_ID = localUser.id;
      setSelectedUser(localUser);
      await axios.post(FOREIGN_AUTHOR_ID+'inbox/', {
        type: 'Follow',
        summary: `${currentUser.displayName} wants to follow ${localUser.displayName}`,
        actor: currentUser,
        object: localUser,
      });

    } else if (Group1RemoteUser) {
      const GROUP1_AUTHOR_ID = Group1RemoteUser.id;
      setSelectedUser(Group1RemoteUser);
      let followBody = {
        'type': 'Follow',
        'summary': `${currentUser.displayName} wants to follow ${Group1RemoteUser.displayName}`,
        'actor': currentUser,
        'object': Group1RemoteUser,
      }
      await axios.post(GROUP1URL + `authors/${GROUP1_AUTHOR_ID}/inbox/`,JSON.stringify(followBody),{
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Basic ' + GROUP1CREDS,
          'Access-Control-Request-Method': 'POST' 
        },
      });
    } else if (Group2RemoteUser) {
      const GROUP2_AUTHOR_ID = Group2RemoteUser.id;
      setSelectedUser(Group2RemoteUser);
      let followBody = {
        'type': 'Follow',
        'summary': `${currentUser.displayName} wants to follow ${Group2RemoteUser.displayName}`,
        'actor': currentUser,
        'object': Group2RemoteUser,
      }
      await axios.post(GROUP2_AUTHOR_ID+'/inbox',JSON.stringify(followBody),{
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Basic ' + GROUP2CREDS,
          'Access-Control-Request-Method': 'POST' 
        },
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

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AppBar from '../MainPage/AppBar';

const AUTHOR_ID = window.localStorage.getItem("UUID")

const FollowersPage = ({ AUTHOR_ID }) => {
  const [followers, setFollowers] = useState([]);
  const [displayName, setDisplayName] = useState('');
  const [selectedUser, setSelectedUser] = useState(null);

//   useEffect(() => {
//     const fetchFollowers = async () => {
//       const response = await axios.get(`/service/authors/${AUTHOR_ID}/followers/`);
//       setFollowers(response.data.items);
//     };

//     fetchFollowers();
//   }, [AUTHOR_ID]);

  const handleAddFriend = async () => {
    const response = await axios.get('/service/authors/');
    const followUser = response.data.items.find((item) => item.displayName === displayName);
    const FOREIGN_AUTHOR_ID = followUser.id;
    const current_author_ID = window.localStorage.getItem("UUID");
    console.log(FOREIGN_AUTHOR_ID);
    const currentUser = response.data.items.find((item) => item.id === current_author_ID);
    console.log('user to follow:', followUser);
    console.log('CURRENT USER:', currentUser);

    if (followUser) {
      setSelectedUser(followUser);
      await axios.post(`/service/authors/${FOREIGN_AUTHOR_ID}/inbox/`, {
        type: 'Follow',
        summary: `${currentUser.displayName} wants to follow ${followUser.displayName}`,
        actor: currentUser,
        object: followUser,
      });

      const updatedFollowersResponse = await axios.get(`/service/authors/${AUTHOR_ID}/followers/`);
      //setFollowers(updatedFollowersResponse.data.items);
    } else {
      console.log(`User with display name ${displayName} not found`);
    }
  };

  return (
    <div>
        <AppBar />     
        <h2>Followers</h2>
        {followers.map((follower) => (
        <div key={follower.id}>
        <p>{follower.displayName}</p>
        </div>
        ))}
        <div>
        <input type="text" value={displayName} onChange={(e) => setDisplayName(e.target.value)} />
        <button onClick={handleAddFriend}>Add Friend</button>
        </div>
        {selectedUser && (
        <div>
        <h3>Selected User</h3>
        <p>{selectedUser.displayName}</p>
        </div>
        )}
        </div>
        );
    };
    
    export default FollowersPage;

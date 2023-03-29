import * as React from 'react';
import { Grid, Button, ButtonGroup } from '@material-ui/core';
import TopAppBar from './AppBar'
import PostCard from './Post';
import LikeCard from './Like'
import CommentCard from './CommentCard';
import FollowCard from './FollowCard';
import { getExplorePosts, getMyPosts, getInbox } from '../API/mainRequests';

export const Main = () => {
    const AUTHOR_ID = window.localStorage.getItem("UUID")
    const AUTHOR = window.localStorage.getItem("Author")
    console.log(AUTHOR_ID)
    console.log(AUTHOR)
    const [inboxFlag, setInboxFlag] = React.useState(false);
    const [exploreFlag, setExploreFlag] = React.useState(true);
    const [myPostsFlag, setMyPostsFlag] = React.useState(false);
    const [myPosts, setMyPosts] = React.useState([]);
    const [explorePosts, setExplorePosts] = React.useState([]);
    const [inbox, setInbox] = React.useState([]);

    // Manage what tab we're on and re-render accordingly
    function handleTabClick(option) {
        if (option === 'inbox') {
            setInboxFlag(true);
            setExploreFlag(false)
            setMyPostsFlag(false);
        } else if (option === 'explore') {
            setInboxFlag(false);
            setExploreFlag(true)
            setMyPostsFlag(false);
        } else {
            setInboxFlag(false);
            setExploreFlag(false)
            setMyPostsFlag(true);
        }
    };

    // API CALL TO GET EXPLORE POSTS
    React.useEffect(() => {
        getExplorePosts().then(posts => {
            console.log(posts)
            setExplorePosts(posts);
        });
    }, []);

    // API CALL TO GET MY POSTS
    React.useEffect(() => {
        getMyPosts().then(posts => {
            setMyPosts(posts);
        });
    }, []);

    // API CALL TO GET INBOX
    React.useEffect(() => {
        getInbox().then(posts => {
            setInbox(posts);
        });
    }, []);

    return (
        <Grid container spacing={2} alignItems="center" justifyContent="center">
            <Grid item xs={12}>
                <TopAppBar></TopAppBar>
            </Grid>
            <Grid item xs={12} style={{textAlign:'center'}}>
                <ButtonGroup variant="contained" aria-label="tabButtonGroup">
                    <Button onClick={() => handleTabClick('explore')}>Explore</Button>
                    <Button onClick={() => handleTabClick('inbox')}>Inbox</Button>
                    <Button onClick={() => handleTabClick('myPosts')}>My Posts</Button>
                </ButtonGroup>
            </Grid>
            {inboxFlag && <Grid item xs={12} style={{textAlign:'center'}}>
                <ButtonGroup variant="contained" aria-label="tabButtonGroup">
                    <Button>All</Button>
                    <Button>Posts</Button>
                    <Button>Comments</Button>
                    <Button>Likes</Button>
                </ButtonGroup>
            </Grid>}
            {myPosts.length>0 && myPostsFlag && myPosts.map(post => (
                <Grid item xs={8} justifyContent="center">
                <PostCard
                    currentAuthorID={AUTHOR_ID}
                    author={post.author}
                    comments={post.comments_set}
                    contentType={post.content_type}
                    content={post.content}
                    title={post.title}
                    visibility={post.visibility}
                    published={post.published}
                    post_id={post.post_id}
                    url={post.id}
                />
                </Grid>
            ))}
            {explorePosts.length>0 && exploreFlag && explorePosts.map(post => (
                <Grid item xs={8} justifyContent="center">
                <PostCard
                    currentAuthorID={AUTHOR_ID}
                    author={post.author}
                    comments={post.comments_set}
                    contentType={post.content_type}
                    content={post.content}
                    title={post.title}
                    visibility={post.visibility}
                    published={post.published}
                    post_id={post.post_id}
                    url={post.id}
                />
                </Grid>
            ))}
            {inbox.length>0 && inboxFlag && inbox.map(item => (
                <Grid item xs={8} justifyContent="center">
                    {item.type === "post" && <PostCard
                        currentAuthorID={AUTHOR_ID}
                        author={item.author}
                        comments={item.comments_set}
                        contentType={item.content_type}
                        content={item.content}
                        title={item.title}
                        visibility={item.visibility}
                        published={item.published}
                        post_id={item.post_id}
                        url={item.id} />}
                    {item.type === "Like" && <LikeCard
                        author={item.author}
                        summary={item.summary}
                        object={item.object} />}
                    {item.type === "comment" && <CommentCard
                        author={item.author}
                        comment={item.comment}
                        published={item.published} />}
                    {item.type === "Follow" && <FollowCard
                        summary={item.summary}
                        actor={item.actor}
                        object={item.object} />} 
                </Grid>
            ))}
        </Grid>
    )
}
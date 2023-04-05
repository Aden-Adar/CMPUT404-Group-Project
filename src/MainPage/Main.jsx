import * as React from 'react';
import { Grid, Button, ButtonGroup } from '@material-ui/core';
import { Pagination } from '@mui/material';
import TopAppBar from './AppBar'
import PostCard from './Post';
import LikeCard from './Like'
import CommentCard from './CommentCard';
import FollowCard from './FollowCard';
import { getExplorePosts, getMyPosts, getInbox } from '../API/mainRequests';

export const Main = () => {
    const UUID = window.localStorage.getItem("UUID")
    const AUTHOR = window.localStorage.getItem("Author")

    const [inboxFlag, setInboxFlag] = React.useState(false);
    const [exploreFlag, setExploreFlag] = React.useState(true);
    const [myPostsFlag, setMyPostsFlag] = React.useState(false);
    const [myPosts, setMyPosts] = React.useState([]);
    const [explorePosts, setExplorePosts] = React.useState([]);
    const [inbox, setInbox] = React.useState([]);
    const [page, setPage] = React.useState(1);

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
        getExplorePosts(page).then(posts => {
            setExplorePosts(posts);
        });
    }, [page]);

    // API CALL TO GET MY POSTS
    React.useEffect(() => {
        getMyPosts(page).then(posts => {
            setMyPosts(posts);
        });
    }, []);

    // API CALL TO GET INBOX
    React.useEffect(() => {
        getInbox().then(posts => {
            setInbox(posts);
            console.log("INBOX ->", posts)
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
                    postAuthor={post.author}
                    commentsURL={post.comments}
                    contentType={post.content_type?post.content_type:post.contentType}
                    content={post.content}
                    title={post.title}
                    visibility={post.visibility}
                    published={post.published}
                    id={post.id}
                    postType="myposts"
                />
                </Grid>
            ))}
            {explorePosts.length>0 && exploreFlag && explorePosts.map(post => (
                <Grid item xs={8} justifyContent="center">
                <PostCard
                    postAuthor={post.author}
                    commentsURL={post.comments}
                    contentType={post.content_type?post.content_type:post.contentType}
                    content={post.content}
                    title={post.title}
                    visibility={post.visibility}
                    published={post.published}
                    id={post.id}
                    postType="explore"
                />
                </Grid>
            ))}
            {inbox.length>0 && inboxFlag && inbox.map(item => (
                <Grid item xs={8} justifyContent="center">
                    {item.type === "post" && <PostCard
                        postAuthor={item.author}
                        commentsURL={item.comments}
                        contentType={item.content_type?item.content_type:item.contentType}
                        content={item.content}
                        title={item.title}
                        visibility={item.visibility}
                        published={item.published}
                        id={item.id}
                        postType="inbox" />}
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
            <Grid item xs={12}>
            </Grid>
            <Grid item xs={4.5}>
                <Pagination count={10} shape="rounded" onChange={(e, page) => setPage(page)}/>
            </Grid>
        </Grid>
    )
}
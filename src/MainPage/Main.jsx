import * as React from 'react';
import { Grid, Button, ButtonGroup } from '@material-ui/core';
import TopAppBar from './AppBar'
import PostCard from './Post';
import LikeCard from './Like'
import CommentCard from './CommentCard';

export const Main = () => {
    const AUTHOR_ID = 'e654cd42-cae7-4934-aaf5-514d62d446d4'
    console.log(AUTHOR_ID)
    const [inboxFlag, setInboxFlag] = React.useState(true);
    const [exploreFlag, setExploreFlag] = React.useState(false);
    const [myPostsFlag, setMyPostsFlag] = React.useState(false);
    const [myPosts, setMyPosts] = React.useState([]);
    const [explorePosts, setExplorePosts] = React.useState([]);
    const [inbox, setInbox] = React.useState([]);

    console.log(inboxFlag, exploreFlag, myPostsFlag)

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
        async function getExplorePosts() {
            let posts = []
            let authorsResponse = await fetch('/service/authors/')
            let authorsRes_data = await authorsResponse.json()
            for (let i = 0; i < authorsRes_data.items.length; i++) {
                if (authorsRes_data.items[i].id !== AUTHOR_ID) {
                    let authorPosts = []
                    let response = await fetch(authorsRes_data.items[i].url + "posts/")
                    let res_data = await response.json()
                    // Filter out any of logged in users' posts
                    for (let j = 0; j < res_data.length; j++) {
                        if (res_data[j].visibility === "PUBLIC") {
                            authorPosts.push(res_data[j])
                        }
                    }
                    posts = posts.concat(authorPosts)
                }
            }
            setExplorePosts(posts);
        }
        getExplorePosts();
    }, []);

    // API CALL TO GET MY POSTS
    React.useEffect(() => {
        async function getMyPosts() {
            let response = await fetch('/service/authors/' + AUTHOR_ID + '/posts/')
            let res_data = await response.json()
            // console.log(res_data)
            setMyPosts(res_data);
        }
        getMyPosts();
    }, []);

    // API CALL TO GET INBOX
    React.useEffect(() => {
        async function getInbox() {
            let response = await fetch('/service/authors/' + AUTHOR_ID + '/inbox/')
            let res_data = await response.json()
            // console.log(res_data)
            setInbox(res_data.items);
        }
        getInbox();
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
                        post_id={item.post_id} />}
                    {item.type === "Like" && <LikeCard
                        author={item.author}
                        summary={item.summary}
                        object={item.object} />}
                    {item.type === "comment" && <CommentCard
                        author={item.author}
                        comment={item.comment}
                        published={item.published} />}
                </Grid>
            ))}
        </Grid>
    )
}
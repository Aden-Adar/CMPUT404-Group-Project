import * as React from 'react';
import { Buffer } from "buffer"

import { Card, CardContent, CardHeader, CardActions, IconButton, Typography, Collapse, List, Divider, ListItem, ListItemText, TextField, ListItemIcon } from '@material-ui/core';
import { Favorite, Comment, AccountCircle, Send } from '@material-ui/icons';

import CommentItem from './Comment';

function PostCard({
    postAuthor,
    comments,
    contentType,
    content,
    title,
    visibility,
    published,
    id
}) {
    const AUTHOR = window.localStorage.getItem("Author")
    const GROUP1URL = "https://social-distribution-w23-t17.herokuapp.com/"
    const GROUP1CREDS = Buffer.from("remote-user-t22:pZHAe3PWukpd3Nv").toString('base64')
    const group1Post = id.includes(GROUP1URL) ? true : false;
    const internalPost = group1Post ? false : true;
    const [liked, setLiked] = React.useState(false);
    const [comment, setComment] = React.useState('');
    const [commentExpanded, setCommentExpanded] = React.useState(false);

    // API CALL TO CHECK IF USER HAS ALREADY LIKED POST
    React.useEffect(() => {
      // Call to our BE
      if (internalPost) {
        async function getLikes() {
          let likesResponse = await fetch(id + 'likes/')
          let likesRes_data = await likesResponse.json()
          for (let i = 0; i < likesRes_data.results.length; i++) {
              if (likesRes_data.results[i].author.id === AUTHOR.id) {
                  setLiked(true)
              }
          }
          }
          getLikes();
      } else if (group1Post) {
      }
    }, []);

    React.useEffect(() => {
    }, [comments]);

    // POST LIKE TO INBOX
    function handleLikeClick() {
        if (!liked) {
          let likeBody = {
            "context": "https://www.w3.org/ns/activitystreams",
            "summary": JSON.parse(AUTHOR).displayName + " Likes your post",
            "type": "Like",
            "author": JSON.parse(AUTHOR),
            "object": id
          }
          setLiked(true)
          if (internalPost) {
            async function postLike() {
              let response = await fetch(postAuthor.id + 'inbox/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json'
                },
                body: JSON.stringify(likeBody)
              })
              let res_data = await response.json()
            }
            postLike();
          } else if (group1Post) {
            async function postLikeGroup1() {
              let response = await fetch(GROUP1URL + 'authors/' + postAuthor.id + '/inbox/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json',
                  'Authorization': 'Basic ' + GROUP1CREDS,
                  'Access-Control-Request-Method': 'POST' 
                },
                body: JSON.stringify(likeBody)
              })
              let res_data = await response.json()
            }
            postLikeGroup1();
          }
        }
    }

    // POST COMMENT TO POST & INBOX
    function handleSendCommentClick() {
        if (internalPost) {
          async function postComment() {
            let response = await fetch(id + 'comments/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              body: JSON.stringify({ "comment" : comment, "content_type" : "text/plain"})
            })
            let res_data = await response.json()
  
            // POST TO INBOX NOW
            let inboxRes = await fetch(postAuthor.id + 'inbox/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              body: JSON.stringify(res_data)
            })
            let inboxRes_data = await inboxRes.json()
            window.location.reload(false);
          }
          postComment();
        } else if (group1Post) {
          // async function postCommentGroup1() {
            // let today = new Date()
            // let commentBody = { 
            //   "comment" : comment, 
            //   "content_type" : "text/plain",
            //   "published": today.toISOString(),
            //   "type": "comment",
            //   "author": JSON.parse(AUTHOR)
            // }
            // let response = await fetch(GROUP1URL+ 'authors/' + author.id + '/posts/' + url + '/comments/', {
            //   method: 'POST',
            //   headers: {
            //     'Content-Type': 'application/json',
            //     'Accept': 'application/json',
            //     'Authorization': 'Basic ' + GROUP1CREDS,
            //     'Access-Control-Request-Method': 'POST',
            //   },
            //   body: JSON.stringify(commentBody)
            // })
            // let res_data = await response.json()
            // console.log(res_data)
            // POST TO INBOX NOW
            // let inboxRes = await fetch('/service/authors/' + author.id + '/inbox/', {
            //   method: 'POST',
            //   headers: {
            //     'Content-Type': 'application/json',
            //     'Accept': 'application/json'
            //   },
            //   body: JSON.stringify(res_data)
            // })
            // let inboxRes_data = await inboxRes.json()
            // console.log(inboxRes_data)
            // window.location.reload(false);
          // }
        }
    }

    return (
        <Card variant='outlined'>
          <CardHeader
            avatar={<AccountCircle fontSize='large'></AccountCircle>}
            title={
              <span>
                <Typography component="span" variant="body1">{postAuthor.displayName}</Typography><Typography component="span" style={{ color: '#a3a3a3' }}>{"  -  " + title}</Typography>
              </span>}
            subheader={published.substring(0, 10)}
          />
          <CardContent>
            <Typography variant="body1">
              {content}
            </Typography>
          </CardContent>
          <CardActions disableSpacing>
            <IconButton aria-label="like" onClick={handleLikeClick}>
              <Favorite style={{ color: liked? 'red' : '#a3a3a3' }}/>
            </IconButton>
            <IconButton aria-label="comment" onClick={() => setCommentExpanded(!commentExpanded)}>
              <Comment style={{ color: '#a3a3a3' }}/>
            </IconButton>
          </CardActions>
          <Collapse in={commentExpanded}>
            <List>
              {comments.length>0 && comments.map(comment => (
                  <><Divider variant='middle'></Divider><CommentItem
                  author={comment.author}
                  comment={comment.comment}
                  contentType={comment.contentType}
                  published={comment.published} /></>
              ))}
              <Divider></Divider>
              <ListItem>
                <ListItemText
                    primary={<TextField onChange={(e) => {setComment(e.target.value)}} fullWidth variant='standard' label='Comment here...'/>}
                />
                <ListItemIcon style={{'justify-content': 'center'}}>
                  <IconButton aria-label="send_comment" onClick={handleSendCommentClick}>
                    <Send  style={{ color: '#346beb' }}></Send>
                  </IconButton>
                </ListItemIcon>
              </ListItem>
            </List>
          </Collapse>
        </Card>
    );
}
export default PostCard;
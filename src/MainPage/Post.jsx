import * as React from 'react';

import { Avatar, Card, CardContent, CardHeader, CardActions, IconButton, Typography, Collapse, List, Divider, ListItem, ListItemText, TextField, ListItemIcon } from '@material-ui/core';
import { Favorite, Comment, AccountCircle, Send } from '@material-ui/icons';

import CommentItem from './Comment';
import LikeCard from './Like';

function PostCard({
    currentAuthorID,
    author,
    comments,
    contentType,
    content,
    title,
    visibility,
    published,
    post_id
}) {
    const [liked, setLiked] = React.useState(false);
    const [comment, setComment] = React.useState('');
    const [commentExpanded, setCommentExpanded] = React.useState(false);

    // API CALL TO CHECK IF USER HAS ALREADY LIKED POST
    React.useEffect(() => {
      async function getLikes() {
          let likesResponse = await fetch('/service/authors/' + author.id + '/posts/' + post_id + '/likes/')
          let likesRes_data = await likesResponse.json()
          for (let i = 0; i < likesRes_data.length; i++) {
              if (likesRes_data[i].author.id === currentAuthorID) {
                  setLiked(true)
              }
          }
      }
      getLikes();
    }, []);

    // POST LIKE TO INBOX
    function handleLikeClick() {
        if (!liked) {
            setLiked(true)
            async function postLike() {
              let response = await fetch('/service/authors/' + currentAuthorID + '/inbox/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json'
                },
                body: JSON.stringify({ "author_id" : author.id, "like_id" : { "post_id" : post_id}})
              })
              let res_data = await response.json()
              console.log(res_data)
            }
            postLike();
        }
    }

    // POST COMMENT TO POST & INBOX
    function handleSendCommentClick() {
        async function postComment() {
          let response = await fetch('/service/authors/' + currentAuthorID + '/posts/' + post_id + '/comments/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
            },
            body: JSON.stringify({ "comment" : comment, "content_type" : "text/plain"})
          })
          let res_data = await response.json()
          console.log(res_data)

          // POST TO INBOX NOW
          let inboxRes = await fetch('/service/authors/' + currentAuthorID + '/inbox/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
            },
            body: JSON.stringify({ "author_id" : author.id, "comment_id" : res_data.comment_id})
          })
          let inboxRes_data = await inboxRes.json()
          console.log(inboxRes_data)
        }
        postComment();
    }

    return (
        <Card variant='outlined'>
          <CardHeader
            avatar={<AccountCircle fontSize='large'></AccountCircle>}
            title={
              <span>
                <Typography component="span" variant="body1">{author.username}</Typography><Typography component="span" style={{ color: '#a3a3a3' }}>{"  -  " + title}</Typography>
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
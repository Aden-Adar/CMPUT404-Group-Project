import * as React from 'react';
import {v4 as uuid} from 'uuid';
import { Buffer } from "buffer"

import { Card, CardContent, CardHeader, CardActions, IconButton, Typography, Collapse, List, Divider, ListItem, ListItemText, TextField, ListItemIcon } from '@material-ui/core';
import { Favorite, Comment, AccountCircle, Send } from '@material-ui/icons';

import CommentItem from './Comment';
import ReactMarkdown from 'react-markdown'
import ReactDom from 'react-dom'


function PostCard({
    postAuthor,
    contentType,
    content,
    title,
    visibility,
    published,
    id,
    commentsURL,
    postType
}) {
    const InternalURL = "http://localhost:8000"

    const AUTHOR = window.localStorage.getItem("Author")
    const UUID = window.localStorage.getItem("UUID")

    const GROUP1URL = "https://social-distribution-w23-t17.herokuapp.com/"
    const GROUP1CREDS = Buffer.from("remote-user-t22:pZHAe3PWukpd3Nv").toString('base64')
    const group1Post = id.includes(GROUP1URL) ? true : false;

    const GROUP2URL = "https://floating-fjord-51978.herokuapp.com/"
    const GROUP2CREDS = Buffer.from("admin:admin").toString('base64')
    const group2Post = id.includes(GROUP2URL) ? true : false;
    
    const internalPost = (group1Post || group2Post) ? false : true;

    const [liked, setLiked] = React.useState(false);
    const [likes, setLikes] = React.useState(0);
    const [comment, setComment] = React.useState('');
    const [comments, setComments] = React.useState([]);
    const [commentExpanded, setCommentExpanded] = React.useState(false);

    // API CALL TO CHECK IF USER HAS ALREADY LIKED POST
    React.useEffect(() => {
      // Call to our BE
      if (internalPost) {
        async function getLikes() {
          let likesResponse = await fetch(id + '/likes')
          let likesRes_data = await likesResponse.json()
          for (let i = 0; i < likesRes_data.results.length; i++) {
              if (likesRes_data.results[i].author.id === JSON.parse(AUTHOR).id) {
                  setLiked(true)
              }
          }
          setLikes(likesRes_data.results.length)
          }
          getLikes();
      } else if (group1Post) {
        async function getLikes() {
          let likesResponse = await fetch(GROUP1URL+ 'authors/' + postAuthor.id + '/posts/' + id + '/likes/', {
            method: 'GET',
            headers: {
              'Authorization': 'Basic ' + GROUP1CREDS,
              'Access-Control-Request-Method': 'GET' 
            }
          })
          let likesRes_data = await likesResponse.json()
          for (let i = 0; i < likesRes_data.items.length; i++) {
              if (likesRes_data.items[i].author.url.includes(UUID)) {
                  setLiked(true)
              }
          }
          setLikes(likesRes_data.items.length)
          }
          getLikes();
      } else if (group2Post) {
        async function getLikes() {
          let likesResponse = await fetch(id + '/likes', {
            method: 'GET',
            headers: {
              'Authorization': 'Basic ' + GROUP2CREDS,
              'Access-Control-Request-Method': 'GET' 
            }
          })
          let likesRes_data = await likesResponse.json()
          for (let i = 0; i < likesRes_data.items.length; i++) {
              if (likesRes_data.items[i].author.id.includes(UUID)) {
                  setLiked(true)
              }
          }
          setLikes(likesRes_data.items.length)
          }
          getLikes();
      }
    }, []);

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
          setLikes(likes + 1)
          if (internalPost) {
            async function postLike() {
              let response = await fetch((postAuthor.id ? postAuthor.id : postAuthor.url) + 'inbox/', {
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

    function handleExpandComment() {
      setCommentExpanded(!commentExpanded)
      async function getComments() {
        if (group1Post) {
          let response = await fetch(commentsURL, {
            method: 'GET',
            headers: {
              'Authorization': 'Basic ' + GROUP1CREDS,
              'Access-Control-Request-Method': 'GET' 
            },
          })
          let res_data = await response.json()
          setComments(res_data)
        } else if (internalPost) {
          let response = await fetch(commentsURL)
          let res_data = await response.json()
          setComments(res_data)
        } else if (group2Post) {
          console.log("Comment url: ", commentsURL)
          let response = await fetch(commentsURL, {
            method: 'GET',
            headers: {
              'Authorization': 'Basic ' + GROUP2CREDS,
              'Access-Control-Request-Method': 'GET' 
            },
          })
          let res_data = await response.json()
          console.log("comment data: ", res_data)
          setComments(res_data)
        }
      }
      getComments()
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
              body: JSON.stringify({ "comment" : comment, "content_type" : "text/plain", "author": JSON.parse(AUTHOR)})
            })
            let res_data = await response.json()
  
            // POST TO INBOX NOW
            let inboxRes = await fetch((postAuthor.id ? postAuthor.id : postAuthor.url) + 'inbox/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              body: JSON.stringify(res_data)
            })
            let inboxRes_data = await inboxRes.json()
            setComments(comments.push(res_data))
            // window.location.reload(false);
          }
          postComment();
        } else if (group1Post) {
          async function postCommentGroup1() {
            let uid = uuid()
            let today = new Date()
            let commentBody = { 
              "comment" : comment, 
              "content_type" : "text/plain",
              "published": today.toISOString(),
              "type": "comment",
              "author": JSON.parse(AUTHOR),
              "id": GROUP1URL+ 'authors/' + postAuthor.id + '/posts/' + id + '/comments/' + uid
            }
            let inboxRes = await fetch(GROUP1URL + 'authors/' + postAuthor.id + '/inbox/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Basic ' + GROUP1CREDS,
                'Access-Control-Request-Method': 'POST' 
              },
              body: JSON.stringify(commentBody)
            })
            let inboxRes_data = await inboxRes.json()
            setComments(commentBody)
            console.log(inboxRes_data)
            // window.location.reload(false);
          }
          postCommentGroup1()
        } else if (group2Post) {
          async function postCommentGroup2() {
            let today = new Date()
            let commentBody = { 
              "comment" : comment, 
              "contenType" : "text/plain",
              "published": today.toISOString(),
              "type": "comment",
              "author": JSON.parse(AUTHOR),
              "id": commentsURL
            }
            let inboxRes = await fetch(postAuthor.id + '/inbox', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Basic ' + GROUP2CREDS,
                'Access-Control-Request-Method': 'POST' 
              },
              body: JSON.stringify(commentBody)
            })
            let inboxRes_data = await inboxRes.json()
            setComments(commentBody)
            console.log(inboxRes_data)
            // window.location.reload(false);
          }
          postCommentGroup2()
        }
      }
    return (
        <Card variant='outlined'>
          <CardHeader
            avatar={<AccountCircle fontSize='large'></AccountCircle>}
            title={
              <span>
                <Typography component="span" variant="body1">{(!internalPost ? '(remote) ' : '') + postAuthor.displayName}</Typography><Typography component="span" style={{ color: '#a3a3a3' }}>{"  -  " + title}</Typography>
              </span>}
            subheader={published.substring(0, 10)}
          />
          <CardContent>
              {contentType === 'image/png;base64' && id.includes(GROUP2URL) &&
                <Typography variant="body1">
                {
                  <img src={content}/>
                }
                </Typography>
              }
              {contentType === 'image/jpeg;base64' && id.includes(GROUP2URL) &&
                <Typography variant="body1">
                {
                  <img src={content}/>
                }
                </Typography>
              }
              {contentType === 'image/jpeg' && id.includes(GROUP1URL) &&
                <Typography variant="body1">
                {
                  <img src={`data:image/jpeg;base64,${content}`}/>
                }
                </Typography>
              }
              {contentType === 'image/png' && id.includes(GROUP1URL) &&
                <Typography variant="body1">
                {
                  <img src={`data:image/jpeg;base64,${content}`}/>
                }
                </Typography>
              }
              {contentType === 'application/base64' && 
                <Typography variant="body1">
                {
                  <img src={`data:image/jpeg;base64,${content}`}/>
                }
                </Typography>
              }
              {contentType === 'image/png;base64' &&  internalPost &&
                <Typography variant="body1">
                {
                  <img src={`data:image/jpeg;base64,${content}`}/>
                }
                </Typography>
              }
              {contentType === 'image/jpeg;base64' && internalPost &&
                <Typography variant="body1">
                {
                  <img src={`data:image/jpeg;base64,${content}`}/>
                }
                </Typography>
              }
              {contentType === 'text/plain' &&//|| contentType === 'text/markdown'&&
                <Typography variant="body1">
                {
                  content
                }
                </Typography>
              }
              {contentType === 'text/markdown' &&//|| contentType === 'text/markdown'&&
                <Typography variant="body1">
                {
                  <ReactMarkdown>
                    {content}
                  </ReactMarkdown>
                  
                }
                </Typography>
              }


          </CardContent>
          {postType !== "myposts" &&
            <CardActions disableSpacing>
              <IconButton aria-label="like" onClick={handleLikeClick}>
                <Favorite style={{ color: liked? 'red' : '#a3a3a3' }}/>
              </IconButton>
              <Typography>{likes} </Typography>
              <IconButton aria-label="comment" onClick={handleExpandComment}>
                <Comment style={{ color: '#a3a3a3' }}/>
              </IconButton>
            </CardActions>
          }
          <Collapse in={commentExpanded}>
            <List>
              {visibility === "PUBLIC" && comments.length>0 && comments.map(comment => (
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